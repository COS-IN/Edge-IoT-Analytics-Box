import logging

import torch
import torch.nn.functional as F

import pandas as pd 
import numpy as np 
import pickle 
import base64

logger = logging.getLogger(__name__)

import os
import re
import string
import unicodedata
from abc import ABC

from ts.torch_handler.base_handler import BaseHandler

#from torch.profiler import ProfilerActivity
#from .base_handler import BaseHandler
#from ..utils.util import CLEANUP_REGEX
#from .contractions import CONTRACTION_MAP

def to(self, x):
    return self 

class DfHandler(BaseHandler, ABC):
    """
    Base class for all text based default handler.
    Contains various text based utility methods
    """

    def __init__(self):
        super().__init__()

    def df_to_bytes(self, df): 
        pickled = pickle.dumps(df)
        pickled_b64 = base64.b64encode(pickled)
        return pickled_b64
    def str_to_bytes(self, data):
        return data.encode()
    def bytes_to_df(self, data): 
        ss_df = pickle.loads(base64.b64decode(data))
        return ss_df 

    def preprocess(self, data):
        rawbytes = data[0]['body']
        df = self.bytes_to_df( rawbytes )
        setattr(df,'to', to.__get__( df ))
        return df 

    def postprocess(self, data):
        data = self.df_to_bytes( data )
        return [data]

