### Classify romanian language with Python


#### Input data

Input data is list of ~100,000 vaccancies written in different languages.
Most of them are romanian, english or mix of those.
Data were split into train (~90,000) and test (10,000) examples.

Labeled test examples could be found [here](https://drive.google.com/open?id=0BwH_IQu68lAbZDR0eG11bm9vUGs).


#### Solution 1 - The *lazy* one

Use stopwords count as features. Since stopwords are usually very frequent 
within the text, a wealth dictionaries of stopwords could be prepared to easily
choose between the languages.

Having nX as count of X-language stopwords and nY as count of Y-language
stopwords for text T, one can construct a distance metric that will take
into account both nX+nY and distance from the line nX=nY


```
D = |nX-nY| / sqrt(2) / (nX+nY+1)
```

Stopwords for romanian language are [here](http://www.ranks.nl/stopwords/romanian).


*Drawbacks*: does not generalize well on short examples.


#### Solution 2 - *KMeans*

Features normalization played an important role in finding
the appropriate clusters.

Predicted train examples could be found [here](https://drive.google.com/open?id=0BwH_IQu68lAbMGREdFVsa1RoV2c).

*Drawbacks*: does not generalize well on short examples.


#### Solution 3 - Chinese Whispers

To be done.


#### Performance

Accuracy for 5500 of test documents with lazy solution: 0.990  
Accuracy for 5500 of test documents with KMeans solution: 0.995


#### Environment setup

```
$ export PROJNAME=classify1 PROJPATH=$(pwd)
$ conda env create --file=$PROJPATH/config/ENVIRONMENT
$ mkdir -p $ANACONDA_HOME/envs/$PROJNAME/etc/conda/activate.d
$ ln -s $PROJPATH/config/env_vars.sh $ANACONDA_HOME/envs/$PROJNAME/etc/conda/activate.d/
$ source activate $PROJNAME
$ unzip ./data/raw_text_ro.zip -d ./data
$ cp ./data/stopwords/romanian $HOME/nltk_data/corpora/stopwords/
```

#### Dependencies

Anaconda (Python 3.5.2) environment with

```
gensim         0.13.4.1  np112py36_0
numpy          1.12.0    py36_0
scikit-learn   0.18.1    np112py36_1
matplotlib     2.0.0     np112py36_0
```
