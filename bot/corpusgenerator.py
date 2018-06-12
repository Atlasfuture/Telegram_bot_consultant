from random import choice
from re import split
import json


class CorpusGenerator:
    def __init__(self, load=False):
        """dictionary of lists
        each dictionary has key as next word and value as it`s frequency"""
        self.__words = {}

        self.__words["*START*"] = []

        if load:
            self.load()

        self.__last_parts = []

    def __add_words(self, key_word, word):
        """add key word if not exsist in dictionary
        add word to dictionary of current key word"""
        if not key_word in self.__words:
            self.__words[key_word] = []

        if not word in self.__words[key_word]:
            self.__words[key_word].append(word)


    def __add_start(self, word):
        """Add every first word in sentence"""
        if not word in self.__words["*START*"]:
            self.__words["*START*"].append(word)

    def __read_sent(self, sent):
        parts = split('[ |,|:]', sent)

        length = len(parts)

        """Add first word"""
        self.__add_start(parts[0])


        """Add last word"""
        if not length == 1:
            self.__add_words(parts[length - 1], "*END*")
        else:
            self.__add_words(parts[0], "*END*")

        for i in range(0, length - 1):
            self.__add_words(parts[i], parts[i + 1])

        self.__last_parts = parts



    def process(self, text):
        sentences = split('[.|!|?]', text)


        for sent in sentences:
            if not sent == '':
                self.__read_sent(sent)


    def generate(self, min_length = 3, max_length=20):
        sent = ""

        word = choice(self.__last_parts)




        if not word in self.__words:
            word = choice(self.__words["*START*"])


        current_length = 0
        while not '*END*' in word and not current_length == max_length:
            current_length+=1
            sent += ' ' + word

            words_list = self.__words[word]

            word = choice(words_list)

            if word == "*END*" and not len(words_list)==1 and current_length < min_length:
                words_list.remove("*END*")
                word = choice(words_list)



        return sent


    def save(self, path="bot_memory.json"):
        with open(path, 'w') as outfile:
            json.dump(self.__words, outfile)

    def load(self, path="bot_memory.json"):
        with open(path) as json_data:
            self.__words = json.load(json_data)