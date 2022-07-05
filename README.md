# What Makes A TED Talk Popular?
### Team: Ruixi Wang, Xin Zhao, Yuhui Ren, Zhizheng Li
### Instructor: Prof. Rong Liu

## 1.Objectives and Expected Contributions

The main objective of our work is to investigate what make a TED Talk popular within the following aspects:
- Is there any relation between speech duration and speech popularity? How does the duration affect the popularity?
- Which aspects are people interested in? Which tags for a TED Talk can make it have more views? Does number of tags for a TED talks affect the views?
- Which speakers are popular?
- Are there any specific words can make a topic gain more click? How about the sentiment for these words?
- How does the speech description affect view?
- What’s emotions do general topics share? Is there any extraordinary topic that has different emotion pattern in hand?
- Whether there are some peculiar emotion patterns which tend to attract more viewers?

We expect our work can make following contributions:
- This work can provide insights about what makes a TED Talk popular. Through sentiment analysis, we could provide tips for speakers about how to create the topics and descriptions that can inspire people’s interest most.
- We can give advice about which aspects’ speeches should be made more.

## 2. Web Mining

TEDtalks_data_collection.py runs for collecting 4329 rows of data
	output data: ted_talks_data.csv
	for testing purpose, users can reduce range() in line 60 to run faster

TEDtalks_data_preprocessing.py runs for data preprocessing.
	input data: ted_talks_data.csv
	output data: ted_talks_data_clean.csv
		     ted_talks_data_1000.csv

TEDtalks_EDA_analysis.ipynb:
- NLP pipline, including tokenization, lemmatization, remove stop_word, computing tfidf matrix, and vectorize docs
- Topic recommendation: Provide keywords return top 10 related topics
- Visualization and analysis

## 3. Topic Clustering Model

By using cosine distance for initializing clustering model, we artificially set 10 numbers of clusters. 
After getting words with top 20 tf-idf weight in the centroid, we name 10 clusters by the top 20 words in each cluster. 
Ten clusters perfectly include the most popular tags of topics. That is, the most frequent words(Top 20) in each cluster are able to represent the majority of the cluster.

## 4. Sentiment Mining

### 4.1 nltk.sentiment.vader approach

we combined topics column and description column in dataset 1 as one topic+desc column, because we wanted to combine all text information together in each speech, so that we only need to do the analysis once. 
By using the SentimentIntensityAnalyzer in nltk.sentiment.vader, it is easy to get sentiment metrices which derived from rating the inputted text. 
The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). 
In our experiment, we extracted only compound score instead of the positive, neutral and negative score, to see the general emotion of each speech.

### 4.2 Textacy approach

To validate our finding more accurately, we tried another library in python, which is textacy, to detect the sentiment in TED Talks. 
Textacy is a Python library for performing higher-level natural language processing (NLP) tasks, built on the high-performance spaCy library. 
It can detect DepecheMood (AFRAID, AMUSED, ANGRY, ANNOYED, DONT_CARE, HAPPY, INSPIRED, SAD) and directly give scores of the moods as well, DepecheMood is a high-quality and high-coverage emotion lexicon for English and Italian text, mapping individual terms to their emotional valences.

## 5. Sentiment Clustering Model

In order to seek more patterns among sentiment, topics, popularity, and so on, we generate a sentiment score dataset for sentiment clustering analysis.
Each row represents each talk, and each column represents each emotion. Unlike topic clustering, sentiment clustering cannot use tfidf vectorizer to look for the vector for each talk. Accordingly, the sequential pattern of sentiment score for each talk is the better way to calculate the pair wise distance. Basically, the idea is that we consider the sequence of sentiment scores as a pattern we rely on to find the pair wise distance for each talk. Thus, the package fastdtw is introduced to implement the idea of sequential pattern pair wise distance. The package takes two series of data as input and use Euclidean distance to find distance between patterns.
Once we found the distance for each talk, we can reshape the distance to better fit in the clustering model. This project uses Gaussian Mixture Models to fit in the calculated dtm. This model uses the lowest BIC score to find out that the best GMM model is 9 components with spherical covariance type. Eventually, this model uses manifold embedding method to visualize the sentiment clustering model.

## 6. Sentiment Clustering Analysis

Word Cloud and Visualization of sentiment clustering model

## 7. Logistic Regression Model

The objective of this task is to detect if the ted talk is popular. For the sake of simplicity, we say how emotion can affect the popularity of Ted Talk. So, the task is to find the
relationship between the emotion and the popularity. The more emotion shows that people have more strong emotion for the Ted Talk. The first LR is with comments and the second one is without comments
Formally, given a training sample of tweets and labels, the higher of views (times that the video had been watched) shows that the video is more popular. I used the mean value of views to decide whether the ted talk is popular. If the views are higher than the mean value represent that the ted talk is popular, and the value will return to 1, otherwise, return to 0 your objective is to predict the labels on the test data.

From both models above we can see that positive emotion like happy, inspired really help the popularity of Ted talk, and the negative emotion like sad and afraid are negative relate to the popularity. With the comments, the model will be more accurate. So I believe with the comments number will better to predict the popularity of the ted talks.

## 8. Conclusion

Tags does affect the views, the most popular tags are science, culture, health, design, global, etc. In some words, speak duration affects the popularity: 1 minute to around 33 minutes are the favorable length of talks. The top 5 popular speakers are Sire Ken Robinson, James Veitch, Amy Cuddy Simon Sinek and Bren Brown.
As for the conclusion about sentiment mining, we can conclude that usually positive sentiment is more than negative sentiment. More specifically, emotion of INSPIRED usually dominates most speeches, emotion of AFRAID and SAD are the least emotion I speeches. Moreover, among many of the speeches, there are some AMUSED and SAD emotions, which could be speakers’ tricks to attract audience’s attention.
Sentiment clustering is a powerful tool to gather many interesting insights about the relationship between topics, popularity, and sentiment patterns. We learned that Topics related to human, people, life, work, and story share similar sentiment patterns and belong to the most popular cluster. We also can get some interesting result such as topics related to photographer, and war virtually share similar sentiment patterns. From the models above we can see that the positive emotion in the Ted Talk like happy, inspired will definitely improve the popularity of the Ted Talk. And the negative emotion like sad afraid is negative relate to the popularity. The number of comments will also improve the popularity.
