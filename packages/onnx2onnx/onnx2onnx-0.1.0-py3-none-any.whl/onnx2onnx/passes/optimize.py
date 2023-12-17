"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

from contextlib import suppress

from . import PASSES, OnnxGraph

with suppress(ImportError):
    import onnxoptimizer

    @PASSES.register()
    def onnx_optimizer(graph: OnnxGraph):
        """Fuse op and remove isolated nodes."""
        return OnnxGraph(onnxoptimizer.optimize(graph.model))
