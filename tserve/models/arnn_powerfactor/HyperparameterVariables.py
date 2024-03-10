class HyperparameterVariables:

    def __init__(self):
        self.hidden_size = 16
        self.rnn_kwargs = {
            "n_rnn_layers": 1,
            "rnn_layer": "RNN",
            "rnn_kwargs": {},
            "dropout": 0.0,
        }
        self.mapper_kwargs = {
            "temporal_mapper": "last",
            "temporal_mapper_kwargs": {},
        }
        self.kwargs = {}