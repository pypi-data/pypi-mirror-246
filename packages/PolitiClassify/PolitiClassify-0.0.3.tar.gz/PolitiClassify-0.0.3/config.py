LSTM_MODEL_PATH = "trained_models/cong_politician_2020-3-12-2021-5-28_balanced_pre-w2v.h5"
LSTM_TOKENIZER_PATH = "trained_models/cong_politician_2020-3-12-2021-5-28_balanced_pre-w2v_tokenizer.pkl"
SEQUENCE_LENGTH = 50
BATCH_SIZE = 512

SVM_LSTM_MODEL_PATH = "trained_models/step2_model_svm_200tweets_lstm.sav"
SVM_BERT_MODEL_PATH = "trained_models/step2_model_svm_200tweets_bert.sav"

DATA_PATH = "data/example_tweets.csv"
TWEET_PRED_DATA_PATH = "pred_data/example_tweets_pred.csv"
USER_PRED_DATA_PATH = "pred_data/example_tweets_user_pred.csv"

TEXT_COLUMN_NAME = "text"
USER_COLUMN_NAME = "user_id"