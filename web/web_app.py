import os
import pandas as pd
from textblob import TextBlob
from flask import Flask


def parse_input(input_data):
    return TextBlob(input_data).words.lower().lemmatize()


def load_data(file_path):
    return pd.read_pickle(file_path)