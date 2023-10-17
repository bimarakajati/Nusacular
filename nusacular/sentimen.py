from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import PredefinedSplit
from scipy.sparse import vstack
from nltk import word_tokenize
import numpy as np
import pandas as pd
import streamlit as st

def load_data(filedir):
    df = pd.read_csv(filedir)
    data = list(df['text'])
    data = [" ".join(word_tokenize(sent)) for sent in data]
    return (data, list(df['label']))

def hyperparam_tuning(xtrain, ytrain, xvalid, yvalid, classifier, param_grid):
    # combine train and valid
    x = vstack([xtrain, xvalid])
    y = ytrain + yvalid

    # create predefined split
    # -1 for all training and 0 for all validation
    ps = PredefinedSplit([-1] * len(ytrain) + [0] * len(yvalid))
    clf = GridSearchCV(classifier, param_grid, cv = ps)
    clf = clf.fit(x, y)
    return clf

def train_and_test(lang, directory="./datasets/nusax/sentiment/", feature="BoW", classifier="nb"):
    xtrain, ytrain = load_data(directory + lang +"/train.csv")
    xvalid, yvalid = load_data(directory + lang + "/valid.csv")
    xtest, ytest = load_data(directory + lang + "/test.csv")
    
    # train feature on train data
    if feature == "bow":
        vectorizer = CountVectorizer()
    elif feature == "tfidf":
        vectorizer = TfidfVectorizer()
    else:
        raise Exception('Vectorizer unknown. Use "BoW" or "tfidf"')
    vectorizer.fit(xtrain)

    # transform
    xtrain = vectorizer.transform(xtrain)
    xvalid = vectorizer.transform(xvalid)
    xtest = vectorizer.transform(xtest)
    
    # all classifiers
    classifier_model = {"nb" : MultinomialNB(),
                        "svm": SVC(),
                        "lr" : LogisticRegression(),
                       }
    # all params for grid-search
    param_grids = {"nb" : {"alpha": np.linspace(0.001,1,50)},
                   "svm": {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['rbf', 'linear']},
                   "lr" : {'C': np.linspace(0.001,10,100)},
                  }
    
    clf = hyperparam_tuning(xtrain, ytrain, xvalid, yvalid,
                            classifier=classifier_model[classifier],
                            param_grid=param_grids[classifier])

    pred = clf.predict(xtest.toarray())
    f1score = f1_score(ytest,pred, average='macro')
    
    return f1score, clf, vectorizer

def sentimen():
    st.title("Sentimen Bahasa Daerah")

    language = st.selectbox(
    'Pilih bahasa daerah:',
    ('indonesian', 'javanese', 'sundanese'))

    input_sentiment = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button ("Deteksi")

    if prediksi:
        f1, clf, vectorizer = train_and_test(language, feature="bow")
        input_sentiment = " ".join(word_tokenize(input_sentiment))
        sent = clf.predict(vectorizer.transform([input_sentiment]).toarray())

        print('Selected language:', language)
        st.write('Selected language:', language)
        print("Sentiment on the input text is:", sent[0])
        st.write("Sentiment on the input text is:", sent[0])
        print("Confidence Score:", f1)
        st.write("Confidence Score:", f1)