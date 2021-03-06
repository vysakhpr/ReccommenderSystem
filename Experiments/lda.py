import gensim
import logging
import os
import numpy as np
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
num_topics=20 			
alpha=0.01
eta=0.01

stoplist = set(stopwords.words('english'))
fpath = os.path.join("preprocessed.txt")
with open(fpath, "r") as script:
	filelines =script.readlines()

documents = filelines  
np.random.seed(42)
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
dictionary = corpora.Dictionary(texts)
dictionary.save('dictionary.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, alpha=alpha, eta = eta,update_every=1, chunksize=100, passes=10, iterations=1000)
lda.save('lda.model')
#print lda.print_topics(10)
lda=models.ldamodel.LdaModel.load('lda.model')
i=0
fp=open("processed_features.txt","w")
for d in documents:
	bow = dictionary.doc2bow(d.split())
	#print bow
	x=""
	x=x+str(i)
	for l in lda.get_document_topics(bow, minimum_probability=0, minimum_phi_value=None, per_word_topics=False):
		x=x+","+str(l[1])
	i=i+1
	fp.write(x+"\n")
fp.close()


#print lda.print_topics(20)
#docTopicProbMat = lda[corpus]
#for topic in docTopicProbMat:
#      print(topic)


#topicWordProbMat = lda.print_topics(20)
#print topicWordProbMat

#fp=open("output.txt","a")
#fp.write("CONF: TOPICS\t ALPHA\t ETA\n =============================================================== \n"+str(num_topics)+"\t"+str(alpha)+"\t"+str(eta)+"\n =============================================================== \n")
#fp.close()
