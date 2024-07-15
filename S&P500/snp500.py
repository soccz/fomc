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

# FOMC 윈도우와 비 FOMC 윈도우의 거래량 데이터 분리
fomc_window_volume = sp500[sp500['FOMC_window']]['Volume']
non_fomc_window_volume = sp500[~sp500['FOMC_window']]['Volume']

# 두 그룹의 평균 거래량 계산
fomc_window_mean = fomc_window_volume.mean()
non_fomc_window_mean = non_fomc_window_volume.mean()

# t-검정 수행
t_stat, p_value = stats.ttest_ind(fomc_window_volume, non_fomc_window_volume, equal_var=False)

# 결과 출력
print(f"FOMC Window Mean Volume: {fomc_window_mean}")
print(f"Non-FOMC Window Mean Volume: {non_fomc_window_mean}")
print(f"T-Statistic: {t_stat}")
print(f"P-Value: {p_value}")

# 시각화
volume_summary = sp500.groupby(['Year', 'FOMC_window'])['Volume'].mean().unstack()
volume_summary.plot(kind='bar', figsize=(14, 7), width=0.8)
plt.title('Average Trading Volume During FOMC Window vs. Non-FOMC Window by Year')
plt.ylabel('Average Volume')
plt.xlabel('Year')
plt.xticks(rotation=45)
plt.legend(['Non-FOMC Window', 'FOMC Window'])
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
