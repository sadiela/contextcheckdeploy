#################
#### Imports ####
#################

# C:\Users\sadie\AppData\Roaming\Python\Python38\Scripts\pipenv shell

import os

import numpy as np
import statistics
import spacy

# torch imports
import torch

# pretrained BERT imports
from pytorch_pretrained_bert.tokenization import BertTokenizer

# other user scripts
from python_functions.models import  BertForMultitaskWithFeatures #, BertForMultitask

nlp = spacy.load("en_core_web_sm")

CUDA = (torch.cuda.device_count() > 0)
if CUDA:
    print("GPUS!")
    input()


## UPDATE THESE!!!
DATA_DIRECTORY = './data/'
LEXICON_DIRECTORY = DATA_DIRECTORY + 'lexicons/'
cache_dir = DATA_DIRECTORY + 'cache/'
model_save_dir = './python_functions/'


def read_lexicon(fp):
        # returns word list as a set
        out = set([
            l.strip() for l in open(fp, errors='ignore') 
            if not l.startswith('#') and not l.startswith(';')
            and len(l.strip().split()) == 1
        ])
        return out

def wordtype(word):
    print(word)

    lexicons = {
            'assertives': read_lexicon(LEXICON_DIRECTORY + 'assertives_hooper1975.txt'),
            'entailed_arg': read_lexicon(LEXICON_DIRECTORY + 'entailed_arg_berant2012.txt'),
            'entailed': read_lexicon(LEXICON_DIRECTORY + 'entailed_berant2012.txt'), 
            'entailing_arg': read_lexicon(LEXICON_DIRECTORY + 'entailing_arg_berant2012.txt'), 
            'entailing': read_lexicon(LEXICON_DIRECTORY + 'entailing_berant2012.txt'), 
            'factives': read_lexicon(LEXICON_DIRECTORY + 'factives_hooper1975.txt'),
            'hedges': read_lexicon(LEXICON_DIRECTORY + 'hedges_hyland2005.txt'),
            'implicatives': read_lexicon(LEXICON_DIRECTORY + 'implicatives_karttunen1971.txt'),
            'negatives': read_lexicon(LEXICON_DIRECTORY + 'negative_liu2005.txt'),
            'positives': read_lexicon(LEXICON_DIRECTORY + 'positive_liu2005.txt'),
            'npov': read_lexicon(LEXICON_DIRECTORY + 'npov_lexicon.txt'),
            'reports': read_lexicon(LEXICON_DIRECTORY + 'report_verbs.txt'),
            'strong_subjectives': read_lexicon(LEXICON_DIRECTORY + 'strong_subjectives_riloff2003.txt'),
            'weak_subjectives': read_lexicon(LEXICON_DIRECTORY + 'weak_subjectives_riloff2003.txt')
        }

    word_tags = []
    for l in list(lexicons.keys()):
        #print(lexicons[l], type(lexicons[l]))
        # each lexicon is a set
        if word in lexicons[l]:
            word_tags.append(l)

    if not word_tags:
        word_tags.append("NONE")
    print(word_tags)
    return word_tags[0]

#####################
### Softmax #############
#####################
def softmax(x, axis=None):
  x=x-x.max(axis=axis, keepdims=True)
  y= np.exp(x)
  return y/y.sum(axis=axis, keepdims=True)

##########################################################
#### SET UP ID DICTIONARIES FOR WORDS, RELATIONS, POS ####
##########################################################


RELATIONS = [
  'det', # determiner (the, a)
  'amod', # adjectival modifier
  'nsubj', # nominal subject
  'prep', # prepositional modifier
  'pobj', # object of preposition
  'ROOT', # root
  'attr', # attribute
  'punct', # punctuation
  'advmod', # adverbial modifier
  'compound', # compound
  'acl', # clausal modifier of noun (adjectivial clause)
  'agent', # agent
  'aux', # auxiliary
  'ccomp', # clausal complement
  'dobj', # direct object
  'cc', # coordinating conjunction 
  'conj', # conjunct
  'appos', # appositional 
  'nsubjpass', # nsubjpass
  'auxpass', # auxiliary (passive)
  'poss', # poss
  'nummod', # numeric modifier
  'nmod', # nominal modifier
  'relcl', # relative clause modifier
  'mark', # marker
  'advcl', # adverbial clause modifier
  'pcomp', # complement of preposition
  'npadvmod', # noun phrase as adverbial modifier
  'preconj', # pre-correlative conjunction
  'neg', # negation modifier
  'xcomp', # open clausal complement
  'csubj', # clausal subject
  'prt', # particle
  'parataxis', # parataxis
  'expl', # expletive
  'case', # case marking
  'acomp', # adjectival complement
  'predet', # ??? 
  'quantmod', # modifier of quantifier
  'dep', # unspecified dependency
  'oprd', # object predicate
  'intj', # interjection
  'dative', # dative
  'meta', # meta modifier
  'csubjpass', # clausal subject (passive)
  '<UNK>' # unknown
]

