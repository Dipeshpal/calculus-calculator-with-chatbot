import random
import json
from keras.models import load_model
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

nltk.data.path.append('./nltk_data/')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def returnBagOfWords(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))


def predictionFilter(sentence, model):

    bagOfWords = returnBagOfWords(sentence, words, show_details=False)
    res = model.predict(np.array([bagOfWords]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbotResponse(sentence):
    ints = predictionFilter(sentence, model)
    res = getResponse(ints, intents)
    return res


# initiate chatbot
sentence = "Hello World!"
chatbotResponse(sentence)
