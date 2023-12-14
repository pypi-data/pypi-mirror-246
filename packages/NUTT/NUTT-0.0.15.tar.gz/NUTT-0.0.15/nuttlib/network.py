"""Network, a collection of layers."""

from .layer import Layer
from .mat import Mat
import logging



class Network:
    def __init__(self):
        self.layers = []

    def add_layer(self, layer: Layer) -> None:
        if not isinstance(layer, Layer):
            raise TypeError("Layer must be a Layer object, duh!")
        else:
            self.layers.append(layer)

    def fwd(self, x: float) -> float:
        logging.debug(f"x: {x} | type(x): {type(x)}")
        output = x
        for layer in self.layers:
            output = layer.fwd(output)
        return output

    def bwd(self, x: float, y: float, eta: float) -> None:
        for l in reversed(range(len(self.layers))):
            layer = self.layers[l]
            if l == len(self.layers) - 1: # output layer
                errors = [layer.output - y for neuron in layer.neurons]
            else:
                nextLayer = self.layers[l + 1]
                nextW = [neuron.weights for neuron in nextLayer.neurons if neuron.weights is not None]
                nextError = [neuron.error for neuron in nextLayer.neurons if neuron.error is not None]
                layer.bwd(x, eta, nextW, nextError)