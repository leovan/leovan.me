# %%
# load libraries
import os
import json
import glob
import pkuseg
import pickle

import numpy as np
import pandas as pd

from tqdm import tqdm

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from gensim import corpora, models

tqdm.pandas()

# %%
# Chinese song lyric
lyrics = []

# data downloaded from https://github.com/liuhuanyong/MusicLyricChatbot

with open('data/music.json', 'r') as f:
    while (line := f.readline()) != '':
        lyric = json.loads(line)
        lyric['geci'] = os.linesep.join(lyric['geci'])
        lyric['id'] = lyric['_id']['$oid']
        del lyric['_id']
        lyrics.append(lyric)

lyrics = pd.DataFrame(lyrics)

# %%
# stopwords
stopwords = set()

# data downloaded from https://github.com/goto456/stopwords

for file in glob.glob('data/stopwords/*.txt'):
    with open(file, 'r') as f:
        while (line := f.readline()) != '':
            stopwords.add(line.strip(os.linesep))

# %%
# segmentation
seg = pkuseg.pkuseg(postag=False)

def segment(text):
    return ' '.join(filter(lambda t: not t in stopwords, seg.cut(text)))

lyrics['seg'] = lyrics['geci'].progress_map(segment)

# %%
# dump lyrics
with open('data/lyrics.pkl', 'wb') as f:
    pickle.dump(lyrics, f)

# %%
# load lyrics
with open('data/lyrics.pkl', 'rb') as f:
    lyrics = pickle.load(f)

# %%
# vocabulary
vocabulary = set()

for seg in lyrics['seg']:
    for token in seg.split(' '):
        vocabulary.add(token)

vocabulary = sorted(list(vocabulary))

print('Vocabulary size: {}'.format(len(vocabulary)))

# %%
# TF-IDF (scikit-learn)
pipe = Pipeline([
    ('count', CountVectorizer(vocabulary=vocabulary)),
    ('tfidf', TfidfTransformer())
]).fit(list(lyrics['seg']))

jaychou_jda = lyrics[(lyrics['singer'] == '周杰伦') & (lyrics['song'] == '简单爱')]
jaychou_jda_tfidf = pipe.transform(jaychou_jda['seg']).toarray()[0]
jaychou_jda_keywords = [vocabulary[idx] for idx in jaychou_jda_tfidf.argsort()[-3:][::-1]]
print(jaychou_jda_keywords)

# %%
# LDA
documents_words = []

for seg in lyrics['seg']:
    documents_words.append(seg.split(' '))

dictionary = corpora.Dictionary(documents_words)
corpus = [dictionary.doc2bow(words) for words in documents_words]

lda = models.ldamodel.LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=6)

documents_topic = []

for idx, document_topics in enumerate(lda.inference(corpus)[0]):
    document_topic = np.argmax(document_topics)
    documents_topic.append(document_topic)

lyrics['topic'] = documents_topic
