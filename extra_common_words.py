from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk
import re
import pymorphy2 as pm2

morph = pm2.MorphAnalyzer()

def lema(word):
    p = morph.parse(word)[0]
    return p.normal_form

class Extra_common_words_summarization:

    def preprocess(self, sentence, lemma, language='english'):
        regular = r'[a-z]*'
        if language == 'russian':
            regular = r'[а-я]*'

        copy = sentence.lower()
        words = word_tokenize(copy)
        final_form = [lemma(word) for word in words if not word in stopwords.words(language)]
        final_form = [word for word in final_form if re.fullmatch(regular, word)]
        return final_form

    def similarity(self, sent1, sent2, lemma, language='english'):
        prepared_1 = self.preprocess(sent1, lemma, language=language)
        prepared_2 = self.preprocess(sent2, lemma, language=language)
        num_of_common = 0
        for word in prepared_1:
            if word in prepared_2:
                num_of_common += 2
        try:
            return num_of_common / (len(prepared_1) + len(prepared_2))
        except ZeroDivisionError:
            return 0

    def get_weights(self, sentences, lemma, language='english'):
        weight = [[0, i] for i in range(len(sentences))]
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    weight[i][0] += self.similarity(sentences[i], sentences[j], lemma, language=language)
        return weight

    def summarize(self, text, language='english'):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        sentences = sent_tokenize(text)
        lemma = WordNetLemmatizer().lemmatize
        if language == 'russian':
            lemma = lema
        
        weight = sorted(self.get_weights(sentences, lemma, language=language))[::-1]

        summary_len = (len(sentences) + 9) // 10
        indexies = sorted([weight[i][1] for i in range(summary_len)])
        
        summary = ' '.join([sentences[i] for i in indexies])
        print(weight[0][0], ' ', weight[summary_len - 1][0])
        return summary

if __name__ == '__main__':

    with open('data.txt', 'r') as file:
        text = file.read()
        summary = Extra_common_words_summarization().summarize(text, language='russian')
        print(summary)