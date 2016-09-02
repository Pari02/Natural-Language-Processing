# Assignment 3: Natural Language Processing
# Author: Parikshita Tripathi
# Date: 10/26/2015

from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn
from itertools import product
from collections import Counter

# tokenize_data function takes the sentence, tokenize and tag it 
# and return only words with tag as "NN"
def tokenize_data(sentence):
    token = word_tokenize(sentence)
    data_tags = pos_tag(token)
    data_nouns = [word for word,pos in data_tags if pos in ('NN', 'NNP')]
    
    for w, p in data_tags:
        if p == 'NNS':
            if wn.synsets(w) == []:
                wrd  = w.rstrip('s')
                if wn.synsets(wrd) != []:
                    data_nouns.append(wrd)
        
    words = [w.lower() for w in data_nouns]
    return words
    
# chain_gen function calls tokenize_data and creates chain 
# by compairing wup_similarity
def chain_gen(sentence):
    words = tokenize_data(sentence)
    lex_chain = []    
    
    for i, word in enumerate(words):
        chain = []
        word_count = dict(Counter(words))    
        
        for j in xrange(i+1, len(words)):
            # avoiding comparison of the word to itself
            if (i != j):
                item1 = words[i] + "(" + str(word_count[words[i]]) + ")"
                item2 = words[j] + "(" + str(word_count[words[j]]) + ")"
                
                # genrating synsets of the consecutive words
                if (words[i] != words[j]):
                    syn1 = wn.synsets(words[i])
                    syn2 = wn.synsets(words[j])
                    
                    # compairing the synsets using wordnet.wup_similarity
                    for s1, s2 in product(syn1, syn2):
                        w = max((wn.wup_similarity(s1, s2) or 0) for s1, s2 in product(syn1, syn2))
    
                if item2 not in chain:
                        if (w >= 0.8) and (item2 not in chain):
                                chain.append(item2)
                        if (w < 0.8) and (item1 not in chain):
                            chain.append(item1)
        lex_chain.append(chain)
                
    return lex_chain
 
# improves redundancy of the chains
def lexical_chains(sentence):
    lex_chain = chain_gen(sentence)
    
    # loop to remove empty sublist
    for l in lex_chain:
        if l == []:
            lex_chain.remove(l)
 
    # removes duplicate sublists
    for i, c in enumerate(lex_chain):
        for j in xrange(i+1, len(lex_chain)):
            if j < len(lex_chain):
                if (lex_chain[i] == lex_chain[j]) :
                    lex_chain.pop(j) 
                if (list(set(lex_chain[i]).union(lex_chain[j]) == lex_chain[i])) or (list(set(lex_chain[i]).union(lex_chain[j]) == lex_chain[j])):
                    lex_chain = list(set(lex_chain[i]).union(lex_chain[j]))
                    lex_chain.pop(j)
                else:
                    lex_chain                

    # prints the final output
    for i, l in enumerate(lex_chain):
        print "Chain", i+1, ":", l
    

#sentence = "I like beer. Miller just launched a new pilsner. But, because I'm a beer snob, I'm only going to drink pretentious Belgian ale."
sentence = open('testFile1.txt')
file = sentence.read()
lexical_chains(file)
#lexical_chains(sentence)  