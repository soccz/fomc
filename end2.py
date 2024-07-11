import yfinance as yf
import pandas as pd

# 데이터 가져오기 기간 설정
start_date = "2018-01-01"
end_date = "2024-06-22"

# CSV 파일에서 심볼 열을 추출합니다.
file_path = 'nasdaq_tickers.csv'
nasdaq_tickers = pd.read_csv(file_path)
symbols = nasdaq_tickers['symbol']

# 데이터프레임 초기화
df_combined = pd.DataFrame()

# 각 심볼에 대해 데이터 수집 및 퍼센트 변동 계산
for symbol in symbols:
    try:
        # 데이터 다운로드
        df = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        
        # 데이터가 비어있는지 확인
        if df.empty:
            print(f"No data for {symbol}, skipping.")
            continue
        
        # 퍼센트 변동 계산
        df['Percent Change'] = (df['Adj Close'] / df['Adj Close'].iloc[0] - 1) * 100
        
        # 필요한 열만 선택하고, 인덱스 이름 변경
        df = df[['Percent Change', 'Volume']].rename(columns={'Percent Change': f'{symbol} Percent Change', 'Volume': f'{symbol} Volume'})
        
        # 결과를 데이터프레임에 합치기
        if df_combined.empty:
            df_combined = df
        else:
            df_combined = df_combined.join(df)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# CSV 파일로 저장
df_combined.to_csv("end2.csv")

# 데이터프레임 표시
df_combined.head()
