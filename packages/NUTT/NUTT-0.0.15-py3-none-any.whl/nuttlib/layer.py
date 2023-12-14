"""Layer, a collection of neurons."""

from .mat import Mat
from .neuron import Neuron
from typing import List
import logging



class Layer:
    def __init__(self, inputSize: int, neuronCount: int = None, bias: float = 0.0, neurons: List = None) -> None:
        if neuronCount is None and neurons is None:
            raise ValueError("Need to specify either neuronCount or Neurons to construct a Layer")
        elif neurons is not None:
            if not all(isinstance(neuron, Neuron) for neuron in neurons) and neurons is not None:
                raise TypeError("Neurons must be a list of Neurons")
        else:
            self.neurons = [Neuron(nInputs=inputSize, bias=bias) for _ in range(neuronCount)]
            self.count = neuronCount

    def fwd(self, x: float) -> float:
        outputs = []
        for neuron in self.neurons:
            logging.debug(f"Neuron: {neuron}\nx: {x}\ntype(x): {type(x)}")
            neuron.activate(x)
            outputs.append(neuron.output)
        self.output = sum(outputs)
        return sum(outputs)

    def bwd(self, x: float, eta: float, nextW: float = None, nextError: float = None) -> None:
        for i, neuron in enumerate(self.neurons):
            if nextW is not None and nextError is not None:
                error = float(sum([w * e for w, e in zip(nextW, nextError)]))
            else:
                error = float(neuron.error)
            neuron.update_weights(x, eta, error)