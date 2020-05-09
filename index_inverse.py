import os
import sys
import json as js
import math
import re
import bs4

class index_inverse ():
    webpages_dir = "pages_web"
    debug = True

    corpus_size = 0
    keyword_corpus = {}
    tf_corpus = {}
    tf_idf_corpus = {}

    current_dir = os.getcwd()
    file_list = None
    def __init__ (self, directory = "pages_web", score ="tf-idf"):
        self.webpages_dir = directory
        self.file_list = os.listdir(self.webpages_dir)
        self.score = score


    def compute_tf(self):

        os.chdir(self.webpages_dir)

        for file_name in self.file_list :
            working_file = open(file_name, "r", errors = "replace")
            working_tf = {}
            is_present = {}
            corpus_size_buffer = self.corpus_size
            ignore_file = False

            if self.debug :
                print(file_name)
                print("traitement")

            try:
                working_string = bs4.BeautifulSoup(working_file).text
                self.corpus_size = self.corpus_size + 1
                working_string = re.sub("\(|\)|\[|\]|,|\."," ",working_string)
                working_string = working_string.replace("\n"," ")


                working_split = working_string.split(" ")

                if False :
                    print(working_string)
                    print(working_split)

                keyword_number = len(working_split)

            except OSError as e:
                self.corpus_size = corpus_size_buffer
                working_split = []
                ignore_file = True
                tf_corpus.pop(file_name, None)

                if self.debug :
                    print("Erreur avec le fichier "+file_name+" \n")
                    print("Ce fichier ne sera pris en compte dans le calcul de tf-idf")

            if not ignore_file :
                for keyword in working_split :

                    if keyword in is_present :
                        pass
                    else :
                        is_present[keyword] = True
                        if keyword in self.keyword_corpus :
                            self.keyword_corpus[keyword] += 1
                        else :
                            self.keyword_corpus[keyword] = 1

                    if keyword in working_tf :
                        working_tf[keyword] += 1
                    else :
                        working_tf[keyword] = 1

                for k in working_tf :
                    working_tf[k] =working_tf[k]/keyword_number
                    if not (k in self.tf_corpus):
                        self.tf_corpus[k]={}
                    self.tf_corpus[k][file_name] = working_tf[k]


                working_file.close()

        os.chdir(self.current_dir)

    def compute_tf_idf(self):
        if self.score == "tf-idf":
            for keyword in self.tf_corpus:

                if self.debug :
                    print(keyword)

                self.tf_idf_corpus[keyword] ={}

                for file in self.tf_corpus[keyword]:

                    if self.debug:
                        print(file)

                    idf_keyword = math.log(self.corpus_size/self.keyword_corpus[keyword])
                    self.tf_idf_corpus[keyword][file] = self.tf_corpus[keyword][file]*idf_keyword
