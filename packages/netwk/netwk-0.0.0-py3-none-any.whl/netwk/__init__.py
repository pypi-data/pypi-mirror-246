import numpy as np
import pickle
from .activations import *

class Module:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __str__(self, *args, **kwargs):
        return f"{self.name}({', '.join(map(str, self.args))}, {', '.join(f'{k}={v}' for k, v in self.kwargs.items())})"

    def __repr__(self, *args, **kwargs):
        return self.__str__()

    def __call__(self, name, *args, **kwargs):
        return self.__class__(name, *args, **kwargs)

    def forward(self, x, *args, **kwargs):
        return x

    def backward(self, x, y, output, *args, **kwargs):
        return np.zeros_like(x)

    def save(self, path, *args, **kwargs):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

        return self

    @staticmethod
    def load(path, *args, **kwargs):
        with open(path, 'rb') as f:
            return pickle.load(f)

class Network(Module):
    def __init__(self, input_layer, hidden_layers, output_layer, *args, **kwargs):
        super().__init__("Network", input_layer, hidden_layers, output_layer)
        self.input = input_layer
        self.input_layer = input_layer.size
        self.hidden_layers = hidden_layers
        self.hidden_sizes = [layer.size for layer in hidden_layers]
        self.output = output_layer
        self.output_layer = output_layer.size

        self.num_layers = len(hidden_layers)

        self.weights = [None] * (self.num_layers + 1)

        self.weights[0] = np.random.randn(self.input_layer, self.hidden_sizes[0])

        for i in range(1, self.num_layers):
            self.weights[i] = np.random.randn(self.hidden_sizes[i - 1], self.hidden_sizes[i])

        self.weights[self.num_layers] = np.random.randn(self.hidden_sizes[-1], self.output_layer)

    def sigmoid(self, x, *args, **kwargs):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x, *args, **kwargs):
        return x * (1 - x)

    def forward(self, x, *args, **kwargs):
        self.z = [None] * (self.num_layers + 1)
        self.a = [None] * (self.num_layers + 2)

        self.a[0] = x

        for i in range(1, self.num_layers + 1):
            self.z[i] = np.dot(self.a[i - 1], self.weights[i - 1])
            self.a[i] = self.hidden_layers[i - 1].forward(self.z[i])

        self.z[self.num_layers] = np.dot(self.a[self.num_layers], self.weights[self.num_layers])
        output = self.sigmoid(self.z[self.num_layers])

        return output

    def backward(self, x, y, output, *args, **kwargs):
        self.output_error = y - output
        self.output_delta = self.output_error * self.sigmoid_derivative(output)

        self.errors = [None] * (self.num_layers + 1)
        self.deltas = [None] * (self.num_layers + 1)

        self.errors[self.num_layers] = self.output_delta
        self.deltas[self.num_layers] = self.output_delta

        for i in range(self.num_layers, 0, -1):
            self.errors[i - 1] = self.deltas[i].dot(self.weights[i].T)
            self.deltas[i - 1] = self.errors[i - 1] * self.hidden_layers[i - 1].backward(self.a[i])

        for i in range(self.num_layers + 1):
            self.weights[i] += self.a[i].T.dot(self.deltas[i])

    def train(self, x, y, epoch, *args, verbose=True, **kwargs):
        for i in range(epoch):
            output = self.forward(x)
            self.backward(x, y, output)
            if verbose==1 or verbose is True:
                if i % (epoch // 10) == 0:
                    print(f"Epoch: {i}, Error: {np.mean(np.abs(y - output))}")

    def predict(self, x, *args, **kwargs):
        return self.forward(x)

    def __str__(self, *args, **kwargs):
        len_hidden = len(self.hidden_sizes)
        hidden_layer = "".join(
            f"\n        {i+1} {str(self.hidden_layers[i])}" for i in range(len_hidden)
        )
        input_layer = f"1 {str(self.input)}"
        output_layer = f"1 {str(self.output)}"

        return f'Network(\n    Input Layer:\n        {input_layer}\n\n    Hidden Layers:        {hidden_layer}\n\n    Output Layer:\n        {output_layer})'


class Input(Module):
    def __init__(self, size=2, *args, **kwargs):
        super().__init__("Input", size)
        self.size = size

    def __str__(self):
        return f"Input(size: {self.size})"

class Hidden(Module):
    def __init__(self, size=2, activation=Sigmoid, *args, **kwargs):
        super().__init__("Hidden", size, activation)
        self.size = size
        self.activation = activation()

    def forward(self, x, *args, **kwargs):
        return self.activation.forward(x)

    def backward(self, x, *args, **kwargs):
        return self.activation.backward(x)

    def __str__(self, *args, **kwargs):
        return f"Hidden(size: {self.size})"

class Output(Module):
    def __init__(self, size=1, *args, **kwargs):
        super().__init__("Output", size)
        self.size = size

    def __str__(self, *args, **kwargs):
        return f"Output(size: {self.size})"