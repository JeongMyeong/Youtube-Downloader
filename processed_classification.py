#
from keras.models import load_model
from sklearn.externals.joblib import load as stdload
from gensim.models import Word2Vec
import numpy as np
from konlpy.tag import Okt
import warnings
from gensim import models
warnings.filterwarnings('ignore')


class ProcessSentence:
    def __init__(self):
        self.cnn_model = load_model('C:/Users/JeongMyeong/Desktop/Jupyter/newmodel2.h5')
        self.scaler = stdload('C:/Users/JeongMyeong/Desktop/Jupyter/std_scaler.bin')
#         self.word2vec_model = Word2Vec.load('C:/Users/JeongMyeong/Desktop/word-embeddings/word2vec/word2vec')
        self.word2vec_model = models.fasttext.load_facebook_model('C:/Users/JeongMyeong/Desktop/word-embeddings/fasttext/fasttext.bin')
        self.tagger = Okt()
        self.subjects = {0: '게임'
            , 1: '음악'
            , 2: 'IT기기'
            , 3: '영화리뷰'}

    def sent_to_vec(self, sentence):
        sentence = self.tagger.morphs(sentence)
        sentence_vector = []
        tmp = []
        for word in sentence:
            try:
                tmp.append(self.word2vec_model.wv.word_vec(word))
            except:
                pass
        if tmp == []:
            sentence_vector.append(np.zeros((self.word2vec_model.wv.vector_size,), dtype='float32'))
        else:
            sentence_vector.append(sum(tmp) / len(tmp))

        self.sentence_scale = self.scaler.transform(sentence_vector)
        return self.sentence_scale

    def predict(self, X):
        pred = self.cnn_model.predict(X)
        pred = list(pred[0])
        result = pred.index(max(pred))

        return self.subjects[result]


if __name__ == '__main__':
    test = ProcessSentence()
    X = test.sent_to_vec('이석현 애쉬 캐리')
    print(test.predict(X))



