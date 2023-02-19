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

![piepline](https://user-images.githubusercontent.com/69261710/219968758-c80ff8be-e18f-4f3d-b8f2-7fa45b406028.png)


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

| Classical Models | Sequence Models  | Transformer-Based Models |
| ----             |  ----            | -----                    |
| Multinomial Naive Base | RNN  | MarBERT |
| SVM | LSTM  | AraBERT|
| Random Forest | | |

- SVM hyperparameter tuning

We used GridSearchCV sklearn function for hyperparameter tuning with the following search space:

| Parameter | Possible Values |
| -----     |   ------        |
| C         |   [0.1, 1, 10]  |
| Gamma     |   [0.1, 1]      |
| Kernel    | ['Sigmoid', 'rbf', 'linear', 'poly'] |
| Tol       | [0.001, 0.0001] |

- AraBert Training Arguments

| Argument | Value |
| -----    | ----  |
| learning_rate |  1e-4|
| optimizer | Adam Optimizer|
| adam_epsilon  | 1e-8 |
| batch size | 64 |
| epochs  | 5 |
| metric  | macro F1 |

- MarBert Training Arguments

| Argument | Value |
| -----    | ----  |
| learning_rate |  2e-06|
| optimizer | Adam Optimizer|
| adam_epsilon  | 2e-06|
| batch size | 32 |
| epochs  | 5 |
| metric  | macro F1 |




## 2 Results

Here we highlight some of the approaches and combinations and their results on the given data. It is worth mentioning that both the training and testing datasets had a lot of misclassifications.

For all the approaches, the different output options of the preprocessing steps were tried and we found that they had a very minor impact on the results. For instance, the difference between using the dialect detection and not using it was always about 0.01 in the F1 score. the same goes for keeping the emojis and digits in the text or not.

The main metric used to evaluate the models is the F1 score.

### 2.1 Stance Classification

That is, over the 3 classes: positive, negative and neutral.

| Approach   | Accuracy | Precision | Recall | **F1 Score** |
| ------------- |:-------------:|:-------------:|:-------------:|:-------------:|
| Classical Models (with TF-IDF):               |______|______|______|______|
| **Random Forest (TF-IDF - no SMOTE)**         | 0.80 | 0.65 | 0.37 | 0.37 |
| **Multinomial Naive Bayes (TF-IDF - SMOTE)**  | 0.81 | 0.60 | 0.57 | 0.59 |
| **SVM (TF-IDF - SMOTE, Sigmoid Kernel)**      | 0.82 | 0.62 | 0.61 | 0.61 |
| Sequential Models (with FastText):            |______|______|______|______|
| **LSTM (FastText Embeddings)**                | 0.79 | 0.35 | 0.33 | 0.30 |
| **RNN (FastText Embeddings)**                 | 0.76 | 0.47 | 0.41 | 0.40 |
| Transformer-based Models:                     |______|______|______|______|
| **MarBERT**                                   | 0.83 | 0.69 | 0.60 | **0.63** |
| **araBERT**                                   | 0.83 | 0.63 | 0.62 | **0.63** |


Note: Precision, Recall and F1 Score are calculated using the macro average method.

### 2.2 Category Classification

That is, over the 10 classes, news, celebrities, plan, request, rumor, advice, restriction, personal, unrelated and others.

| Approach   | Accuracy | Precision | Recall | **F1 Score** |
| ------------- |:-------------:|:-------------:|:-------------:|:-------------:|
| Classical Models (with TF-IDF):               |______|______|______|______|
| **Random Forest (TF-IDF - no SMOTE)**         | 0.58 | 0.34 | 0.17 | 0.18 |
| **Multinomial Naive Bayes (TF-IDF - SMOTE)**  | 0.62 | 0.44 | 0.36 | **0.39** |
| **SVM (TF-IDF - SMOTE, Sigmoid Kernel)**      | 0.64 | 0.47 | 0.37 | **0.40** |
| Sequential Models (with FastText):            |______|______|______|______|
| **LSTM (FastText Embeddings)**                | 0.51 | 0.05 | 0.10 | 0.07 |
| **RNN (FastText Embeddings)**                 | 0.60 | 0.17 | 0.18 | 0.17 |
| Transformer-based Models:                     |______|______|______|______|
| **MarBERT**                                   | 0.69 | 0.41 | 0.35 | 0.37 |
| **araBERT**                                   | 0.68 | 0.41 | 0.36 | 0.38 |


Note: Precision, Recall and F1 Score are calculated using the macro average method.

## 3 Conclusions & Future work

- Transformer-based models and Classical models with TF-IDF both worked surprisingly well on the stance problem.

- using SMOTE balancing on the TF-IDF embeddings of the training data almost always improved the results.

- Our preprocessing produced a variety of options (removing vs. keeping emojis and digits, translating them to text, appending the dialect as a feature, etc.). But, upon testing them, we found that all of them had very minor effects on the results.

- Our straightforward usage of Sequential models (LSTM and RNN) did not perform well. It might be worthwhile to try and play around with the hyperparameters and other details of the models to see if we can get better results. Since we did not have a lot of time to invest in them.

## 4 References

- [A review of sentiment analysis research in Arabic language](https://www.sciencedirect.com/science/article/abs/pii/S0167739X19311537)
- [Preprocessing Arabic text on social media](https://www.sciencedirect.com/science/article/pii/S2405844021002966)
- [arcovidvac: A Twitter Dataset for Arabic COVID-19 Vaccine Stance Classification](https://arxiv.org/pdf/2201.06496.pdf)
- [AraStance: A Multi-Country and Multi-Domain Dataset of Arabic Stance Detection for Fact Checking](https://aclanthology.org/2021.nlp4if-1.9.pdf)
- [A review of sentiment analysis research in Arabic language](https://www.sciencedirect.com/science/article/abs/pii/S0167739X19311537)
- [Camel Tools](https://camel-tools.readthedocs.io/)
