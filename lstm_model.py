import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.layers import Embedding,Dense,LSTM,SpatialDropout1D
import tensorflow
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from sklearn.utils import resample
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix,classification_report
import re
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import json
import tensorflow as tf

PROCESSED_DATA_PATH = 'data/hasil'
train_data = pd.read_csv('{}/clear_train.csv'.format(PROCESSED_DATA_PATH))
train_data = train_data[['hasil_normalisasi', 'Label']]

class LSTM_model:

    def __init__(self,filepath=PROCESSED_DATA_PATH):
        self.max_fatures = 2000
        self.batch_size = 128
        self.build_model()
        return print('Train data shape                 :', train_data.shape)

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

    def make_model(self):
        embed_dim = 128
        lstm_out = 196
        model = tensorflow.keras.Sequential()
        model.add(Embedding(self.max_fatures,embed_dim,input_length=self.X.shape[1]))
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
        self.build_model()
        twt=[]
        twt.append(text)
        print(twt)
        # vectorizing the tweet by the pre-fitted tokenizer instance
        twt = self.tokenizer.texts_to_sequences(twt)
        # padding the tweet to have exactly the same shape as `embedding_2` input
        twt = pad_sequences(twt, maxlen=112, dtype='int32', value=0)
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
        text=normal.text_prepocessing(text)
        twt=[]
        twt.append(text)
        print(twt)
        # vectorizing the tweet by the pre-fitted tokenizer instance
        twt = self.tokenizer.texts_to_sequences(twt)
        # padding the tweet to have exactly the same shape as `embedding_2` input
        twt = pad_sequences(twt, maxlen=112, dtype='int32', value=0)
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


# test=LSTM_model()
# test.build_model()
# test.predict_comment('ada yang bulat tapi bukan tekat')
