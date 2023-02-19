# Arabic_Sentiment_Analysis

<div align="center">
<img src="./image/README/1676823077790.png" style="width:600px;" alt="Cover">
</div>
<div align="center">
(generated using <a href="https://midjourney.com/home/">MidJourney</a>)
</div>
<h1 align="center">
  Arabic Sentiment Analysis
</h1>

# Overview

A Natural Language Processing model that Analyzes Arabic tweets (with arbitrary dialects) and classifies them based on stance (positive, negative or neutral) and category (news, rumors, advice, unrelated, ..etc).

# Built With

<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Python_logo_01.svg/640px-Python_logo_01.svg.png" alt="Python" style="height: 60px">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1200px-Scikit_learn_logo_small.svg.png" alt="SK learn" style="height: 60px">

<img src="https://user-images.githubusercontent.com/67586773/105040771-43887300-5a88-11eb-9f01-bee100b9ef22.png" alt="Numpy" style="height: 60px">

<img src="https://avatars.githubusercontent.com/u/45758208?s=280&v=4" alt="Camel Tools" style="height: 60px">

<img src="https://cdn-images-1.medium.com/max/1200/1*iDQvKoz7gGHc6YXqvqWWZQ.png" alt="TensorFlow" style="height: 60px">

<img src="https://img-blog.csdnimg.cn/e8664fbfb5cc48e9a45b98d0b905959d.png" alt="Pandas" style="height: 60px">

</div>


# Project Pipeline

` <image/> `

## 1. Methodology

### 1.1 Data Preprocessing
Simple investigation revealed duplicate tweets in the data set that have different classes, we solved this as follows:
- For a single group of duplicate tweets, we replaced them with a single instance and assign to it the top frequent class in such group.

After that we proceed to the data preprocessing step which is done on 3 levels

1. Cleaning Text:
  Using regex and simple filteration code, we managed to do the following:
    | Processing             | Example          |
    | -------                |  ------          |
    | Remove line break tags | `<LF>` ,  `<CR>` |
    | Reduce consecutive duplicate letters to only 2 | "سمعليكووووووو" => "سمعليكوو |
    | Remove URLs and mentions| `https://btly.blabla` ,  `@USER` |
    | Remove hashtag sign | `#هيئة_الصحة_العالمية` <= `هيئة_الصحة_العالمية` |
    | Remove numbers, brackets, and qutoes  |     |
    | Remove english letters | `USER` |
    | Remove abbreviations  | `أ.د محمد => محمد`|
    | Replace _ and - with space | `هيئة_الصحة-العالمية` => `هيئة الصحة العالمية` |
    | Dediacterize Text | `لَقَاحُ مَرَضِ كَوَّرُونَا` => `لقاح مرض كورونا` |
    
2. Tokenizing:
  With the help of camel-tools, we were able to do the following:
    - Detect dialect of the tweet, `we used this information in the next two points` .
    - Perform lemmatization.
    - Perform tokenization.
3. Normalizing Characters:
    - Normalize alef and ya'
    <br>
    
    | Replacement   | character|
    | ------------- |:-------------:|
    | ا    | أ ,  إ , ا , آ |
    | ى     | ى , ي , ئ      |
    
    - Replace emoji with equivalent text `😂 -> face_tearing_with_joy`
### 1.2 Feature Extraction
We have extracted the following features to be used for classification:

1-TF-IDF
   
   Have extracted the Term Frequency-Inverse Term Frequency measure for unigrams, bigrams, trigrams, a combination of unigrams and bigrams, and a combination of unigrams and trigrams using `sklearn.feature_extraction.text.TfidfVectorizer` 

2- BOW
   
Represented the corpus as a Bag of Words using `sklearn.feature_extraction.text.CountVectorizer`
    
3- Dialect
- We thought that there could be a correlation between if the dialect was MSA or not and with the category being from a more formal source like “Info news”, “plans”
- Used camel tools dialect detector to predict the dialect and used it as an additional feature
- Did not have a significant effect
    
4- Word Embeddings

We have also used FastText word embeddings to feed the RNN and LSTM models
### 1.3 Building Models

## 2 Results
