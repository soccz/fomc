import pandas as pd
from datetime import datetime, timedelta

# 주식 데이터 CSV 파일 경로
stock_data_file = 'end2.csv'  # 실제 경로를 여기에 입력

# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv(stock_data_file)

# 날짜 데이터를 datetime 형식으로 변환
df['Date'] = pd.to_datetime(df['Date'])

# FOMC 일정
fomc_dates = [
    '2018-01-31 14:00', '2018-03-21 14:00', '2018-05-02 14:00','2018-06-13 14:00', '2018-08-01 14:00', '2018-09-26 14:00', '2018-11-08 14:00', '2018-12-19 14:00',
    '2019-01-30 14:00', '2019-03-20 14:00', '2019-05-01 14:00', '2019-06-19 14:00', '2019-07-31 14:00', '2019-09-18 14:00', '2019-10-30 14:00', '2019-12-11 14:00',
    '2020-01-29 14:00', '2020-03-18 14:00', '2020-04-29 14:00', '2020-06-10 14:00', '2020-07-29 14:00', '2020-09-16 14:00', '2020-11-05 14:00', '2020-12-16 14:00',
    '2021-01-27 14:00', '2021-03-17 14:00', '2021-04-28 14:00', '2021-06-16 14:00', '2021-07-28 14:00', '2021-09-22 14:00', '2021-11-03 14:00', '2021-12-15 14:00',
    '2022-01-26 14:00', '2022-03-16 14:00', '2022-05-04 14:00', '2022-06-15 14:00', '2022-07-27 14:00', '2022-09-21 14:00', '2022-11-02 14:00', '2022-12-14 14:00',
    '2023-02-01 14:00', '2023-03-22 14:00', '2023-05-03 14:00', '2023-06-14 14:00', '2023-07-26 14:00', '2023-09-20 14:00', '2023-11-01 14:00', '2023-12-13 14:00',
    '2024-01-31 14:00', '2024-03-20 14:00', '2024-05-01 14:00', '2024-06-12 14:00'
]

# FOMC 날짜를 datetime 형식으로 변환
fomc_dates = [datetime.strptime(date_str, '%Y-%m-%d %H:%M') if ' ' in date_str else datetime.strptime(date_str, '%Y-%m-%d') for date_str in fomc_dates]

# 최종 결과를 저장할 데이터프레임 초기화
final_df = pd.DataFrame()

# 각 FOMC 날짜에 대해 처리
for fomc_date in fomc_dates:
    # FOMC 날짜 기준으로 1주일 전, 1주일 후의 데이터 구하기
    start_date = fomc_date - timedelta(days=7)
    end_date = fomc_date + timedelta(days=7)
    
    # 해당 기간의 데이터 필터링
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_data = df.loc[mask]
    
    # 거래량 평균 top10 구하기
    volume_columns = [col for col in filtered_data.columns if 'Volume' in col]
    volume_data = filtered_data[volume_columns]
    avg_volumes = volume_data.mean().nlargest(10).reset_index()
    avg_volumes.columns = ['Ticker', 'Average_Volume']
    avg_volumes['FOMC_Date'] = fomc_date
    
    # 주식 가격 변동이 큰 top10 구하기
    percent_change_columns = [col for col in filtered_data.columns if 'Percent Change' in col]
    percent_change_data = filtered_data[percent_change_columns]
    sum_percent_changes = percent_change_data.abs().sum().nlargest(10).reset_index()
    sum_percent_changes.columns = ['Ticker', 'Total_Price_Variation']
    sum_percent_changes['FOMC_Date'] = fomc_date
    
    # 데이터를 최종 데이터프레임에 추가
    final_df = pd.concat([final_df, avg_volumes, sum_percent_changes])

# 날짜별로 정렬
final_df = final_df.sort_values(by='FOMC_Date')

# 최종 데이터를 CSV 파일로 저장
final_output_file = 'fomc_analysis_results.csv'
final_df.to_csv(final_output_file, index=False)
print(f"Saved final analysis results to {final_output_file}")
