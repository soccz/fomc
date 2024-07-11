import pandas as pd
import yfinance as yf
import requests
from io import StringIO

# 나스닥 종목 리스트 가져오기
url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
response = requests.get(url)
data = StringIO(response.text)

# 종목 리스트를 데이터프레임으로 변환
df = pd.read_csv(data, sep="|")

# 종목 심볼 리스트 추출
symbols = df['Symbol'].tolist()

# 데이터를 저장할 리스트 초기화
stock_data = []

# 각 종목의 데이터를 가져와 리스트에 추가
for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        stock_data.append(info)
        print(f"데이터 수집 완료: {symbol}")
    except Exception as e:
        print(f"데이터 수집 실패: {symbol}, 오류: {str(e)}")

# 데이터프레임으로 변환
result_df = pd.DataFrame(stock_data)

# CSV 파일로 저장
result_df.to_csv('nasdaq_tickers.csv', index=False)

print("모든 나스닥 종목 데이터가 CSV 파일로 저장되었습니다.")
