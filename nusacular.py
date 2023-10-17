import g4f
import pickle
import streamlit as st
from local_db import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import f1_score,accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import PredefinedSplit
from scipy.sparse import vstack
from nltk import word_tokenize
import numpy as np
import pandas as pd

with open('model/lrmodel.pckl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

def deteksi():
    st.title("Deteksi Bahasa Daerah")

    input_kata = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button ("Deteksi")

    if prediksi or input_kata != "":
        predicted_language = loaded_model.predict([input_kata])
        print("Predicted language:", predicted_language)
        st.write("Predicted Language:", predicted_language[0])

        class_probabilities = loaded_model.predict_proba([input_kata])
        print("Class probabilities:", class_probabilities)

        confidence_score = max(class_probabilities[0])
        st.write("Confidence Score:", confidence_score)

        with st.expander("Lihat detail"):
            bahasa = ['Bataknese', 'Indonesian', 'Javanese', 'Sundanese']
            for i in range(len(bahasa)):
                st.write(f'{bahasa[i]}:')
                st.progress(class_probabilities[0][i])

def chatbot():
    st.title("Nusacular Bot")

    # Load chat history from the database
    messages = retrieve_messages()
    for message in messages :
        with st.chat_message(message[0]):  # message[0] corresponds to the 'role'
            st.markdown(message[1])  # message[1] corresponds to the 'content'

    # React to user input
    if prompt := st.chat_input("Mau tanya apa?"):
        # Display user message in chat message container
        prompt = prompt.strip()
        st.chat_message("user").markdown(prompt)
        print('Prompt:', prompt)

        # Add user message to the database
        insert_message("user", prompt)

        # Define roles for messages
        role = ["system", "user", "assistant"]

        while True:
            response = g4f.ChatCompletion.create(
                        model=g4f.models.default,
                        provider=g4f.Provider.You,
                        messages=[{"role": role[1], "content": prompt}]
                    )
            if response == '':
                print("Empty response, retrying...")
                continue
            else:
                print('Response:', response, '\n')
                break

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to the database
        insert_message("assistant", response)

    # Button to clear the database (conditionally displayed)
    if messages:
        if st.button("Clear Database"):
            clear_database()
            st.experimental_rerun() # Reload the Streamlit app

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

        st.write('Selected language:', language)
        st.write("Sentiment on the input text is:", sent[0])
        st.write("Confidence Score:", f1)

def about_us():
    st.title("About Us")

    # About Us
    st.markdown("""
    Dibuat pada 4 Oktober 2023, Nusacular (Nusantara Vernacular) adalah sebuah aplikasi yang dapat memprediksi bahasa daerah dan juga dapat digunakan sebagai chatbot.

    Bahasa daerah yang dapat diprediksi oleh aplikasi ini adalah:
    - Bahasa Jawa
    - Bahasa Sunda
    - Bahasa Batak Toba

    Aplikasi ini dibuat oleh:
    |             Name            |      NIM       |
    | --------------------------- | -------------- |
    | Bima Rakajati               | A11.2020.13088 |
    | Enrico Zada                 | A11.2020.12972 |
    | Rosalia Natal Silalahi      | A11.2020.13084 |
    | Devi Kartika Sari           | A11.2020.12518 |
    """)