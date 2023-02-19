# Arabic_Sentiment_Analysis




## Project Pipeline



## 1 Methodology

### 1.1 Data Preprocessing
Simple investigation revealed duplicate tweets in the data set that have different classes, we solved this as follows:
- for a single group of duplicate tweets, we replaced them with a single instance and assign to it the top frequent class in such group.
After that we proceed to the data preprocessing step which is done on 3 levels
* Cleaning Text:
  Using regex and simple filteration code, we managed to do the following:
    - Remove line break tags: `<LF>` , `<CR>`
    - Reduce consecutive duplicate letters to only 2: "سمعليكووووووو" => "سمعليكوو
    - Remove URLs and mentions
    - Remove numbers
* Tokenizing:
  With the help of camel-tools, we were able to do the following:
    - Detect dialect of the tweet, `we used this information in the next two points` .
    - Perform lemmatization.
    - Perform tokenization.
* Normalizing Characters:
    - Normalize alef and ya'
    <br>
    
    | Replacement   | character|
    | ------------- |:-------------:|
    | ا    | أ ,  إ , ا , آ |
    | ى     | ى , ي , ئ      |
    
    - Replace emoji with equivalent text `😂 -> face_tearing_with_joy`
### 1.2 Feature Extraction

### 1.3 Building Models

## 2 Results
