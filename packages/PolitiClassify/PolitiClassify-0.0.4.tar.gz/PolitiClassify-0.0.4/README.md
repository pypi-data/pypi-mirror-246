# PolitiClassify
A Python package for classifying Twitter users' political orientation using two-step deep learning models.

In the first step, the model classifies the political orientation of individual tweets. In the second step, the model classifies the political orientation of individual users based on their multiple tweets and output the label (0 for liberal/democratic; 1 for conservative/republican) for each user. The accuracy of using this two-step method to classify non-politician Twitter users' political orientation based on their 200 tweets is around 96.33%.

Two trained models can be chosen for the first step of the method: LSTM and BERT. The trained BERT model is the default and will be automatically downloaded. The trained LSTM model needs to be downloaded from [here](https://drive.google.com/file/d/1uqw9rjmDyDtJ-Z827O85SiE3lY00l1ed/view?usp=drive_link). After downloading the trained LSTM model, you can store the model in the "trained_models" folder, or you can specify the path of the model in the function argument "step1_model_path.

To use this Python package, you can install it by using:
```
pip install PolitiClassify
```
Then you can import the functions from the package and use it as follows:
```Python
from PolitiClassify import two_step_BERT_predict
user_pred = two_step_BERT_predict(
    data_path="data/example_tweets.csv",
    text_variable="text",
    user_variable="user_id"
    )
```
If you prefer to use the trained LSTM model as the first-step model, you can do the following:

```Python
from PolitiClassify import two_step_LSTM_predict
user_pred = two_step_LSTM_predict(
    step1_model_path="trained_models/cong_politician_2020-3-12-2021-5-28_balanced_pre-w2v.h5",
    data_path="data/example_tweets.csv",
    text_variable="text",
    user_variable="user_id"
    )
```

Alternatively, you can download it from GitHub, store your dataset in the "data" folder, change the name of the dataset in the `config.py` file, and then run `PolitiClassify.py` in your terminal.

Please cite this paper:

@article{HuL,\
&nbsp;&nbsp;&nbsp;&nbsp;    author = {Lingshu Hu},\
&nbsp;&nbsp;&nbsp;&nbsp;    title = {A Two-Step Method for Classifying Political Partisanship Using Deep Learning Models},\
&nbsp;&nbsp;&nbsp;&nbsp;    journal = {Social Science Computer Review},\
&nbsp;&nbsp;&nbsp;&nbsp;    DOI = {10.1177/08944393231219685},\
&nbsp;&nbsp;&nbsp;&nbsp;    year = {2023}\
}

The training dataset can be obtained from [kaggle](https://www.kaggle.com/datasets/lingshuhu/political-partisanship-tweets).
