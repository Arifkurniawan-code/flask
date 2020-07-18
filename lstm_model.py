import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.layers import Embedding,Dense,LSTM,SpatialDropout1D
import tensorflow
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from numpy import asarray
from numpy import zeros
import tensorflow as tf
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import codecs
from nltk.tokenize import word_tokenize
import gensim.models as Word2vec

PROCESSED_DATA_PATH = 'data/hasil'
train_data = pd.read_csv('{}/clear_train.csv'.format(PROCESSED_DATA_PATH))
train_data = train_data[['hasil_normalisasi', 'Label']]

class LSTM_model:

    def __init__(self,filepath=PROCESSED_DATA_PATH):
        self.max_fatures = 5000
        self.batch_size = 128
        # self.build_model()
        return print('Train data shape :', train_data.shape)

    def describe_model(self):
        bullying = 0
        netral = 0
        nonbull = 0
        irrelevant = 0
        for label in train_data['Label']:
            if label == 0:
                bullying += 1
            elif label == 1:
                irrelevant += 1
            elif label == 2:
                netral += 1
            else:
                nonbull += 1

        print("Total komentar cyberbullying adalah " + str(bullying) + ", atau",
              '{0:.2%}'.format(bullying / len(train_data['Label'])))
        print("Total komentar Non cyberbullying adalah " + str(irrelevant) + ", atau ",
              '{0:.2%}'.format(irrelevant / len(train_data['Label'])))
        print("Total komentar Netral adalah " + str(netral) + ", atau ",
              '{0:.2%}'.format(netral / len(train_data['Label'])))
        print("Total komentar Non cyberbullying adalah " + str(nonbull) + ", atau ",
              '{0:.2%}'.format(nonbull / len(train_data['Label'])))
        missing_train = train_data.isnull().sum()
        print(missing_train)
        # n_words = [len(komen) for komen in train_data.hasil_normalisasi]
        # n_words = pd.Series(n_words)
        # n_words.describe()
        # print(train_data['hasil_normalisasi'].describe())

    def tokenize_data(self):
        self.tokenizer = Tokenizer(num_words=self.max_fatures, split=' ')
        self.tokenizer.fit_on_texts(train_data['hasil_normalisasi'].values)
        self.X = self.tokenizer.texts_to_sequences(train_data['hasil_normalisasi'].values)
        print(self.X)
        self.X = pad_sequences(self.X)
        # print(X[:2])
        self.Y = pd.get_dummies(train_data['Label']).values
        print('Nilai Y adalah ', self.Y)
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.20, random_state=42)
        print(self.X_train.shape,self.Y_train.shape)
        print(self.X_test.shape, self.Y_test.shape)
        with open('data/tokenizer.pickle', 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.vocab_size = len(self.tokenizer.word_index) + 1

    def TFIDF(self):
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(train_data['hasil_normalisasi'].values)
        feature_names = vectorizer.get_feature_names()
        print(vectorizer.get_feature_names())
        print(X.shape)
        doc = 0
        feature_index = X[doc, :].nonzero()[1]
        tfidf_score = zip(feature_index, [X[doc, x] for x in feature_index])
        for w, s in [(feature_names[i], s) for (i, s) in tfidf_score]:
            print(w, s)
        df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
        print(df)
        df.to_csv('model/TFIDF.csv')

    def word2vec(self):
        with codecs.open('clear_traincoba.csv', 'r')as f:
            for line in f:
                tweet = f.readlines()
                tokenized_sent = [word_tokenize(i) for i in tweet]
                for i in tokenized_sent:
                    print(i)
        model = Word2vec.Word2Vec(tokenized_sent, min_count=1, size=200)
        print(model)
        model.wv.save_word2vec_format('model/model_word2vecWindow.txt', binary=False)
        word = list(model.wv.vocab)

    def make_model(self):
        embeddings_index = dict()
        # f = open('mymodel/idwiki_word2vec_200.model',encoding='utf-8')
        f = open('model/model_word2vec.txt')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        f.close()
        print('Loaded %s word vectors.' % len(embeddings_index))

        # create a weight matrix for words in training docs
        embedding_matrix = zeros((self.vocab_size, 200))
        for word, i in self.tokenizer.word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

        print(embedding_matrix[21])
        embed_dim = 200
        lstm_out = 196
        model = tensorflow.keras.Sequential()
        model.add(Embedding(self.vocab_size, embed_dim,weights=[embedding_matrix],input_length=self.X.shape[1]))
        model.add(SpatialDropout1D(0.4))
        model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
        # model.add(LSTM(lstm_out,activation='tanh'))
        model.add(Dense(4, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        print(model.summary())
        history=model.fit(self.X_train, self.Y_train, epochs=20, batch_size=self.batch_size, validation_data=(self.X_test, self.Y_test), verbose=1)
        model.save('model/My_model.h5')
        # hist_df=pd.DataFrame(self.history.history)
        # with open('model/history.json','w')as file:
        #     json.dump(history.history,file)
        np.save('model/history_model.npy',history.history)

    def load_model(self):
        self.model = load_model('model/My_model.h5')
        Y_pred = self.model.predict_classes(self.X_test, batch_size=self.batch_size)
        df_test = pd.DataFrame({'true': self.Y_test.tolist(), 'pred': Y_pred})
        df_test['true'] = df_test['true'].apply(lambda x: np.argmax(x))
        print("confusion matrix")
        print(confusion_matrix(df_test.true, df_test.pred))
        print(classification_report(df_test.true, df_test.pred))

    def show_plot(self):
        # with open('model/history.json','r') as f:
        #     history_json=json.loads(f.read())
        history=np.load('model/history_model.npy',allow_pickle='TRUE').item()
        plt.figure(figsize=(12, 12))
        plt.plot(history['loss'])
        plt.plot(history['val_loss'])
        plt.title('Loss')
        plt.legend(['train', 'val'], loc='upper left')
        # plt.show()
        plt.savefig('images/plot/loss.png')

        plt.figure(figsize=(12, 12))
        plt.plot(history['accuracy'])
        plt.plot(history['val_accuracy'])
        plt.title('Accuracy')
        plt.legend(['train', 'val'], loc='upper left')
        # plt.show()
        plt.savefig('images/plot/accuracy.png')

    def new_model(self):
        self.describe_model()
        self.tokenize_data()
        self.TFIDF()
        self.make_model()
        self.load_model()
        self.show_plot()

    def build_model(self):
        self.describe_model()
        self.tokenize_data()
        # self.make_model()
        self.load_model()
        self.show_plot()

    def predict_comment(self,text):
        # self.build_model()
        self.model = load_model('model/My_model.h5')
        with open('data/tokenizer.pickle', 'rb') as handle:
            tokenizer2 = pickle.load(handle)
        twt=[]
        twt.append(text)
        print(twt)
        # vectorizing the tweet by the pre-fitted tokenizer instance
        twt = tokenizer2.texts_to_sequences(twt)
        # padding the tweet to have exactly the same shape as `embedding_2` input
        twt = pad_sequences(twt, maxlen=110, dtype='int32', value=0)
        print(twt)

        sentiment = self.model.predict(twt,batch_size=1, verbose=2)[0]
        kelas=self.model.predict_classes(twt,batch_size=1)
        print(kelas)
        print(sentiment)
        if (kelas == [0]):
            print("Cyberbullying")
        elif (kelas == [1]):
            print("Irrelevant")
        elif (kelas == [2]):
            print("Netral")
        else:
            print("Non Cyberbullying")

        dict={}
        dict['class']=kelas
        dict['probabilities']=sentiment
        print(dict['class'])
        print(dict['probabilities'][1])
        return dict

    def balas_komen(self,text):
        import Prepocessing_sentence as normal
        self.model = load_model('model/My_model.h5')
        with open('data/tokenizer.pickle', 'rb') as handle:
            tokenizer2 = pickle.load(handle)
        text=normal.text_prepocessing(text)
        twt=[]
        twt.append(text)
        print(twt)
        # vectorizing the tweet by the pre-fitted tokenizer instance
        twt = tokenizer2.texts_to_sequences(twt)
        # padding the tweet to have exactly the same shape as `embedding_2` input
        twt = pad_sequences(twt, maxlen=110, dtype='int32', value=0)
        print(twt)

        sentiment = self.model.predict(twt,batch_size=1, verbose=2)[0]
        kelas=self.model.predict_classes(twt,batch_size=1)
        print(kelas)
        print(sentiment)
        if (kelas == [0]):
            kelas=0
        elif (kelas == [1]):
            kelas=1
        elif (kelas == [2]):
            kelas=2
        else:
            kelas=3
        return kelas

    def prediction(self,array):
        import Prepocessing_sentence as normal
        self.model = load_model('model/My_model.h5')
        with open('data/tokenizer.pickle', 'rb') as handle:
            tokenizer2 = pickle.load(handle)
        print(array)
        # vectorizing the tweet by the pre-fitted tokenizer instance
        twt = tokenizer2.texts_to_sequences(array)
        # padding the tweet to have exactly the same shape as `embedding_2` input
        twt = pad_sequences(twt, maxlen=110, dtype='int32', value=0)
        print(twt)

        sentiment = self.model.predict(twt, batch_size=1, verbose=2)[0]
        kelas = self.model.predict_classes(twt, batch_size=1)
        return kelas

# test=LSTM_model()
# test.build_model()
# test.predict_comment('ada yang bulat tapi bukan tekat')
