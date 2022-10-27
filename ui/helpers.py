import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.probability import FreqDist
nltk.download('punkt')
nltk.download("stopwords")

def senti_helper(df):
    conditions = [
        (df['Sentiment score'] <0),
        (df['Sentiment score'] == 0),
        (df['Sentiment score'] > 0)
    ]

    # create a list of the values we want to assign for each condition
    values = ['Negative', 'Neutral', 'Positive']

    df['Sentiment'] = np.select(conditions, values)

    total_rows = df.shape[0]
    categorized_rows = total_rows
    uncategorized_rows = 0

    positive_rows = df[df['Sentiment'] == 'Positive'].shape[0]
    negative_rows = df[df['Sentiment'] == 'Negative'].shape[0]
    neutral_rows = df[df['Sentiment'] == 'Neutral'].shape[0]

    # Word Cloud Code
    df_eng_pos = df[df['Sentiment']=='Positive']
    df_eng_neg = df[df['Sentiment']=='Negative']
    df_eng_neu = df[df['Sentiment']=='Neutral']

    context = {
        "total_rows": df.shape[0],
        "categorized_rows": df.shape[0],
        "uncategorized_rows": 0,

        "positive_rows": df[df['Sentiment'] == 'Positive'].shape[0],
        "negative_rows": df[df['Sentiment'] == 'Negative'].shape[0],
        "neutral_rows": df[df['Sentiment'] == 'Neutral'].shape[0],

        "positive_percent": round((positive_rows / total_rows) * 100, 1),
        "negative_percent": round((negative_rows / total_rows) * 100, 1),
        "neutral_percent": round((neutral_rows / total_rows) * 100, 1),

        # WORD CLOUD
        "data_pos": word_counter(df_eng_pos, "Positive"),
        "data_neg": word_counter(df_eng_neg, "Negative"),
        "data_neu": word_counter(df_eng_neu, "Neutral"),

    }
    print(context["data_pos"])
    return context


def word_counter(df, sentiment):
    text = ''
    temp_list = []
    words_no_punc = []
    clean_words = []

    for i in df['Text'].tolist():
        text = text + '. ' + i

    words = word_tokenize(text)
    words_no_punc = []
    for word in words:
        if word.isalpha():
            words_no_punc.append(word.lower())
    stopwords_list = stopwords.words("english")
    for word in words_no_punc:
        if word not in stopwords_list:
            clean_words.append(word)

    fdist = FreqDist(clean_words)

    temp_list.append(fdist.most_common(20))

    temp_df = pd.DataFrame(temp_list[0], columns =['Word', 'Freq'])
    temp_df["Sentiment"] = sentiment
    temp_df.columns = ['x', 'value', 'category']
    data2 = temp_df.to_dict('records')
    return data2


def emotion_helper(df):
    total_rows = df.shape[0]
    uncategorized_rows = df[df['traits'] == 'NA'].shape[0]
    categorized_rows = total_rows - uncategorized_rows
    context = {
        "total_rows": total_rows,
        "categorized_rows": categorized_rows,
        "uncategorized_rows": uncategorized_rows,
    }
    return context