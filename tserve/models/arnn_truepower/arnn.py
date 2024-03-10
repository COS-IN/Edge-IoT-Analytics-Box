import pandas as pd
import numpy as np 
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data



def merge_dicts(a, b, overwrite=True):
    if not (isinstance(a, dict) or isinstance(b, dict)):
        raise ValueError("Expected two dictionaries")
    if overwrite:
        return {**a, **b}
    c = copy_dict(a)
    for key, value in b.items():
        if not key in a:
            c[key] = value
    return c


def make_msg_block(msg, block_char="#"):
    msg_line = 3*block_char + " " + msg + " " + 3*block_char
    msg_line_len = len(msg_line)
    msg_block = "%s\n%s\n%s" % (
        msg_line_len*block_char,
        msg_line,
        msg_line_len*block_char
    )
    return msg_block


class RNNCell(torch.nn.Module):

    debug = 0

    def __init__(self, in_size, out_size, n_rnn_layers=1, rnn_layer="LSTM", rnn_kwargs={}, dropout=0.0):
        super(RNNCell, self).__init__()
        print("RNNCell :", in_size, out_size, n_rnn_layers, rnn_layer, rnn_kwargs, dropout)
        self.supported_layers = ["RNN", "GRU", "LSTM"]
        assert rnn_layer in self.supported_layers, "Layer \"%s\" not supported" % (rnn_layer)
        # Instantiate model layers
        def init_cell(in_size, out_size, rnn_layer, **rnn_kwargs):
            return {
                "RNN": torch.nn.RNNCell,
                "GRU": torch.nn.GRUCell,
                "LSTM": torch.nn.LSTMCell,
            }[rnn_layer](in_size, out_size, **rnn_kwargs)
        self.cell_forward = getattr(self, "%s_forward" % (rnn_layer))
        self.cells = [init_cell(in_size, out_size, rnn_layer, **rnn_kwargs)]
        self.cells += [init_cell(out_size, out_size, rnn_layer, **rnn_kwargs) for i in range(1, n_rnn_layers)]
        self.drops = [torch.nn.Dropout(dropout) for i in range(n_rnn_layers)]
        self.cells = torch.nn.ModuleList(self.cells)
        self.drops = torch.nn.ModuleList(self.drops)
        # Save all vars
        self.in_size = in_size
        self.out_size = out_size
        self.n_layers = n_rnn_layers
        self.rnn_layer = rnn_layer
        self.rnn_kwargs = rnn_kwargs
        self.dropout = dropout

    def forward(self, **inputs):
        for i in range(self.n_layers):
            self.cells[i].debug = self.debug
        x, xs, xt = inputs["x"], inputs.get("xs", None), inputs.get("xt", None)
        temporal_dim = inputs.get("temporal_dim", -2)
        init_state, n_steps = inputs.get("init_state", None), inputs.get("n_steps", x.shape[temporal_dim])
        if self.debug:
            print(make_msg_block("RNN Forward"))
        if self.debug:
            print("x =", x.shape)
            if self.debug > 1:
                print(x)
            if not xs is None:
                print("xs =", xs.shape)
            if not xt is None:
                print("xt =", xt.shape)
        autoregress = False
        if n_steps != x.shape[temporal_dim]: # encode autoregressively
            assert x.shape[temporal_dim] == 1, "Encoding a sequence from %d to %d time-steps is ambiguous" % (
                x.shape[temporal_dim], n_steps
            )
            autoregress = True
        outputs = {}
        get_idx_fn = self.index_select
        A = [None] * n_steps
        a = get_idx_fn(x, 0, temporal_dim)
        xt_t = None
        for i in range(self.n_layers):
            prev_state = init_state
            for t in range(n_steps):
                x_t = (a if autoregress else get_idx_fn(x, t, temporal_dim))
                if not xt is None:
                    xt_t = get_idx_fn(xt, t, temporal_dim)
                inputs_t = merge_dicts(inputs, {"x": x_t, "xt": xt_t, "prev_state": prev_state})
                a, prev_state = self.cell_forward(self.cells[i], **inputs_t)
                if self.debug:
                    print("Step-%d Embedding =" % (t+1), a.shape)
                A[t] = a
            a = torch.stack(A, temporal_dim)
            a = self.drops[i](a)
            x = a
        outputs["yhat"] = a
        outputs["final_state"] = prev_state
        return outputs

    def RNN_forward(self, cell, **inputs):
        hidden_state = cell(inputs["x"], inputs["prev_state"])
        return hidden_state, hidden_state

    def GRU_forward(self, cell, **inputs):
        hidden_state = cell(inputs["x"], inputs["prev_state"])
        return hidden_state, hidden_state

    def LSTM_forward(self, cell, **inputs):
        hidden_state, cell_state = cell(inputs["x"], inputs["prev_state"])
        return hidden_state, (hidden_state, cell_state)

    def index_select(self, x, idx, dim):
        return torch.index_select(x, dim, torch.tensor(idx, device=x.device)).squeeze(dim)

    def reset_parameters(self):
        for cell in self.cells:
            if hasattr(cell, "reset_parameters"):
                cell.reset_parameters()



