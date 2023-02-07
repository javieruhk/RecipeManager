import json
from operator import is_, xor

import nltk
from nltk import Tree
from flair.data import Sentence
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.models import MultiTagger


def process_tree(node):
    result_p_t = []

    if type(node) == Tree:
        for sub_node in node:
            data, neg_data, _, _, _ = process_tree_node(sub_node, [], [], [], False, 0)
            if len(data)>0 or len(neg_data)>0:
                result_p_t.append({'pos': data, 'neg': neg_data})
    else:
        data, neg_data, _, _, _ = process_tree_node(node, [], [], [], False, 0)
        if len(data) > 0 or len(neg_data) > 0:
            res.append({'pos': data, 'neg': neg_data})
    return result_p_t


def process_tree_node(node, data, neg_data, cur_el, is_negation, level):
    # simple NP
    if type(node) == tuple:
        word, category = node
        if category in ('PP', 'JJ') or category.startswith('N'): # NN, NPP, NP
            contains_free = False
            if '-free' in word:
                is_negation = not is_negation
                word = word.replace('-free', '')
                cur_el.append(dict(term='free', probable_type='MODIFIER', category='JJ', negating=is_negation))
            elif 'free' in word:
                is_negation = not is_negation
                cur_el.append(dict(term='free', probable_type='MODIFIER', category='JJ', negating=is_negation))
            if not word == '':
                probable_type = 'INGREDIENT'
                if contains_free:
                    category = 'NN_F'
                elif category in ('JJ'):
                    probable_type = 'MODIFIER'
                cur_el.append(dict(term=word, probable_type=probable_type, category=category, negated=is_negation))
        elif category.startswith('V'):
            cur_el.append(dict(term=word, probable_type='METHOD', category=category, negated=is_negation))
        elif category in ('IN', 'RB', 'CD', 'TO'):
            is_negation = xor(parse_conjuctions(node), is_negation)
            cur_el.append(dict(term=word, probable_type='MODIFIER', category=category, negating=is_negation))
        else:  # , . DT
            is_negation = xor(parse_conjuctions(node), is_negation)

        return data, neg_data, cur_el, is_negation, level
    # subtree NP
    if type(node) == Tree:
        for sub_node in node:
            data_r, neg_data_r, cur_el, is_negation, _ = process_tree_node(sub_node, data, neg_data, cur_el, is_negation, level + 1)
        if level == 1 and len(cur_el) > 0:
            if is_negation:
                neg_data_r.append(cur_el.copy())
            else:
                data_r.append(cur_el.copy())
            cur_el = []
            is_negation = False

        return data_r, neg_data_r, cur_el, is_negation, level


def parse_conjuctions(node):
    word, category = node
    return word.lower() in ( 'without', 'not', 'no', 'negative', 'free', '-free', 'zero', '0') # 'nor',


if __name__ == '__main__':

    text = "Flaky pastry, filled with chocolate cream"
    #text = "Flaky pastry, filled without chocolate cream"
    #text = "Pasta, filled with meat, boiled in water, zero no sugar"
    #text = "Breakfast cereal with wheat and corn and no sugar-free"
    text = "Sugar-free Breakfast cereal boiled, canned in water and cheese. Adding three teaspoons of George Washington in the mix, after mix it for eighty five minutes"
    #text = 'Pasta, filled with meat, boiled'
    #text = 'Pasta, filled with meat mix, cooked'
    #text = 'Meat loaf with cheese, vegetables or other'
    #text = 'Omelette with mushrooms'
    #text = 'My pretty old dog'
    #text = 'Gratin of Belgian endives with ham and cheese sauce'
    #text = 'Kebab with yoghurt'

    flair_pos_tagger = MultiTagger.load(['pos', 'ner'])

    sent_text = nltk.sent_tokenize(text)  # this gives us a list of sentences
    for sentence in sent_text:

        nltk_tokens = nltk.word_tokenize(sentence)
        nltk_tagged_sentence = nltk.pos_tag(nltk_tokens)
        print(nltk_tagged_sentence)

        # load tagger for POS and NER
        flair_sentence = Sentence(sentence)
        # predict with both models
        flair_pos_tagger.predict(flair_sentence)
        print(flair_sentence)
        flair_tagged_sentence = []
        # for storing pos tagged string#
        flair_pos_tagger.predict(flair_sentence)
        i=0
        if len(flair_sentence.get_labels('pos')) > 0:
            for token in flair_sentence.tokens:
                if token.text == nltk_tagged_sentence[i][0]:
                    label = token.get_labels('pos')[0]
                    if not label.value.__eq__(nltk_tagged_sentence[i][1]):
                        print("%s : NLTK '%s', FLAIR '%s' : %2.4f" % (token.text, nltk_tagged_sentence[i][1], label.value, label.score))
                        nltk_tagged_sentence[i] = (nltk_tagged_sentence[i][0], label.value)
                i=i+1
        else:
            print('No POS Tags detected')
        if len(flair_sentence.get_labels('ner'))>0:
            for label in flair_sentence.get_labels('ner'):
                print(label)
        else:
            print('No NER Tags detected')

        '''
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        grammar = r"""
                  NP: {<DT|PP\$>?<JJ>*<NN.*>+}          # Chunk sequences of DT, JJ, NN
                  PP: {<IN|RB|CD|TO>+<NP>}               # Chunk prepositions followed by NP
                  V: {<VB.*>}
                  VP: {<V><NP|PP|CLAUSE>+}     # Chunk verbs and their arguments
                  CLAUSE: {<NP><V|PP>+}           # Chunk NP, VP
                  """  # CC ?
        '''
        grammar = r"""
          NP: {<DT|CD|PRP\$>*<JJ>*<PRP|NN.*>+}          # Chunk sequences of DT, JJ, NN
          PP: {<IN|TO>+<NP>}               # Chunk prepositions followed by NP   -- RB|    <CC>?<NP>?
          V: {<VB.*>}
          CLAUSE: {<NP|V>*<NP|LNP|PP>*}     # Chunk verbs and their arguments  
          """ # CC ? CLAUSE: {<NP><V|PP>+}           # Chunk NP, VP
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(nltk_tagged_sentence)

        result.draw()

        # inspect ['without' (IN), 'not' (RB), 'no' (DT), 'negative' (JJ), 'free' (JJ), '-free' (JJ), 'zero' (CD), 0 (CD)]
        res = process_tree(result)
        print(res)
        #sentence = nltk.corpus.treebank.tagged_sents()[22]
        print(nltk.ne_chunk(nltk_tagged_sentence, binary=True))

        # Opening JSON file
        #f = open('input json/not perfect matches.json')
        '''
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        print(data)
        # Iterating through the json
        # list
        
        i = 0
        for k in data:
            print(k)
            i = i + 1
    
        print(i)
        
        # Closing file
        f.close()
        '''