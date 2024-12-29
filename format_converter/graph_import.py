import granville_first_case as fc
import yfinance as yf
import matplotlib.pyplot as plt

# 데이터 가져오기
data = yf.download("AAPL", start="2023-01-01", end="2024-01-01")
data["MA_50"] = data["Close"].rolling(window=50).mean()


plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='종가', color='blue')
plt.plot(data['MA_50'], label='50일 이동평균선', color='orange')

plt.title('그랜빌의 법칙 첫 번째 조건')
plt.xlabel('날짜')
plt.ylabel('주가 ($)')
plt.legend()
plt.grid()
plt.show()

# 함수 호출
#print(data["Close"])
print(data["MA_50"])
#buy_signals = fc.granville_first_rule(data["Close"], data["MA_50"])
#print("Buy Signals:", buy_signals)