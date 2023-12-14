import pandas as pd
import numpy as np
import pickle
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from model_codes.Attention import AttentionWithContext
from processing.text_preprocessing import preprocess

def LSTM_predict(model_path,
                 tokenizer_path,
                 data_path,
                 text_variable,
                 user_variable,
                 maxlen,
                 batch_size):
    """
    LSTM_predict takes texts from a csv file and makes predictions about the political identity of those texts.

    :param model_path: The path for the pretrained LSTM model.
    :param tokenizer_path: The path for the trained tokenizer.
    :param data_path: The path for the input dataset.
    :param text_variable: The name of the column that contains texts. 
    :param user_variable: The name of the column that contains user ids.
    :param maxlen: The max number of tokens of the input texts. 
    :param batch_size: Batch size.

    :return: A dataframe with predicted probabilities for each tweet/text. 
    """ 
    # load the trained LSTM model
    model = load_model(model_path,
                       custom_objects={'AttentionWithContext': AttentionWithContext})

    # load the trained tokenizer
    tokenizer = pickle.load(open(tokenizer_path, "rb"))

    # load the data
    df = pd.read_csv(data_path)

    # clean data
    df[text_variable] = df[text_variable].apply(lambda x: preprocess(x, remove_stop_words = False))
    df = df[df[text_variable].notna()]

    # pad data
    X = pad_sequences(tokenizer.texts_to_sequences(df[text_variable]), maxlen=maxlen)

    # make predictions
    y_proba = model.predict(X, verbose=1, batch_size=batch_size)

    # make predictions a dataframe
    y_proba = [item for elem in y_proba for item in elem]
    df_pred = pd.DataFrame(zip(df[user_variable].values, y_proba), columns=[user_variable, 'pred_proba'])
    
    return(df_pred)