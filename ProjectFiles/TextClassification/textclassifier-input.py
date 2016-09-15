import nltk
import string
import os
import io
import pandas as pd
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from nltk.corpus import stopwords

# set parameters
candidates = ["romney", "obama"]
pathname = "./speeches/"


# customized tokenizr for cleaning texts
def mytokenizer(corpus):
    punctuations = list(string.punctuation)
    stop_words = set(stopwords.words('english'))
    punctuations.append("''")
    tokens = nltk.word_tokenize(corpus)
    tokens = [tk.strip("".join(punctuations)) for tk in tokens if tk not in punctuations]
    tokens = [tk.lower() for tk in tokens]
    tokens = [tk.strip() for tk in tokens]
    tokens = [tk for tk in tokens if tk not in stop_words]
    return tokens


# create text document matrix
def generateTDM(candidates):
    vect = CountVectorizer(tokenizer=mytokenizer, min_df=0.7)
    all_docs = []
    # CHANGED: Store all the docs first before vectorizing
    for i, cand in enumerate(candidates):
        docs = []
        doc_names = []
        for filename in os.listdir(pathname + cand):
            fd = io.open(os.path.join(pathname + cand, filename), encoding='utf-8', errors='ignore')  
            file_text = fd.read()
            docs.append(file_text)
            doc_names.append(filename)
       	all_docs.append(docs)

    # CHANGED: Fitting all the docs before transforming
    vect.fit(list(itertools.chain.from_iterable(all_docs)))
    
    # CHANGED: Transforming the candidates, each separetly 
    tdm = []
    for i, cand in enumerate(candidates):
        cand_tdm = vect.transform(all_docs[i])
        cand_tdm = pd.DataFrame(cand_tdm.toarray(), columns=vect.get_feature_names())
        tdm.append(cand_tdm)
    return tdm, vect
    
# apply function
# CHANGED: Change the function to talk all the candidates at the same time, to unify the vectorizer
tdm, vect = generateTDM(candidates)

# create target(response)
y = []
for i in range(len(tdm)):
    y += tdm[i].shape[0]*[i]

# stack texts(create feature)
X = pd.concat(tdm, ignore_index=True)
# set NA values to 0
X.fillna(value=0, inplace=True)

# split X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=1)

# instantiate the model (with the default parameters)
knn = KNeighborsClassifier()

# train the model using X_train
knn.fit(X_train, y_train)

# make class predictions for X_test
y_pred_class = knn.predict(X_test)

# calculate accuracy of class predictions
print ( metrics.accuracy_score(y_test, y_pred_class))

# print the confusion matrix
print ( metrics.confusion_matrix(y_test, y_pred_class))

# CHANGED: The new part of predicting the new speech
file_speech = io.open(os.path.join(pathname, "new_speech.txt"), encoding='utf-8', errors='ignore')  
new_speech = file_speech.read()

new_tdm = vect.transform([new_speech])
transformed_speech = pd.DataFrame(new_tdm.toarray(), columns=vect.get_feature_names())
transformed_speech.fillna(value=0, inplace=True)

print (candidates[knn.predict(new_tdm.toarray())[0]])
