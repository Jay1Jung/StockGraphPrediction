import pandas as pd

# CSV 파일 로드
file_path = '/Users/jayjung/Desktop/dataset/sp500_data.csv'  # 파일 경로
data = pd.read_csv(file_path)

# 'Date' 열을 datetime 형식으로 변환 (타임존 제거 포함)
data['Date'] = pd.to_datetime(data['Date'].astype(str).str.replace(r'-\d{2}:\d{2}$', '', regex=True), errors='coerce')

# 연도, 월, 일 분리
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

# 'Close' 열 이름 변경
data = data.rename(columns={'Close': 'Closing price'})

# 필요한 열 선택
processed_data = data[['Year', 'Month', 'Day', 'Closing price']]

# 결과 저장
processed_data.to_csv('/Users/jayjung/Desktop/dataset/processed_sp500_data.csv', index=False)

print("data processed" + "processed as"  + 'processed_sp500_data.csv')