**Personality Prediction Using Machine Learning - README**

**Project Overview**<br>
This project aims to predict an individual's personality type using machine learning algorithms based on the Myers-Briggs Type Indicator (MBTI). The MBTI model categorizes personalities into 16 types based on four dimensions: Introvert (I) vs. Extrovert (E), Sensation (S) vs. Intuition (N), Thinking (T) vs. Feeling (F), and Perceiving (P) vs. Judging (J). We use various machine learning algorithms, including K-Nearest Neighbors (KNN), Logistic Regression, and XGBoost, to develop a predictive model. The dataset for this project is sourced from Kaggle and contains social media posts tagged with MBTI personality types.

**Key Features**

**Notifications**<br>
The "Notifications" feature keeps users informed about any updates, advancements, or supplementary details related to the ongoing personality assessment process.

**Voice-Based Text Detection**<br>
The "Voice-Based Text Detection" feature allows users to interact with the system using spoken language or voice commands. The system converts spoken words into text for personality analysis, offering a convenient alternative to typing.

**Project Phases**

**A. Data Analysis and Pre-Processing**<br>

**Data Import and Initial Analysis:**<br>
Import the dataset from Kaggle, which includes attributes like "Type" (MBTI personality type) and "Posts" (last 50 social media posts of each user).
Analyze the dataset to identify missing values, data types, dataset size, and attribute dependencies.
Examine the proportions of each personality type in the dataset.<br>
**Data Cleaning:**<br>
Remove non-words, punctuation, repeated letters, and stop-words.
Selectively remove words that might confuse the machine learning model.
Perform lemmatization to reduce words to their root forms (e.g., "running" becomes "run").
Convert MBTI personality types to binary form (e.g., ENFP becomes [1,0,0,1]).
Tokenize the text to pick the most frequently used words.

**B. Feature Engineering**<br>

**Transform Pre-Processed Data:**<br>
Convert the cleaned text data into features that the machine learning model can understand.
Use techniques like TF-IDF (Term Frequency-Inverse Document Frequency) to vectorize the text data.

**C. Model Training and Testing**<br>

**Algorithm Selection:**<br>
Consider various algorithms for text classification, including Random Forest, Stochastic Gradient Descent, K-Nearest Neighbor (KNN), Logistic Regression, and XGBoost.<br>
**Model Training:**<br>
Train models on the pre-processed and vectorized text data.
Use a 70:30 train-test split ratio for evaluation.<br>
**Model Evaluation:**<br>
Evaluate model performance using metrics such as accuracy and other relevant performance metrics.
Based on these metrics, select Logistic Regression as the primary model for this project.

**Dependencies**

**Python 3.x**: The main programming language used for this project.<br>
**Pandas**: For data manipulation and analysis, particularly useful for handling tabular data and time series.<br>
**Numpy**: For numerical computations and handling arrays.<br>
**Scikit-learn**: For machine learning tasks, including model fitting, data preprocessing, and evaluation.<br>
**NLTK (Natural Language Toolkit)**: For natural language processing tasks such as tokenization, stemming, and lemmatization.<br>
**XGBoost**: For efficient and accurate gradient boosting.<br>
**Flask**: For developing the web application interface.<br>
**SpeechRecognition**: For converting spoken language into text for analysis.<br>


**Conclusion**<br>

Personality prediction using machine learning can provide valuable insights into individual behaviors, preferences, and interactions. This project leverages the MBTI model and various machine learning algorithms to develop a robust personality prediction system. By analyzing social media posts, the system can accurately predict personality types, aiding in applications ranging from mental health assessments to human resource decisions.
