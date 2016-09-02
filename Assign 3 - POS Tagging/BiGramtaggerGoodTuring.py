import math
import nltk
import xml.etree.ElementTree
from collections import Counter

START = "<START>"
END = "<END>"

# function to read the corpus and return all the sentences, tags and words
def read_tagged_corpus(filename):
    
    sentences = []
    tags = []
    words = []
    STW = []
    
    e = xml.etree.ElementTree.parse(filename).getroot()
    for p in e.findall('p'):
        for s in p.findall('s'):
            sentence = []
            tags.append(START)
            sentence.append(('',START))
            for t in s.findall('t'):
                 tag = t.get('pos')
                 word = t.text
                 sentence.append((word, tag))
                 tags.append(tag)
                 words.append(word) 
            tags.append(END)
            sentence.append(('',END))
            sentences.append(sentence) 
    
    STW.append(sentences)
    STW.append(tags)
    STW.append(words)
    return STW

# baseline using NLTK
def most_common_tag(tagged_sentences):
    tags = {}
    for sentence in tagged_sentences:
        for _, tag in sentence:
            tags[tag] = tags.get(tag, 0) + 1
    return max(tags, key=tags.get)

def train_nltk_baseline(tagged_sentences):
    backoff_tagger = nltk.DefaultTagger(most_common_tag(tagged_sentences))
    return nltk.UnigramTagger(tagged_sentences, backoff=backoff_tagger)


    
#bigram tagger code
def lookp_transition(tag1, tag2, tags):
    # estimate transition probabilities
    count = 0.1
    for k in xrange(0, len(tags) - 1):
        if((tags[k] == tag1) and (tags[k+1] == tag2)):
                count += 1
    transition = float(count)/(float(tags.count(tag1))+0.001) #change made here
              
    return transition
    #return the probability tables

def good_turing(pair, all_sentences, count):
    
    wordpair = []
    for sent in all_sentences:
        for wordp in sent:
            wordpair.append(wordp)
            
    wordfreq = dict(Counter(wordpair))
    freq_freq = dict(Counter(Counter(wordpair).values()))
    
    if pair in wordpair: # the frequecny of a word
        r = wordfreq[pair]
    else:
        r = count + 1   
    #print ('r', r)  
    r_1 = r + 1 # the plus one increase of new word
    n_r = freq_freq[r] # frequency of r

    if r_1 in freq_freq: # frequency of r + 1
        n_r1 = freq_freq[r_1]
    else:
        n_r1 = 1
    if r == 0:
        r = count + 1
    else:
        count = float(r_1* n_r1)/float(n_r)
    return count
    
def lookup_emission(word, tag, all_sentences, tags):
    pair = (word , tag)
    count = 0
    tags_count = tags.count(tag)
    
    for sentences in all_sentences:
        count += sentences.count(pair)
        
    count_new = good_turing(pair, all_sentences, count)
    
    emission = float(count_new)/(float(tags_count) + 1)
    
    return emission


def hmm_tag_sentence(tagger_data, sentence, tags):
    # apply the Viterbi algorithm
    end_item = viterbi(tagger_data, sentence, tags)
    tags = retrace(end_item)
    return tags
     # then retrace your steps
 #   tagged_words = retrace(end_item)
    # finally return the list of tagged words
   # return tagged_words
   

def get_possible_tags(all_sentences, word):
    possible_tags = []
    for sentence in all_sentences:
        for tag in sentence:
            if(tag[0] == word):
                #optimize by using if
                if(possible_tags.count(tag[1]) == 0):
                    possible_tags.append(tag[1])
                
    return possible_tags
                
def viterbi(tagger_data, sentence, tags):
    # make a dummy item with a START tag, no predecessor, and log probability 0
    dummy = (START,'', 0)
    curr_list = [ dummy ]
    
    for word in sentence:
        prev_list = curr_list
        curr_list = []
        possible_tags = get_possible_tags(tagger_data, word)
       
        if ((len(possible_tags) == 0) or ((possible_tags[0] == START))):
            possible_tags = set(tags)
        
        for tag in possible_tags:
            best_item = find_best_item(word, tag, prev_list, tagger_data, tags)
            curr_list.append(best_item)
        
       
       
    curr_list.sort(key = lambda x: x[2])
    end_item = (END, curr_list[0], curr_list[0][2]) #create end Dummy here
        
    return end_item
          
    # for each word in the sentence:
    #    previous list = current list
    #    current list = []        
    #    determine the possible tags for this word
    #  
    #    for each tag of the possible tags:
    #         add the highest-scoring item with this tag to the current list

    # end the sequence with a dummy: the highest-scoring item with the tag END
    pass
    
