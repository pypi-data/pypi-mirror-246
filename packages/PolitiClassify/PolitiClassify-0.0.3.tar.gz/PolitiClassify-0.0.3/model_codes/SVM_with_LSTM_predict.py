import pandas as pd
from sklearn import svm
import pickle

def SVM_with_LSTM_predict(df_pred,
                          user_variable,
                          model_path):

    """
    SVM_with_BERT_predict takes the predictions from the first step BERT model and makes predictions about each Twitter user's political identity.

    :param df_pred: The dataframe containing the predicted probability of each text. 
    :param model_path: The path for the trained SVM model.
    :param user_variable: The name of the column that contains user ids.

    :return: A dataframe with predicted probabilities for each user. 
    """                                             
    # obtain features from the step 1 predictions.
    ds = df_pred.groupby([user_variable])['pred_proba'].describe()

    ds_total = df_pred.groupby([user_variable])[user_variable].count()
    dsR = df_pred.query("pred_proba > 0.6").groupby([user_variable])[user_variable].count()
    dsD = df_pred.query("pred_proba < 0.4").groupby([user_variable])[user_variable].count()
    dsR = dsR/ds_total
    dsD = dsD/ds_total

    dsC = pd.concat([dsR,dsD], axis=1)
    dsC.columns = ['R','D']
    ds_plus = pd.merge(ds,dsC, on=user_variable)
    ds_plus = ds_plus.fillna(0)

    X = ds_plus[['mean','std','min','max','R','D','25%','50%','75%']].values

    # load the svm model
    svm_model = pickle.load(open(model_path, 'rb'))
    # make predictions
    user_pred_label = svm_model.predict(X)
    user_pred_proba = svm_model.predict_proba(X)
    # form a dataframe
    user_pred = pd.DataFrame(zip(ds_plus.index.values,user_pred_proba, user_pred_label), 
                            columns=[user_variable, 'pred_proba', 'pred_label'])
    return(user_pred)