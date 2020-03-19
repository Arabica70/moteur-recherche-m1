#!/usr/bin/python3

import os
import sys
import json as js
import math

from config import *

def tf_idf():

    corpus_size = 0
    keyword_corpus = {}
    tf_corpus = {}
    tf_idf_corpus = {}
    os.chdir(webpages_dir)
    file_list = os.listdir(".")

    for file_name in file_list :
        working_file = open(file_name, "rb")
        working_tf = {}
        is_present = {}
        corpus_size_buffer = corpus_size
        ignore_file = False
        try:
            working_string = str(working_file.read(), errors = "ignore")
            corpus_size = corpus_size + 1
            working_string = working_string.replace("\n", " ")
            working_split = working_string.split(" ")
            keyword_number = len(working_split)
        except OSError as e:
            corpus_size = corpus_size_buffer
            working_split = []
            ignore_file = True
            tf_corpus.pop(working_file, None)
            print("Erreur avec le fichier "+working_file+" \n")
            print("Ce fichier ne sera pris en compte dans le calcul de tf-idf")

        if not ignore_file :
            for keyword in working_split :

                if keyword in is_present :
                    pass
                else :
                    is_present[keyword] = True
                    if keyword in keyword_corpus :
                        keyword_corpus[keyword] += 1
                    else :
                        keyword_corpus[keyword] = 1

                if keyword in working_tf :
                    working_tf[keyword] += 1
                else :
                    working_tf[keyword] = 1

            for k in working_tf :
                working_tf[k] =working_tf[k]/keyword_number

            tf_corpus[file_name] = working_tf
            working_file.close()

    for file in tf_corpus :
        tf_idf_corpus[file] = {}
        for keyword in tf_corpus[file] :
            idf_keyword = math.log(corpus_size/keyword_corpus[keyword])
            tf_idf_corpus[file][keyword] = tf_corpus[file][keyword]*idf_keyword


    try:
        os.chdir("..")
        js_dump = open("tf_idf.json", "w")
        js.dump(tf_idf_corpus, js_dump)
        js_dump.close()
    except OSError as e:
        print("erreur json")

if __name__ == "__main__" :
    tf_idf()
