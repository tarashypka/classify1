### Classify romanian language with Python


##### Solution 1 - The *lazy* one

Use stopwords count as features. Since stopwords are usually very frequent 
within the text, a wealth dictionaries of stopwords could be prepared to easily
choose between the languages.

Having nX as count of X-language stopwords and nY as count of Y-language
stopwords for text T, one can construct a distance metric that will take
into account both nX+nY and distance from the line nX=nY


```
D = |nX-nY| / sqrt(2) / (nX+nY+1)
```


Drawbacks: does not generalize well on the very short texts.

##### Solution 2


##### Environment setup

```
$ export PROJNAME=classify1 PROJPATH=$(pwd)
$ conda env create --file=$PROJPATH/config/ENVIRONMENT
$ mkdir -p $ANACONDA_HOME/envs/$PROJNAME/etc/conda/activate.d
$ ln -s $PROJPATH/config/env_vars.sh $ANACONDA_HOME/envs/$PROJNAME/etc/conda/activate.d/
$ source activate $PROJNAME
$ unzip ./data/raw_text_ro.zip -d ./data
$ cp ./data/stopwords/romanian $HOME/nltk_data/corpora/stopwords/
```

##### Dependencies

Anaconda (Python 3.5.2) environment with

```
numpy          1.12.0    py36_0
pandas         0.19.2    np112py36_1
scikit-learn   0.18.1    np112py36_1
matplotlib     2.0.0     np112py36_0
nltk           3.2.2     py36_0
```


##### Notes

Stopwords for romanian language were fetched from [here](http://www.ranks.nl/stopwords/romanian).
