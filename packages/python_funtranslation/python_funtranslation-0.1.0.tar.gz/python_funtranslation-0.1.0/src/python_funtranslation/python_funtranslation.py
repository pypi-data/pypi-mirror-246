import requests
import json

import os
import random
import re

import lxml
from lxml import html
from lxml import etree

import pandas as pd
import urllib.parse

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


languages = {
    # fictions
    'tolkien': ['sindarin', 'quenya'],
     'starwars': ['yoda', 'sith', 'gungan', 'huttese', 'mandalorian', 'cheunh'],
     'startrek': ['vulcan', 'klingon'],
     'gameofthrones': ['dothraki', 'valyrian'],
     'marvel': ['groot', 'minion'],

     # english varieties
     'englishes': ['oldenglish', 'shakespeare', 'post-modern', 'pirate'],
     
     # language games
     'wordgame': ['leetspeak', 'pig-latin', 'ferb-latin']}

languages_list = [val for key, values in languages.items() for val in values]
languages_list.append('morse') # special category


def get_full_description(language = 'leetspeak'):
    """
    Get the full description of one fun language by web scraping.

    Parameters
    ----------
    language : string
        Set as 'leetspeak' by default.

    Returns
    -------
    Returns a string of the language's full description
    Returns "no description" if the input language is not a part of the Fun Translation API website.

    Example
    --------
    >>> get_full_description()
    'Convert from English to Leet Speak. Leetspeak an informal language or code used on the Internet, in which standard letters are often replaced by numerals or special characters. It is also sometimes referred as H4X0R which is "Hacker" in leetspeak. Leet (or "1337"), also known as eleet or leetspeak, can be thought of as an alternative alphabet for the English language. It is used primarily on the Internet. It uses various combinations of ASCII characters to replace Latinate letters. For example, leet spellings of the word leet include 1337 and l33t; eleet may be spelled 31337 or 3l33t.'

    >>> get_full_description(language = 'post-modern')
    'Convert from plain English to Postmordern Speak. If you have the need to sound semiotic-ally and subliminally cool in party conversations we can help you! Our post-modern translator will make you the sophisticated conversationalist.'
    """
    web_url = f'https://funtranslations.com/{language}'
    web_html = requests.get(web_url)
    web_doc = html.fromstring(web_html.content)
    description = web_doc.xpath('//meta[@name="description"]/@content')
    if description:
        return description[0]
    else:
        return "no description"



def get_languages():
    """
    Get short descriptions of all fun languages and their category.
    
    """
    result = []
    for category, language_list in languages.items():
        for language in language_list:
            description = get_full_description(language)
            sentences = description.split('. ')
            new_description = '. '.join(sentences[1:])
            result.append({"language": language, "description": new_description})
    df1 = pd.DataFrame(result)
    df2 = pd.DataFrame([(key, val) for key, values in languages.items() for val in values], columns=['category', 'language'])
    df = pd.merge(df2, df1, on='language')
    return df

def get_translation_json(in_text = 'Hello World!', target_language = 'random'):
    """
    Translate input text into one fun target language and returns the json format of API client request.

    Parameters
    ----------
    in_text :  string
        Set as 'Hello World!' by default.
        Strongly recommended in_text language: English

    target_language : string
        Set as "random" by default.
        Use the function get_languages() for more information on available target languages.
    
    Returns
    -------
    Returns the json format of API client request

    Example
    --------
    >>> get_translation_json()
    {'success': {'total': 1},
    'contents': {'translated': "Hello qo'!",
    'text': 'Hello World!',
    'translation': 'klingon'}}
    """
    
    url_text = urllib.parse.quote(in_text)

    if target_language == 'random':
        category = random.choice(list(languages.keys()))
        target_language = random.choice(languages[category])
    url = f'https://api.funtranslations.com/translate/{target_language}.json?text={url_text}'
    #headers = {'X-Funtranslations-Api-Secret': API_KEY}
    #r1 = requests.get(url, headers=headers)
    r1 = requests.get(f'https://api.funtranslations.com/translate/{target_language}.json?text={url_text}')
    fun_json1 = r1.json()
    return fun_json1



def get_hard2read(in_text = 'How hard can it be?', lan1 = 'minion', lan2 = 'leetspeak'):
    """
    Turn your input into a secret code by translating it twice.

    Parameters
    ----------
    in_text : string
        Set as 'How hard can it be?' by default.
        Strongly recommended in_text language: English

    lan1 : string
        Set as 'minion' by default.
        This is the language your input firstly gets translated into.
        Use the function get_languages() for more information on available target languages.

    lan2 : string
        Set as 'leetspeak' by default.
        This is the language your input eventually gets translated into.
        Strongly recommended lan2: leetspeak, pig-latin, ferb-latin, morse
    
    Returns
    -------
    Returns a string as a secret code.
    Returns False if the input is not correct.
    Returns nothing if the request fails.

    Example
    --------
    >>> get_hard2read()
    '4m3e 0W PUdum p!K 83?'
    
    >>> get_hard2read(lan1 = "newspeak")
    False
    """

    if type(lan1) != str or lan1.lower() not in languages_list or type(lan2) != str or lan2.lower() not in languages_list:
        return False
    
    json1 = get_translation_json(in_text = in_text, target_language = lan1)
    if list(json1.keys())[0] != 'success': return
    text2 = json1['contents']['translated']
    json2 = get_translation_json(in_text = text2, target_language = lan2)
    if list(json1.keys())[0] != 'success': return
    return json2['contents']['translated']



