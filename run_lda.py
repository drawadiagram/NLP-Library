# implement LDA with a helper function to flatten text files

import numpy as np
import lda
import lda.datasets # remove later
import matplotlib.pyplot as plt

# Create a Document-Term Matrix (DTM)
# Example pulls one from Reuters dataset.
# X = lda.datasets.load_reuters()

# Create a tuple of corpus words to count.
# vocab = lda.datasets.load_reuters_vocab()

# Create a tuple of document titles, or some other meaningful index.
# titles = lda.datasets.load_reuters_titles()

# Separate train/test
# X_train = X[10:]
# X_test = X[:10]
# titles_test = titles[:10]

# Fit model
model = lda.LDA(n_topics=17, n_iter=1500, random_state=1)
model.fit(my_freq)

topic_word = model.topic_word_ # or model.components_
n_top_words = 8

for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(my_vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))


doc_topic = model.doc_topic_
for i in range(len(my_titles)):
    print('{} (top topic: {})'.format(my_titles[i], doc_topic[i].argmax()))

# doc_topic_test = model.transform(X_test)
# for title, topics in zip(titles_test, doc_topic_test):
#     print('{} (top topic: {})'.format(title, topics.argmax()))

plt.plot(model.loglikelihoods_[5:])
plt.show()
