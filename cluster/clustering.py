import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 데이터 로드 및 전처리
data = pd.read_csv('end2.csv')
data['Date'] = pd.to_datetime(data['Date'])

# FOMC 날짜 리스트
fomc_dates = [
    '2018-01-31 14:00', '2018-03-21 14:00', '2018-05-02 14:00','2018-06-13 14:00', '2018-08-01 14:00', '2018-09-26 14:00', '2018-11-08 14:00', '2018-12-19 14:00',
    '2019-01-30 14:00', '2019-03-20 14:00', '2019-05-01 14:00', '2019-06-19 14:00', '2019-07-31 14:00', '2019-09-18 14:00', '2019-10-30 14:00', '2019-12-11 14:00',
    '2020-01-29 14:00', '2020-03-18 14:00', '2020-04-29 14:00', '2020-06-10 14:00', '2020-07-29 14:00', '2020-09-16 14:00', '2020-11-05 14:00', '2020-12-16 14:00',
    '2021-01-27 14:00', '2021-03-17 14:00', '2021-04-28 14:00', '2021-06-16 14:00', '2021-07-28 14:00', '2021-09-22 14:00', '2021-11-03 14:00', '2021-12-15 14:00',
    '2022-01-26 14:00', '2022-03-16 14:00', '2022-05-04 14:00', '2022-06-15 14:00', '2022-07-27 14:00', '2022-09-21 14:00', '2022-11-02 14:00', '2022-12-14 14:00',
    '2023-02-01 14:00', '2023-03-22 14:00', '2023-05-03 14:00', '2023-06-14 14:00', '2023-07-26 14:00', '2023-09-20 14:00', '2023-11-01 14:00', '2023-12-13 14:00',
    '2024-01-31 14:00', '2024-03-20 14:00', '2024-05-01 14:00', '2024-06-12 14:00'
]

# 문자열을 datetime 형식으로 변환
fomc_dates = [datetime.strptime(date, '%Y-%m-%d %H:%M') for date in fomc_dates]

# 1주일 전과 후의 날짜 범위 설정
date_ranges = [(date - timedelta(days=7), date + timedelta(days=7)) for date in fomc_dates]

# 결과 저장 리스트
results = []

# 각 날짜 범위에 대해 클러스터링 수행
for start_date, end_date in date_ranges:
    mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
    filtered_data = data.loc[mask]

    # 필요한 열만 선택
    selected_columns = [col for col in filtered_data.columns if 'Percent Change' in col or 'Volume' in col]
    filtered_data = filtered_data[selected_columns].dropna()

    # 데이터 스케일링
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(filtered_data)

    # 클러스터링 분석 (K-Means)
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(data_scaled)

    # 클러스터 결과를 데이터프레임에 추가
    filtered_data['Cluster'] = clusters
    filtered_data['FOMC_Date'] = start_date + timedelta(days=7)  # FOMC 날짜 추가

    # 결과 저장
    results.append(filtered_data)

# 모든 결과를 하나의 데이터프레임으로 병합
final_result = pd.concat(results)

# 클러스터링 결과를 CSV 파일로 저장
final_result.to_csv('Clustered_Data_for_Each_FOMC_Date.csv', index=False)

# 결과 시각화
for fomc_date in fomc_dates:
    fomc_data = final_result[final_result['FOMC_Date'] == fomc_date]
    plt.figure(figsize=(10, 7))
    plt.scatter(fomc_data.iloc[:, 0], fomc_data.iloc[:, 1], c=fomc_data['Cluster'], cmap='viridis')
    plt.xlabel('Percent Change (First Stock)')
    plt.ylabel('Volume (First Stock)')
    plt.title(f'Cluster Analysis of Stocks Around FOMC Date: {fomc_date.strftime("%Y-%m-%d")}')
    plt.colorbar(label='Cluster')
    plt.show()
