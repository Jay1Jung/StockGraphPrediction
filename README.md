# StockGraphPrediction


기본 아이디어: 주식 초보자를 위한 주식앱
그니까 예를 들어 주식 그래프를 넣었을때, 이게 기간에 따라서 이러한 기간에는 주식 추세가 이렇게 변할것이다. 이거를 학습시키는거지
수치에 따른 정확한 분석이 아니라 그래프에 따른 막연한 분석을 기준으로 함.

이 주식 그래프를 어떻게 학습시키냐면 오로지 이전의 주식 모델을 갖고서만 학습을 진행시킴.
예를 들어 삼성 전자의 그래프를 학습 시킨다고 하면, 다른 그래프와 합쳐서 보는게 아니라 삼성 전자의 경우 그래프 모양이 이럴때, 그래프 모양이 이렇게 변했다를 찾는거임
(이게 충분하지는 않을듯) 근데 내가 생각한건 뭐냐면 우리 같은 개미 투자자들한테 언제 얼마냐 오르는거는 중요한게 아니고, 이게 오를건지 안오를건지 분석해주는 수학적 모델이 필요한거임.

S&P 500 주식들 중에서 산업별로 크게 9개의 섹터로 나누어서 산업별 현황이랑 앞으로의 추세를 볼때 큰 그림으로 봄
이 9개의 섹터들은 미국의 경제지표에 따라서 특정한 연관성을 찾을 수 있음 예를 들면 CPI, PPI, 금리 같은 것들이 9개의 섹터 중 특정 섹터에 영향을 끼침

우리가 할거는 이런 지수들이랑 산업별 주식들이 어떻게 연관되어서 움직이는지 regression line을 만들어서 앞으로의 경제 지수 발표들이 그 섹터들에 어떻게 가격으로 반영되는지 예측하는 모델을 만드는거

주가만 보고 모델을 만들기에는 예측하지 못하는 영역들이 있고 그 영역들도 주가에 반영됨 그래서 이 부분들의 영향을 어떻게 배제를 할건지, 배제를 안한다면 어떻게 반영을 할건지도 고려를 해야함

경제 지수 
1. 신규 실업수당청구건수 - New Jobless Claims
2. S&P 글로벌 제조업 PMI *
3. S&P 글로벌 서비스업 PMI *
4. S&P 글로벌 합성 PMI
5. 연준 기준금리 결정 *
6. 실질 GDP 성장률 *  https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
7. 근원 PCE 가격지수
10. EIA 원유재고
12. 신규주택판매
13. 컨퍼런스보드 소비자신뢰지수
14. 미국 국채경매
15. 기존주택판매
18. 실업률 * https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=AE-US&name_desc=false
19. CPI 상승률 * https://data.worldbank.org/indicator/FP.CPI.TOTL?locations=US
20. PPI 상승률 
21. 경기선행지수 * https://fred.stlouisfed.org/series/USSLIND

1. 투자 보조 지표 \n
  a. MACD (Moving Average Convergence Divergence) \n
  b. RSI (Relative Strength Index) \n
  c. Stochastic Slow \n
  d. Bollinger band \n
2. TTS 조건 검색


https://www.valley.town/join

https://github.com/msitt/blpapi-python/blob/master/README.md
