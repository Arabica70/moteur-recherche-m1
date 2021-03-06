import os
import sys
import json as js
import math
import re
import bs4
import chardet

class index_inverse ():
    webpages_dir = "pages_web"
    debug = True
    use_chardet = True

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
            if self.use_chardet:
                working_file = open(file_name, "rb")
                detect = chardet.detect(working_file.read())
                encoding = detect["encoding"]
                confidence = detect["confidence"]
                if confidence > 0.90:
                    working_file = open(file_name, "r", errors= "replace", encoding = encoding)
                else:
                    working_file = open(file_name, "r", errors= "replace", encoding = None)
            else :
                working_file = open(file_name, "r", errors= "replace")


            working_tf = {}
            is_present = {}
            corpus_size_buffer = self.corpus_size
            ignore_file = False

            if self.debug :
                print(file_name)
                print("traitement")

            try:
                working_string = bs4.BeautifulSoup(working_file).prettify()
                working_string = bs4.BeautifulSoup(working_string).text
                self.corpus_size = self.corpus_size + 1
                working_string = re.sub("\(|\)|\[|\]|,|\.|;"," ",working_string)
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

                if self.score == "tf-idf" or self.score =="log":
                    for k in working_tf :
                        if self.score == "tf-idf" :
                            working_tf[k] =working_tf[k]/keyword_number
                        elif self.score =="log" :
                            working_tf[k] = working_tf[k]/keyword_number
                            working_tf[k] = 1+math.log(working_tf[k])

                        if not (k in self.tf_corpus):
                            self.tf_corpus[k]={}
                        self.tf_corpus[k][file_name] = working_tf[k]

                if self.score =="max" :
                    for k in working_tf:
                        working_tf[k] =working_tf[k]/keyword_number

                    max_tf = max(working_tf.values())

                    for k in working_tf:
                        working_tf[k] = 0.5+ 0.5*(working_tf[k]/max_tf)

                        if not (k in self.tf_corpus):
                            self.tf_corpus[k]={}

                        self.tf_corpus[k][file_name] = working_tf[k]

                if self.score == "binary":
                    for k in working_tf:
                        working_tf[k] = 1

                        if not (k in self.tf_corpus):
                            self.tf_corpus[k]={}

                        self.tf_corpus[k][file_name] = working_tf[k]


                working_file.close()

        os.chdir(self.current_dir)

    def compute_tf_idf(self):
        if self.score == "tf-idf" or self.score == "max" or self.score == "log" or self.score == "binary":
            for keyword in self.tf_corpus:

                if self.debug :
                    pass

                self.tf_idf_corpus[keyword] ={}

                for file in self.tf_corpus[keyword]:

                    if self.debug:
                        print(keyword)
                        print(file)

                    idf_keyword = math.log(self.corpus_size/self.keyword_corpus[keyword])
                    self.tf_idf_corpus[keyword][file] = self.tf_corpus[keyword][file]*idf_keyword

                    if self.debug :
                        print(self.tf_idf_corpus[keyword][file])



    def sort_tf_idf(self, keyword):
        sorted_tf_idf = {}
        try:
            sorted_tf_idf = sorted(self.tf_idf_corpus[keyword].items(), key = lambda item: item[1])
            return sorted_tf_idf
        except NameError as e:
            return None
        except KeyError as e :
            return None

    def ten_first(self, keyword):
        sorted_tf_idf = self.sort_tf_idf(keyword)
        ten_first_pages = []
        i = 0

        for item in sorted_tf_idf:
            if self.debug:
                print(item)
                ten_first_pages.append(item)

            if i > 10 :
                break
            i = i+1
        return ten_first_pages

    def compute(self):
        if self.score == "bm-25":
            pass
        else :
            self.compute_tf()
            self.compute_tf_idf()