def find_best_item(word, tag, possible_predecessors, tagger_data, tags):    
    emission = lookup_emission(word, tag, tagger_data, tags)
    
    # determine the emission probability: 
    #  the probability that this tag will emit this word
    total = 0
    new_item = (tag, '', -1000)
    for item in possible_predecessors:
        #print item
        total = 0
        total = math.log(emission,2) + math.log(lookp_transition(item[0], tag, tags),2) + item[2]
        if(total > new_item[2]):
            new_item = (tag, item, total)
       
            
    #print new_item
    return new_item
     
    # find the predecessor that gives the highest total log probability,
    #  where the total log probability is the sum of
    #    1) the log probability of the emission,
    #    2) the log probability of the transition from the tag of the 
    #       predecessor to the current tag,
    #    3) the total log probability of the predecessor
    
    # return a new item (tag, best predecessor, best total log probability)
    pass

def retrace(end_item):
    
    tags = []
    item = end_item[1]
    # item = predecessor of end_item
    while( item[0] != START):
        tags.append(item[0])
        item = item[1]
        
    tags.reverse()
    # while the tag of the item isn't START:
    #     add the tag of item to tags
    #     item = predecessor of item
    # reverse the list of tags and return it
    #print tags
    return tags

def test_NLTK_unigramTagger(unigramTagger, testFile):
    words = []
    manualTag = []
    e = xml.etree.ElementTree.parse(testFile).getroot()
    for p in e.findall('p'):
           for s in p.findall('s'):
               for t in s.findall('t'):
                    tag = t.get('pos')
                    word = t.text
                    words.append(word)
                    manualTag.append((word,tag))
    taggedData = unigramTagger.tag(words)
    
    count = sum(i!=j for i,j in zip(taggedData,manualTag))
   # print words[1:10]
   #print manualTag[1:10]
   # print taggedData[1:10]
    print 100 - (float(count)/float(len(taggedData)))*100
    
def test_BigramTagger(fileName,all_sentence, tags):
    sentence = []
    givenTags = []
    bigramTags = []
    
    e = xml.etree.ElementTree.parse(fileName).getroot()
    for p in e.findall('p'):
        for s in p.findall('s'):
           sentence = []
           for t in s.findall('t'):
                tag = t.get('pos')
                word = t.text
                sentence.append(word)
                givenTags.append(tag)
            
        tags = hmm_tag_sentence(all_sentences, sentence, tags)
        for x in tags:
            bigramTags.append(x)
    
    #print tags
    count = sum(i!=j for i,j in zip(bigramTags,givenTags))
    print (float(count)/float(len(bigramTags)))*100


print "Training on small-train.xml"
STW = read_tagged_corpus("small-train.xml")
#sentence = ['Standard','&','Poor',"'s",'Corp.','said','it','placed','the','state','of','Florida',"'s",'double-A-rated','debt','on','its','CreditWatch','list','``','with','negative','implications','.',"''",'']
#testFile = "test_2.xml"
testFile1 = "test_1.xml"
testFile2 = "test_2.xml"

all_sentences = STW[0]
tags = STW[1]
words = STW[2]

unigramTagger = train_nltk_baseline(all_sentences)
print "Efficiency of NLTK Unigram Tagger on test_1.xml"
test_NLTK_unigramTagger(unigramTagger, testFile1)
print "Efficiency of Bigram Tagger on test_1.xml"
test_BigramTagger(testFile1,all_sentences,tags)
#hmm_tag_sentence(all_sentences, sentence, tags)

print "......................................................................................................."
print "Efficiency of NLTK Unigram Tagger on test_2.xml"
test_NLTK_unigramTagger(unigramTagger, testFile2)
print "Efficiency of Bigram Tagger on test_2.xml"
test_BigramTagger(testFile2,all_sentences,tags)


print "......................................................................................................."

print "......................................................................................................."

print "Training on medium-train.xml"
STW = read_tagged_corpus("medium-train.xml")

all_sentences = STW[0]
tags = STW[1]
words = STW[2]

unigramTagger = train_nltk_baseline(all_sentences)
print "Efficiency of NLTK Unigram Tagger on test_1.xml"
test_NLTK_unigramTagger(unigramTagger, testFile1)
print "Efficiency of Bigram Tagger on test_1.xml"
test_BigramTagger(testFile1,all_sentences,tags)

print "......................................................................................................."
print "Efficiency of NLTK Unigram Tagger on test_2.xml"
test_NLTK_unigramTagger(unigramTagger, testFile2)
print "Efficiency of Bigram Tagger on test_2.xml"
test_BigramTagger(testFile2,all_sentences,tags)


#sentence = ['Standard','&','Poor',"'s",'Corp.','said','it','placed','the','state','of','Florida',"'s",'double-A-rated','debt','on','its','CreditWatch','list','``','with','negative','implications','.',"''",'']

#tags = hmm_tag_sentence(all_sentences, sentence, tags)


#emission_prob(all_sentences, tags, words)
# divide the sentences into a training and a test part
# train the bigram tagger
# train the baseline tagger
# evaluate the bigram tagger and the baseline