REL2ID = {x: i for i,x in enumerate(RELATIONS)}

# PARTS OF SPEECH
POS_TAGS = [
  'DET', # determiner (a, an, the)
  'ADJ', # adjective (big, old, green, first)
  'NOUN', # noun (girl, cat, tree)
  'ADP', # adposition (in, to, during)
  'NUM', # numeral (1, 2017, one, IV)
  'VERB', # verb (runs, running, eat, ate)
  'PUNCT', # punctuation (., (, ), ?)
  'ADV', # adverb (very, tomorrow, down)
  'PART', # particle ('s, not)
  'CCONJ', # coordinating conjunction (and, or, but)
  'PRON', # pronoun(I, you, he, she)
  'X', # other (fhefkoskjsdods)
  'INTJ', # interjection (hello, psst, ouch, bravo)
  'PROPN', # proper noun (Mary, John, London, HBO) 
  'SYM', # symbol ($, %, +, -, =)
  '<UNK>' # unknown
]

POS2ID = {x: i for i, x in enumerate(POS_TAGS)}

EDIT_TYPE2ID = {'0':0, '1':1, 'mask':2}

# BERT initialization params
config = 'bert-base-uncased'
cls_num_labels = 43
tok_num_labels = 3

tokenizer = BertTokenizer.from_pretrained(config, os.getcwd() + '/cache')
tok2id = tokenizer.vocab
tok2id['<del>'] = len(tok2id)


# PADDING TO MAX_SEQ_LENGTH
def pad(id_arr, pad_idx):
  max_seq_len = 60
  return id_arr + ([pad_idx] * (max_seq_len - len(id_arr)))

def to_probs(logits, lens):
    #print(logits)
    per_tok_probs = softmax(np.array(logits)[:, :, :2], axis=2)
    pos_scores = per_tok_probs[-1, :, :]
    out = []
    #for score_seq, l in zip(pos_scores, lens):
    out.append(pos_scores[:].tolist())
    return out

# Take one sentence ... 
def run_inference(model, ids, pos_ids): #, tokenizer):
    #global ARGS
    # we will pass in one sentence, no post_toks, 

    out = {
        'input_toks': [], # text input
        'tok_logits': [],
        'tok_probs': [] # bias probabilities
    }

    pre_len = len(ids)

    with torch.no_grad():
        _, tok_logits = model(ids, attention_mask=None,
            rel_ids=None, pos_ids=pos_ids, categories=None,
            pre_len=None) # maybe pre_len
    
    out['input_toks'] += [tokenizer.convert_ids_to_tokens(seq) for seq in ids.cpu().numpy()]
    logits = tok_logits.detach().cpu().numpy()
    out['tok_logits'] += logits.tolist()
    out['tok_probs'] += to_probs(logits, pre_len)

    return out

def test_sentence(model, tokens, pos): 
    # get tokens ids from BERT
    ids = pad([tok2id.get(x, 0) for x in tokens], 0)
    ids = torch.LongTensor(ids)
    ids = ids.unsqueeze(0)
    pos_ids = pad([POS2ID.get(x, POS2ID['<UNK>']) for x in pos], 0)

    model.eval() # constant random seed
    output = run_inference(model, ids, pos_ids) #, tokenizer)
    return output

def changeRange(old_range, new_range, value):
    # given an old range, new range, and value in the old range, 
    # maps it to the new range
    # we will use old_range[0,1] new_range [0,10]
    (old_min, old_max), (new_min, new_max) = old_range, new_range
    return  new_min + ((value - old_min) * (new_max - new_min) / (old_max - old_min))

