#!/usr/bin/python3

import os
import sys
import json as js
import math
import re

from config import *

def tf_idf():
    regex_head = "<(\s|\t)*(head|HEAD)(.*)>(.*)<(\s|\t)*/(\s|\t)*(head|HEAD)>"
    regex_script = "<(\s|\t)*(script|SCRIPT)(.*)>(.*)<(\s|\t)*/(\s|\t)*(script|SCRIPT)(\s|\t)*>"
    regex_balise_close = "</(.*)>"
    regex_balise_orphan = "<(.*)/>"
    regex_balise = "<(.*)>"

    corpus_size = 0
    keyword_corpus = {}
    tf_corpus = {}
    tf_idf_corpus = {}
    os.chdir(webpages_dir)
    file_list = os.listdir(".")

    for file_name in file_list :
        working_file = open(file_name, "r", errors = "replace")
        working_tf = {}
        is_present = {}
        corpus_size_buffer = corpus_size
        ignore_file = False

        if debug :
            print(file_name)
            print("traitement")

        try:
            working_string = working_file.read()
            corpus_size = corpus_size + 1

            #on retire les balises
            working_string = re.sub(regex_head,"", working_string)
            working_string = re.sub(regex_script,"", working_string)

            #on retire la mise en forme
            working_string = working_string.replace("\n", " ")
            working_string = working_string.replace("\t","")

            working_string = re.sub(regex_balise_close, "", working_string)
            working_string = re.sub(regex_balise_orphan, "", working_string)
            working_string = re.sub(regex_balise, "", working_string)
            #on sépare les mots clés du texte
            working_split = working_string.split(" ")

            keyword_number = len(working_split)

        except OSError as e:
            corpus_size = corpus_size_buffer
            working_split = []
            ignore_file = True
            tf_corpus.pop(file_name, None)
            print("Erreur avec le fichier "+file_name+" \n")
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

        if debug :
            print("dump tf-idf")

        js_dump = open("tf_idf.json", "w")
        js.dump(tf_idf_corpus, js_dump)
        js_dump.close()

        if debug :
            print("dump mot-clefs")

        keyword_dump = open("keyword.json", "w")
        js.dump(keyword_corpus, keyword_dump)
        keyword_dump.close()

    except OSError as e:
        print("erreur json")

if __name__ == "__main__" :
    tf_idf()
