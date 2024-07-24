import requests
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

# NLTK 데이터 다운로드
nltk.download('punkt')
nltk.download('stopwords')

# Bing 뉴스 검색 API 키
api_key = '4378fc2ec4bf44baa1cb38792cdd2333'
query = 'FOMC rate cut'

# Bing 뉴스 검색 API 요청 URL 구성
bing_url = f'https://api.bing.microsoft.com/v7.0/news/search?q={query}&freshness=Month&count=100&offset=0&mkt=en-US&safeSearch=Moderate'

# 요청 헤더 설정
headers = {
    'Ocp-Apim-Subscription-Key': api_key
}

# API 요청 보내기
response = requests.get(bing_url, headers=headers)

# 응답 상태 코드 확인
if response.status_code == 200:
    news_data = response.json()
    articles = news_data.get('value', [])
else:
    print(f"Error: API request failed with status code {response.status_code}")
    articles = []

# 불용어 설정
stop_words = set(stopwords.words('english'))

# 텍스트 전처리 함수
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # 다중 공백 제거
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # 특수 문자 제거
    tokens = word_tokenize(text.lower())  # 토큰화 및 소문자 변환
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]  # 불용어 제거 및 단어 길이 필터링
    return tokens

# 문장에서 FOMC와 함께 나타나는 경우만 필터링하는 함수
def filter_sentences_with_fomc_and_cut(text):
    sentences = sent_tokenize(text)
    filtered_tokens = []
    for sentence in sentences:
        if 'fomc' in sentence.lower() and 'cut' in sentence.lower():
            filtered_tokens.extend(preprocess_text(sentence))
    return filtered_tokens

# 전체 텍스트를 처리하고 FOMC와 cut이 함께 나타나는 경우만 포함
all_tokens = []
for article in articles:
    if 'description' in article and article['description']:
        tokens = filter_sentences_with_fomc_and_cut(article['description'])
        all_tokens.extend(tokens)

# 전체 단어 빈도 계산
word_freq = Counter(all_tokens)

# 상위 20개의 빈도 높은 단어 출력
top_20_words = word_freq.most_common(20)
print("Top 20 Most Frequent Words in FOMC News Articles:", top_20_words)

# 인상, 동결, 인하 키워드 설정
rate_hike_keywords = ['raise', 'hike', 'increase']
rate_hold_keywords = ['hold', 'unchanged', 'maintain']
rate_cut_keywords = ['cut', 'lower', 'decrease', 'reduce']

# 매파 및 비둘기파 키워드 설정
hawkish_keywords = ['hawkish'] + rate_hike_keywords
dovish_keywords = ['dovish'] + rate_cut_keywords

# 키워드 빈도 계산 함수
def keyword_frequency(tokens, keywords):
    keyword_freq = Counter(tokens)
    return {word: keyword_freq[word] for word in keywords if word in keyword_freq}

# 인상 키워드 빈도 계산
hike_freq = keyword_frequency(all_tokens, rate_hike_keywords)

# 동결 키워드 빈도 계산
hold_freq = keyword_frequency(all_tokens, rate_hold_keywords)

# 인하 키워드 빈도 계산
cut_freq = keyword_frequency(all_tokens, rate_cut_keywords)

# 매파 키워드 빈도 계산
hawkish_freq = keyword_frequency(all_tokens, hawkish_keywords)

# 비둘기파 키워드 빈도 계산
dovish_freq = keyword_frequency(all_tokens, dovish_keywords)

# 결과 출력
print("Rate Hike Keywords Frequency:", hike_freq)
print("Rate Hold Keywords Frequency:", hold_freq)
print("Rate Cut Keywords Frequency:", cut_freq)
print("Hawkish Keywords Frequency:", hawkish_freq)
print("Dovish Keywords Frequency:", dovish_freq)

# 시각화를 위한 데이터 준비
hike_df = pd.DataFrame(list(hike_freq.items()), columns=['Keyword', 'Frequency'])
hold_df = pd.DataFrame(list(hold_freq.items()), columns=['Keyword', 'Frequency'])
cut_df = pd.DataFrame(list(cut_freq.items()), columns=['Keyword', 'Frequency'])
hawkish_df = pd.DataFrame(list(hawkish_freq.items()), columns=['Keyword', 'Frequency'])
dovish_df = pd.DataFrame(list(dovish_freq.items()), columns=['Keyword', 'Frequency'])

# Seaborn 스타일 설정
sns.set(style="whitegrid")

# 하나의 그림에 여러 그래프를 배치
fig, axs = plt.subplots(3, 2, figsize=(20, 18), sharey=True)

# 전체 키워드 빈도 시각화
top_words_df = pd.DataFrame(top_20_words, columns=['Keyword', 'Frequency'])
sns.barplot(x='Keyword', y='Frequency', data=top_words_df, palette='viridis', ax=axs[0, 0], legend=False)
axs[0, 0].set_title('Top 20 Most Frequent Words in FOMC News Articles')
axs[0, 0].set_xticks(range(len(top_words_df)))
axs[0, 0].set_xticklabels(axs[0, 0].get_xticklabels(), rotation=45)

# 인상 키워드 빈도 시각화
sns.barplot(x='Keyword', y='Frequency', data=hike_df, palette='Reds', ax=axs[0, 1], legend=False)
axs[0, 1].set_title('Frequency of Rate Hike Keywords in FOMC News Articles')
axs[0, 1].set_xticks(range(len(hike_df)))
axs[0, 1].set_xticklabels(axs[0, 1].get_xticklabels(), rotation=45)

# 동결 키워드 빈도 시각화
sns.barplot(x='Keyword', y='Frequency', data=hold_df, palette='Greens', ax=axs[1, 0], legend=False)
axs[1, 0].set_title('Frequency of Rate Hold Keywords in FOMC News Articles')
axs[1, 0].set_xticks(range(len(hold_df)))
axs[1, 0].set_xticklabels(axs[1, 0].get_xticklabels(), rotation=45)

# 인하 키워드 빈도 시각화
sns.barplot(x='Keyword', y='Frequency', data=cut_df, palette='Blues', ax=axs[1, 1], legend=False)
axs[1, 1].set_title('Frequency of Rate Cut Keywords in FOMC News Articles')
axs[1, 1].set_xticks(range(len(cut_df)))
axs[1, 1].set_xticklabels(axs[1, 1].get_xticklabels(), rotation=45)

# 매파 키워드 빈도 시각화
sns.barplot(x='Keyword', y='Frequency', data=hawkish_df, palette='Reds', ax=axs[2, 0], legend=False)
axs[2, 0].set_title('Frequency of Hawkish Keywords in FOMC News Articles')
axs[2, 0].set_xticks(range(len(hawkish_df)))
axs[2, 0].set_xticklabels(axs[2, 0].get_xticklabels(), rotation=45)

# 비둘기파 키워드 빈도 시각화
sns.barplot(x='Keyword', y='Frequency', data=dovish_df, palette='Blues', ax=axs[2, 1], legend=False)
axs[2, 1].set_title('Frequency of Dovish Keywords in FOMC News Articles')
axs[2, 1].set_xticks(range(len(dovish_df)))
axs[2, 1].set_xticklabels(axs[2, 1].get_xticklabels(), rotation=45)

# 전체 레이아웃 조정
plt.tight_layout()
plt.savefig('fomc_keywords_analysis.png')
plt.show()

# Word Cloud 추가
from wordcloud import WordCloud

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of FOMC News Articles')
plt.savefig('fomc_wordcloud.png')
plt.show()
