from constant import PROJECT_ROOT
import pdfplumber
import os
import re
import json
from pprint import pprint
from tqdm import tqdm

def get_words():
    pdf_file = PROJECT_ROOT + "/temp_files/page-1.pdf"
    words = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            words = page.extract_words(x_tolerance=0, y_tolerance=0)

    return words



def find_y_cordinate_overlap(word_1, word_2):
    if word_1['top'] >= word_2['top'] <= word_1['bottom']:
        if int(word_2['bottom'] - word_1['top']) <= 3:
            return False
        return True

    if word_1['top'] >= word_2['bottom'] <= word_1['bottom']:
        return True

    if word_2['top'] >= word_1['top'] <= word_2['bottom']:
        if int(word_2['top'] - word_1['bottom']) <= 3:
            return False
        return True

    if word_2['top'] >= word_1['top'] <= word_2['bottom']:
        if int(word_2['top'] - word_1['bottom']) <= 3:
            return False

        return True

    return False

def find_x_cordinate_overlap(word_1, word_2):

    if word_1['x0'] >= word_2['x0'] <= word_1['x1']:
        if word_1['x0'] > word_2['x1']:
            return False
        return True

    if word_1['x0'] >= word_2['x1'] <= word_1['x1']:
        return True

    if word_2['x0'] >= word_1['x0'] and word_1['x1'] >= word_2['x1']:
        return True

    return False


def find_overlaps():
    overlap_words = []
    words = get_words()
    for word_1 in words:
        #all_words.append(word_1['text'])
        if len(word_1['text']) < 2:
            continue
        for word_2 in words:
            if len(word_1['text']) < 2 or len(word_2['text']) < 2:
                continue
       
            if word_1['text'] != word_2['text']:
                if word_2['x0'] > word_1['x1'] or word_2['x1'] < word_1['x0']:
                    continue
                if word_2['top'] > word_1['bottom'] or word_2['bottom'] < word_1['top']:
                    continue
       
                flag = find_x_cordinate_overlap(word_1, word_2)
                if flag:
                    if find_y_cordinate_overlap(word_1, word_2):
                        print("********FOUND*********")
                        print(f"word_1--->{word_1}")
                        print(f"word_2--->{word_2}")
                        print("********FOUND*********")
                        #print(f"all_words--->{all_words}")
                        #found = found + 1
                        #if found == 10:
                        #   exit()
                        #overlap_words.append({"word_1": word_1['text'], "word_2": word_2['text']})
                        overlap_words.append( [ word_1['text'], word_2['text'] ] )

    json_data = []
    #json_data.append({"description": "Overlap", "data": overlap_words, "headers": ['word', 'overlapping word'], 'type': 'multiple'})
    json_data.append({"description": "Overlap Found on Page 1", "data": overlap_words, "headers": ['word', 'overlapping word'], 'type': 'multiple'})
    return json_data
    #return overlap_words

def extract_overlaps():
    return find_overlaps()
