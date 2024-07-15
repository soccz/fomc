import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# S&P 500 지수 데이터 다운로드
sp500 = yf.download('^GSPC', start='2018-01-01', end='2024-06-12')

# FOMC 발표일 데이터
fomc_dates = [
    '2018-01-31', '2018-03-21', '2018-05-02', '2018-06-13',
    '2018-08-01', '2018-09-26', '2018-11-08', '2018-12-19',
    '2019-01-30', '2019-03-20', '2019-05-01', '2019-06-19',
    '2019-07-31', '2019-09-18', '2019-10-30', '2019-12-11',
    '2020-01-29', '2020-03-03', '2020-03-15', '2020-04-29',
    '2020-06-10', '2020-07-29', '2020-09-16', '2020-11-05',
    '2020-12-16', '2021-01-27', '2021-03-17', '2021-04-28',
    '2021-06-16', '2021-07-28', '2021-09-22', '2021-11-03',
    '2021-12-15', '2022-01-26', '2022-03-16', '2022-05-04',
    '2022-06-15', '2022-07-27', '2022-09-21', '2022-11-02',
    '2022-12-14', '2023-02-01', '2023-03-22', '2023-05-03',
    '2023-06-14', '2023-07-26', '2023-09-20', '2023-11-01',
    '2023-12-13', '2024-01-31', '2024-03-20', '2024-05-01', '2024-06-12'
]
fomc_dates = pd.to_datetime(fomc_dates)

# 발표 전후 1주일을 포함한 데이터 마크
sp500['FOMC_window'] = sp500.index.map(lambda date: any((date >= fomc_date - pd.Timedelta(days=7)) & (date <= fomc_date + pd.Timedelta(days=7)) for fomc_date in fomc_dates))
sp500['Year'] = sp500.index.year

# 발표 전후 1주일 동안의 거래량 변화율 계산 함수
def calculate_volume_change(sp500, fomc_dates):
    volume_changes = []
    for fomc_date in fomc_dates:
        pre_window = sp500.loc[(sp500.index >= fomc_date - pd.Timedelta(days=7)) & (sp500.index < fomc_date)]
        post_window = sp500.loc[(sp500.index > fomc_date) & (sp500.index <= fomc_date + pd.Timedelta(days=7))]
        if not pre_window.empty and not post_window.empty:
            pre_avg_volume = pre_window['Volume'].mean()
            post_avg_volume = post_window['Volume'].mean()
            volume_change = (post_avg_volume - pre_avg_volume) / pre_avg_volume
            volume_changes.append(volume_change)
    return volume_changes

volume_changes = calculate_volume_change(sp500, fomc_dates)

# 변화율의 평균과 표준편차 계산
mean_change = np.mean(volume_changes)
std_change = np.std(volume_changes)

# t-검정 수행
t_stat, p_value = stats.ttest_1samp(volume_changes, 0)

# 결과 출력
print(f"Mean Volume Change: {mean_change}")
print(f"Standard Deviation of Volume Change: {std_change}")
print(f"T-Statistic: {t_stat}")
print(f"P-Value: {p_value}")

# 평균 거래량 비교 시각화
data = {
    'Non-FOMC Days': non_fomc_mean,
    'FOMC Post Day': fomc_post_mean,
    'FOMC Post Week': fomc_post_week_mean
}

names = list(data.keys())
values = list(data.values())

plt.figure(figsize=(10, 6))
plt.bar(names, values, color=['blue', 'orange', 'green'])
plt.title('Average Trading Volume: Non-FOMC Days vs. FOMC Post Days')
plt.xlabel('Category')
plt.ylabel('Average Volume')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# 변화율 시각화
plt.figure(figsize=(10, 6))
plt.hist(volume_changes, bins=20, edgecolor='black', alpha=0.7)
plt.axvline(mean_change, color='r', linestyle='dashed', linewidth=1)
plt.title('Distribution of Volume Changes Around FOMC Announcements')
plt.xlabel('Volume Change')
plt.ylabel('Frequency')
plt.show()
