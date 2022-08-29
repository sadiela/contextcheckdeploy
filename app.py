import os
from flask import Flask, request
import json
import time
import nltk.data

import python_functions.TestSentence as TestSentence
import python_functions.newscraper as newscraper
import python_functions.RelatedArticles_five_calls as RA #import getarticles
import python_functions.keyword_detection as keyword_detection
import python_functions.tips as tips

app = Flask(__name__, static_folder='build/', static_url_path='/')
app.debug = 'DEBUG' in os.environ

keyword_api = "d28b596641e1690c696909f66408b6d0ad53e5ca"

def analyze_sentences(text, start_time):
    # Split into multiple sentences here
    #nltk.download('punkt')
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sentence_tokenizer.tokenize(text)

    # Run through algorithm 
    results = TestSentence.output(sentences)

    #print('SENTENCE RESULTS!', results['sentence_results'])
    results['runtime'] = str(time.time() - start_time) + " seconds\n"

    # REMERGE TOKENIZED WORDS (BID ##EN = BIDEN)
    # Make sure sentence parsing is working?!?!?
    return results

@app.route('/result', methods=['POST'])
def api_post():
    print("GET RESULTS!")
    start_time = time.time() # to keep track of analysis runtime

    # get text and format it
    text = request.data
    texty = text.decode('utf-8')
    dictionary = json.loads(texty) # why are we loading it into a dictionary and then back out? 
    #print(dictionary['myText'])
    var = dictionary['myText'] #.lower()

    res = analyze_sentences(var, start_time)
    return res

@app.route('/scrape', methods=['POST'])
def scrape_article():
    start_time = time.time() # to keep track of analysis runtime
    url = request.data
    url = url.decode('utf-8')
    url = json.loads(url)
    print(url)
    url = url['input_url']
    print("PARSING URL")
    res = newscraper.article_parse(url)
    if type(res) is not dict: 
        print("NOT A DICTIONARY:", type(res))
        res = json.loads(res) 

    # res.title, res.author, res.feedText, res.date, res.meta (?)
    print("DONE SCRAPING")
    results = analyze_sentences(res['feedText'], start_time)
    res['bias_results'] = results
    print("DATE:", res['date'])
    
    keywords = keyword_detection.get_keywords(res['title'] + " " + res['feedText'])
    print(keywords)
    related_articles = RA.getarticles(keywords, url)
    # Call function # return dictionary of {"left":url1, "left-leaning":url2 etc.}
    res['related'] = related_articles

    return res

@app.route('/loaderwords', methods=['GET'])
def get_word():
    return tips.get_tips()

@app.route('/', methods=['GET', 'POST'])
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

'''@app.route('/', methods=['GET', 'POST'])
def index():
    return app.send_static_file('index.html')


'''

# https://heroku-framework18.herokuapp.com/