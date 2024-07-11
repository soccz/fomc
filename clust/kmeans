import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# 데이터 로드 및 전처리
data = pd.read_csv('end2.csv')
data['Date'] = pd.to_datetime(data['Date'])

# 엘보우 방법을 통한 최적의 클러스터 수 찾기
selected_columns = [col for col in data.columns if 'Percent Change' in col or 'Volume' in col]
filtered_data = data[selected_columns].dropna()
scaler = StandardScaler()
data_scaled = scaler.fit_transform(filtered_data)

wcss = []
for k in range(1, 15):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 15), wcss, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method for Optimal k')
plt.show()

# 실루엣 분석을 통한 최적의 클러스터 수 찾기
silhouette_scores = []
for k in range(2, 15):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    score = silhouette_score(data_scaled, kmeans.labels_)
    silhouette_scores.append(score)

plt.plot(range(2, 15), silhouette_scores, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Analysis for Optimal k')
plt.show()
