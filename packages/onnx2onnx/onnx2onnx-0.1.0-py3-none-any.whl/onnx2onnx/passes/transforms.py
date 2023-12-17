"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""
from typing import List

import numpy as np
from onnx import NodeProto, numpy_helper
from onnx.helper import make_node

from onnx2onnx.graph import OnnxGraph

from . import PASSES
from .pattern import SingleNodePattern
from .rewriter import Rewriter
from .utils import make_constant


@PASSES.register(name="split_to_slice")
class SplitToSliceRewriter(Rewriter):
    """Change Split node to Slice node."""

    def __init__(self):
        super().__init__(SingleNodePattern("Split"))

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        node_pb = nodes[0]
        node = node_pb.name
        split = self.get_value(self.get_input_node(node_pb, 1))
        axis = self.get_attribute(node_pb, "axis") or 0
        starts = 0
        for i, (ch, _) in enumerate(zip(split, graph.onnx_successors(node_pb))):
            starts_node = make_constant(
                name=f"{node}/Starts{i}", value=np.array([starts], dtype="int64")
            )
            ends_node = make_constant(
                name=f"{node}/Ends{i}", value=np.array([starts + ch], dtype="int64")
            )
            axes_node = make_constant(
                name=f"{node}/Axes{i}", value=np.array([axis], dtype="int64")
            )
            slice_node = make_node(
                op_type="Slice",
                inputs=[
                    node_pb.input[0],
                    starts_node.output[0],
                    ends_node.output[0],
                    axes_node.output[0],
                ],
                outputs=[node_pb.output[i]],
                name=f"{node}/Slice{i}",
            )
            self += [starts_node, ends_node, axes_node, slice_node]
            starts += ch
        self -= node_pb


@PASSES.register(name="resize_move_size_to_scale")
class ResizeMoveSizeToScaleRewriter(Rewriter):
    """Move `size` input to `scale` input for Resize Op."""

    def __init__(self):
        super().__init__(SingleNodePattern("Resize"))

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        node_pb = nodes[0]
        node = node_pb.name
        _, roi, scales, sizes = self.get_input_nodes(node_pb)
        if sizes is None and scales is None:
            raise ValueError(
                f"Op '{node}' both scales and sizes are empty!"
                " Try fold_constant pass before this."
            )
        if scales is not None:
            return
        input_shape = graph.tensor_shape(node_pb.input[0])
        axes = self.get_attribute(node_pb, "axes") or range(len(input_shape))
        ct_mode = self.get_attribute(node_pb, "coordinate_transformation_mode")
        sizes_val = numpy_helper.to_array(sizes.attribute[0].t)
        if roi is not None and ct_mode == "tf_crop_and_resize":
            roi_val = self.get_value(roi).reshape([2, -1])
            roi_size = []
            for i, j, k in zip(roi_val[0], roi_val[1], sizes_val):
                if i < 0:
                    i += k
                if j < 0:
                    j += k
                assert j >= i >= 0
                roi_size.append(j - i)
            scales_val = [sizes_val[i] / roi_size[i] for i, _ in enumerate(axes)]
        else:
            scales_val = [sizes_val[i] / input_shape[j] for i, j in enumerate(axes)]
        scales = make_constant(
            f"{node}/const/scales", np.array(scales_val, dtype="float32")
        )
        node_pb.input[2] = scales.output[0]
        node_pb.input.pop()  # remove `sizes`
        self += scales
        self -= sizes


@PASSES.register(name="resize_to_nearest_neighbor")
class ResizeToNearestNeighborRewriter(Rewriter):
    """Simplify any resize with integer scales to nearest neighbor interpolate"""

    def __init__(self):
        super().__init__(SingleNodePattern("Resize"))

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        node_pb = nodes[0]
        mode = self.get_attribute(node_pb, "mode")
        if mode != "nearest":
            self.set_attribute(node_pb, "mode", "nearest")
        self._simplify_coordinate_transformation_mode(node_pb)

    def _simplify_coordinate_transformation_mode(self, node_pb):
        self.set_attribute(node_pb, "coordinate_transformation_mode", "asymmetric")