class TemporalMapper(torch.nn.Module):

    debug = 0

    def __init__(self, in_size, out_size, temporal_mapper="last", temporal_mapper_kwargs={}):
        super(TemporalMapper, self).__init__()
        # Setup
        self.supported_methods = ["last", "last_n"]
        assert temporal_mapper in self.supported_methods, "Temporal mapping method \"%s\" not supported" % (method)
        self.method_init_map = {}
        for method in self.supported_methods:
            self.method_init_map[method] = getattr(self, "%s_init" % (method))
        self.method_mapper_map = {}
        for method in self.supported_methods:
            self.method_mapper_map[method] = getattr(self, "%s_mapper" % (method))
        # Instantiate method
        self.method_init_map[temporal_mapper](in_size, out_size, temporal_mapper_kwargs)
        self.mapper = self.method_mapper_map[temporal_mapper]

    def last_init(self, in_size, out_size, kwargs={}):
        pass

    def last_n_init(self, in_size, out_size, kwargs={}):
        pass

    def forward(self, **inputs):
        if self.debug:
            print(make_msg_block("TemporalMapper Forward"))
        return self.mapper(**inputs)

    def last_mapper(self, **inputs):
        if self.debug:
            print(make_msg_block("last_mapper() forward"))
        x, temporal_dim = inputs["x"], inputs.get("temporal_dim", -2)
        if self.debug:
            print("x =", x.shape)
            print("temporal_dim =", temporal_dim)
        return {
            "yhat": torch.index_select(x, temporal_dim, torch.tensor(x.shape[temporal_dim]-1, device=x.device))
        }

    def last_n_mapper(self, **inputs):
        x, n_temporal_out, temporal_dim = inputs["x"], inputs["n_temporal_out"], inputs.get("temporal_dim", -2)
        if self.debug:
            print("x =", x.shape)
            print("temporal_dim =", temporal_dim)
        t = x.shape[temporal_dim]
        return {
            "yhat": torch.index_select(
                x, temporal_dim, torch.tensor(range(t-n_temporal_out, t), device=x.device)
            )
        }

    def reset_parameters(self):
        pass



class A_RNN(torch.nn.Module):

    debug = 0

    def __init__(
        self,
        in_size,
        out_size,
        n_temporal_in, 
        hidden_size=16,
        rnn_kwargs={},
        mapper_kwargs={}, 
        kwargs={}, 
    ):
        super(A_RNN, self).__init__()
        # Instantiate model layers
        self.attn = torch.nn.Parameter(torch.ones((n_temporal_in, in_size)))
        self.attn_act = torch.nn.Softmax(-1)
        self.enc = RNNCell(in_size, hidden_size, **rnn_kwargs)
        self.map = TemporalMapper(hidden_size, hidden_size, **mapper_kwargs)
        self.dec = RNNCell(hidden_size, hidden_size, **rnn_kwargs)
        self.out_proj = torch.nn.Linear(hidden_size, out_size)
        # Save all vars
        self.in_size = in_size
        self.out_size = out_size
        self.hidden_size = hidden_size
        self.kwargs = kwargs
        # Pairs (name, partition) that identify this model
        self.id_pairs = [
            ["hidden_size", None],
            ["rnn_kwargs", None],
            ["mapper_kwargs", None],
            ["kwargs", None],
        ]
        

    def forward(self, **inputs):
#        self.debug = 1
        self.enc.debug = self.debug
        self.map.debug = self.debug
        self.dec.debug = self.debug
        x, n_temporal_out = inputs["x"], inputs["n_temporal_out"]
        n_samples, n_temporal_in, n_spatial, in_size = x.shape # shape=(N, T, |V|, F)
        if self.debug:
            print("x =", x.shape)
        #####################
        ### Start forward ###
        #####################
        a = torch.reshape(torch.transpose(x, 1, 2), (-1, n_temporal_in, in_size)) # shape=(N*|V|, T, F)
        if self.debug:
            print("x reshaped =", a.shape)
        # Attention layer forward
        attn_w = self.attn_act(self.attn[None,:,:])
        a = a * attn_w
        if self.debug:
            print("attn_w =", attn_w.shape)
        if self.debug:
            print("attended x =", a.shape)
        # Encoding layer forward
        self.enc.debug = self.debug
        a = self.enc(x=a)["yhat"] # shape=(N*|V|, T, H)
        if self.debug:
            print("Encoding =", a.shape)
        a = self.map(x=a, n_temporal_out=n_temporal_out, temporal_dim=-2)["yhat"] # shape=(N*|V|, ?, H)
        if self.debug:
            print("Encoding Remapped =", a.shape)
        # Decoding layer forward
        a = self.dec(x=a, n_steps=n_temporal_out)["yhat"] # shape=(N*|V|, T', H)
        if self.debug:
            print("Decoding =", a.shape)
        a = torch.reshape(a, (n_samples, n_spatial, n_temporal_out, self.hidden_size)) # shape=(N, |V|, T', H)
        a = torch.transpose(a, 1, 2) # shape=(N, T', |V|, H)
        if self.debug:
            print("Decoding Reshaped =", a.shape)
        # Output layer forward
        a = self.out_proj(a) # shape=(N, T', |V|, F')
        if self.debug:
            print("Output =", a.shape)
        if self.debug:
            sys.exit(1)
        outputs = {"yhat": a}
        return outputs

    def reset_parameters(self):
        self.enc.reset_parameters()
        self.map.reset_parameters()
        self.dec.reset_parameters()
        self.out_proj.reset_parameters()

    def load(self, path):
        checkpoint = torch.load(path)
        self.load_state_dict(checkpoint["model_state_dict"])
        return self

