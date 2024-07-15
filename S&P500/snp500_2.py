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

# FOMC 발표일 이후의 거래량 데이터 추출
fomc_post_volume = sp500.loc[sp500.index.isin(fomc_dates + pd.Timedelta(days=1))]['Volume']
fomc_post_week_volume = sp500.loc[sp500.index.map(lambda date: any((date > fomc_date) & (date <= fomc_date + pd.Timedelta(days=7)) for fomc_date in fomc_dates))]['Volume']

# 전체 주식 거래량 데이터 (FOMC 발표일 전후 제외)
non_fomc_volume = sp500.loc[~sp500.index.isin(fomc_dates) & ~sp500.index.isin(fomc_dates + pd.Timedelta(days=1)) & ~sp500.index.map(lambda date: any((date > fomc_date) & (date <= fomc_date + pd.Timedelta(days=7)) for fomc_date in fomc_dates))]['Volume']

# 평균 거래량 계산
fomc_post_mean = fomc_post_volume.mean()
fomc_post_week_mean = fomc_post_week_volume.mean()
non_fomc_mean = non_fomc_volume.mean()

# t-검정 수행 (FOMC 발표 이후 하루 vs 비 FOMC 기간)
t_stat_post, p_value_post = stats.ttest_ind(fomc_post_volume, non_fomc_volume, equal_var=False)
# t-검정 수행 (FOMC 발표 이후 일주일 vs 비 FOMC 기간)
t_stat_post_week, p_value_post_week = stats.ttest_ind(fomc_post_week_volume, non_fomc_volume, equal_var=False)

# 결과 출력
print(f"FOMC Post Mean Volume: {fomc_post_mean}")
print(f"FOMC Post Week Mean Volume: {fomc_post_week_mean}")
print(f"Non-FOMC Mean Volume: {non_fomc_mean}")
print(f"T-Statistic (Post): {t_stat_post}")
print(f"P-Value (Post): {p_value_post}")
print(f"T-Statistic (Post Week): {t_stat_post_week}")
print(f"P-Value (Post Week): {p_value_post_week}")

# 시각화
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
