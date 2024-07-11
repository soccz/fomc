import pandas as pd
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

# 결과 저장 리스트
volatility_results = []

# 각 FOMC 날짜에 대해 변동성 계산
for fomc_date in fomc_dates:
    start_date = fomc_date - timedelta(days=7)
    end_date = fomc_date + timedelta(days=7)
    
    mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
    filtered_data = data.loc[mask]
    
    # 필요한 열만 선택
    selected_columns = [col for col in filtered_data.columns if 'Percent Change' in col]
    filtered_data = filtered_data[['Date'] + selected_columns].dropna()
    
    # FOMC 발표 전후의 변동성 계산
    pre_fomc = filtered_data[filtered_data['Date'] < fomc_date]
    post_fomc = filtered_data[filtered_data['Date'] >= fomc_date]
    
    pre_volatility = pre_fomc[selected_columns].std()
    post_volatility = post_fomc[selected_columns].std()
    
    # 결과 저장
    for col in selected_columns:
        stock_name = col.replace(' Percent Change', '')
        volatility_results.append({
            'Stock_Name': stock_name,
            'FOMC_Date': fomc_date,
            'Pre_Volatility': pre_volatility[col],
            'Post_Volatility': post_volatility[col]
        })

# 결과를 데이터프레임으로 변환
volatility_df = pd.DataFrame(volatility_results)

# 결과를 CSV 파일로 저장
volatility_df.to_csv('Volatility_Analysis.csv', index=False)