def output(sentences):
    print("BIAS START")
    results = {}
    results['sentence_results'] = []
    #print('sentences:', sentences)
    #print("New testsentence code!")
    # Takes a list of sentences = [s1, s2, s3]
    # Returns list of tokens and list of corresponding bias scores for each sentence
    #   So, list of lists: 
    #       word_list = [[w1,w2,...wn_1], . . . [w1, w2, ... wn_2]]
    #       bias_list = [[0.1,0.33, ... 0.02], . . .[0.9, 0.002, ... 0.5]]

    # using new models with linguistic features

    model = BertForMultitaskWithFeatures.from_pretrained(
        config, LEXICON_DIRECTORY,
        cls_num_labels=cls_num_labels,
        tok_num_labels=tok_num_labels,
        tok2id=tok2id, 
        lexicon_feature_bits=1)

    # Load model
    saved_model_path = model_save_dir + 'features.ckpt'
    model.load_state_dict(torch.load(saved_model_path, map_location=torch.device("cpu")))

    word_list = []
    pos_list = []
    bias_list = []
    for sentence in sentences:
        sentence_dat = nlp(sentence)
        sentence_pos = [i.pos_ for i in sentence_dat]
        sentence_tokens = [i.text.lower() for i in sentence_dat]
        final_tokens = []
        final_pos = [] 
        for word, pos in zip(sentence_tokens, sentence_pos):
            cur_tok = tokenizer.tokenize(word)
            for c in cur_tok:
                final_tokens.append(c)
                final_pos.append(pos)
        #print(sentence)
        out = test_sentence(model, final_tokens, final_pos) 
        #print("Results:")

        bias_val = out['tok_probs'][0][:len(final_pos)]
        prob_bias = [b[1] for b in bias_val]

        word_list.append(out['input_toks'][0][:len(final_pos)])
        pos_list.append(final_pos)
        bias_list.append(prob_bias)

    scaled_bias_scores = []
    num = 0
    for words, biases, pos in zip(word_list, bias_list, pos_list):
        # Format output string 
        # starts as python dictionary which we will convert to a json string
        outWordsScores = []
        avg_sum = 0

        for word, score, cur_pos in zip(words, biases, pos):
            bias_score = score*10 #changeRange([0,1], [0,10], score)
            avg_sum += bias_score
            if len(word) >= 3 and word[:2] == "##":
                # stuff
                last_word_score = outWordsScores[-1]
                #print(last_word_score, word, score)
                outWordsScores[-1][0] = last_word_score[0] + word[2:]
                outWordsScores[-1][1] = max(last_word_score[1], bias_score)
                if outWordsScores[-1][1] > 4:
                    outWordsScores[-1][3] = wordtype(outWordsScores[-1][0])
                # won't have to change/add POS!
            else:
                if bias_score > 4:
                    outWordsScores.append([word, bias_score, cur_pos, wordtype(word)])
                else:
                    outWordsScores.append([word, bias_score, cur_pos, "NONE"])
        
        max_biased = outWordsScores[0]

        for elem in outWordsScores:
            if elem[1] > max_biased[1]:
                max_biased = elem
        # one of these per sentence
        
        scaled_bias_scores.append(max_biased[1])
        #print("Scaled bias scores: ", scaled_bias_scores)

        #print("max biased and max score:", max_biased, max_score)
        num = num + 1
        s_level_results = {
            "words" : outWordsScores,
            "average": "{:.5f}".format(avg_sum/len(words)),
            "max_biased_word": max_biased[0] + ": " + "{:.5f}".format(max_biased[1]),
            "bias_score":max_biased[1],
            "order":num
        } 

        results['sentence_results'].append(s_level_results)

    # out of for loop...
    # Full article data
    # Sort scaled bias score largest to smallest: 
    scaled_bias_scores.sort(reverse=True)
    upper_bound = int(len(scaled_bias_scores)/2)

    if upper_bound == 0:
        upper_bound = 1

    top_twenty_fifth = scaled_bias_scores[:upper_bound]
    results['article_score'] = statistics.mean(top_twenty_fifth)
    
    return results 