def get_translation(
    in_text = """Some say the world will end in fire,
    Some say in ice.
    From what I’ve tasted of desire
    I hold with those who favor fire.
    But if it had to perish twice,
    I think I know enough of hate
    To say that for destruction ice
    Is also great
    And would suffice.""", 
    target_languages = ['klingon'],
    by_sentence = False):
    
    """
    Get some fun translations in a pd dataframe format.

    Parameters
    ----------
    in_texts: string
        Set as a short poem by Robert Frost by default.
        Strongly recommended in_text language: English

    target_languages : list parameter
        Set as ['klingon'] by default.
        Put all fun languages you want the in_text to be translated into!
        However, users of public endpoint without an API key have a rate limit. Be careful!

    by_sentence : boolean
        Set as False by default.
        Decides whether the output is separated by sentences.
        Yoda speak and morse code cannot be seperated by sentence.
    
    Returns
    -------
    Returns a dataframe that contains the input text, the translated text, and the corresponding fun language of the translated text.

    Example
    --------
    >>> get_translation(target_languages = ['klingon', 'sith'])
        Sentence	Translated	Translation
    0	Some say the world will end in fire, Some say ...	'op jatlh the qo' will van in qul, 'op jatlh ...	klingon
    1	Some say the world will end in fire, Some say ...	Kair zodis tave visuom valia qorit kash saud, ...	sith
    
    """
    

    in_text = in_text.replace('\n', ' ')
    in_text = re.sub(r'\s+', ' ', in_text)

    in_list = []
    out_list = []
    lan_list = []
    df = pd.DataFrame({'Sentence':[], 'Translated': [], 'Translation': []})

    if type(target_languages) != list:
        return False
        
    else:
        for target in target_languages:
            if type(target) != str or target.lower() not in languages_list:
                continue
                
            else:
                json = get_translation_json(in_text = in_text, target_language = target.lower())

            if list(json.keys())[0] != 'success':
                in_list.append(in_text)
                out_list.append('')
                lan_list.append(target)
                continue
                
            if by_sentence == True:
                sentences1 = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', json['contents']['text'])
                sentences2 = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', json['contents']['translated'])
                df1 = pd.DataFrame({'Sentence': sentences1, 'Translated': sentences2, 'Translation': json['contents']['translation']})
                df = pd.concat([df, df1])

            else:
                in_list.append(json['contents']['text'])
                out_list.append(json['contents']['translated'])
                lan_list.append(json['contents']['translation'])
                
            data = {'Sentence': in_list, 'Translated': out_list, 'Translation': lan_list}
            df_data = pd.DataFrame(data)
            
        if by_sentence == False: return df_data
        else: return df
    



def sentence_similarity(sentence1, sentence2):
    """
    Calculate the percentage of similarity between two sentences.
    
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([sentence1, sentence2])
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity_score


def similarity_matrix(sentences):
    """
    Generate a matrix for the compare_fun_languages function
    
    """
    n = len(sentences)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            matrix[i][j] = sentence_similarity(sentences[i], sentences[j])
    return matrix



def compare_fun_languages(in_text = """Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!""", 
    target_languages = ['sindarin', 'yoda', 'vulcan', 'dothraki', 'groot', 'oldenglish', 'leetspeak'],
    heatmap = True, mapnote = False):

    
    """
    Compare some fun translations by looking at their similarity heatmap, their similarity matrix, or simply the translation result gathered in a pd dataframe.

    Parameters
    ----------
    in_text : string
        Set as Zen of Python by default.
        Strongly recommended in_text language: English

    target_languages : list parameter
        Set as ['sindarin', 'yoda', 'vulcan', 'dothraki', 'groot', 'oldenglish', 'leetspeak'] by default.
        Put all fun languages you want the in_text to be translated into!
        However, users of public endpoint without an API key have a rate limit. Be careful!

    heatmap : boolean
        Set as True by default.
        Decides whether show a graph that compares fun languages.

    mapnote : boolean
        Set as False by default.
        Decides the graph displays the specific numbers of sentence similarity.
    
    Returns
    -------
    return[0]: a dataframe that contains the input text, the translated text, and the corresponding fun language of the translated text.
    return[1]: a matrix of sentence similarity
    if hearmap == True, there will be a return[2], which is the heatmap graph.

    """

    
    df = get_translation(in_text = in_text, target_languages = target_languages, by_sentence = False)
    sentences = list(df['Translated'])
    sentences.append(in_text)
    lans = list(df['Translation'])
    lans.append('input language')
    matrix = similarity_matrix(sentences)
    if heatmap == True:
        graph = sns.heatmap(matrix, annot= mapnote, xticklabels=lans, yticklabels=lans)
        graph.set_title('Language Similarity Heatmap')
        plt.show()
        return df, matrix, graph
    return df, matrix
