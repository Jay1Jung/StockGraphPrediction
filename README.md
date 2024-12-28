# StockGraphPrediction


기본 아이디어: 주식 초보자를 위한 주식앱
그니까 예를 들어 주식 그래프를 넣었을때, 이게 기간에 따라서 이러한 기간에는 주식 추세가 이렇게 변할것이다. 이거를 학습시키는거지
수치에 따른 정확한 분석이 아니라 그래프에 따른 막연한 분석을 기준으로 함.

이 주식 그래프를 어떻게 학습시키냐면 오로지 이전의 주식 모델을 갖고서만 학습을 진행시킴.
예를 들어 삼성 전자의 그래프를 학습 시킨다고 하면, 다른 그래프와 합쳐서 보는게 아니라 삼성 전자의 경우 그래프 모양이 이럴때, 그래프 모양이 이렇게 변했다를 찾는거임
(이게 충분하지는 않을듯) 근데 내가 생각한건 뭐냐면 우리 같은 개미 투자자들한테 언제 얼마냐 오르는거는 중요한게 아니고, 이게 오를건지 안오를건지 분석해주는 수학적 모델이 필요한거임.

1. 투자 보조 지표 \n
  a. MACD (Moving Average Convergence Divergence) \n
  b. RSI (Relative Strength Index) \n
  c. Stochastic Slow \n
  d. Bollinger band \n
2. TTS 조건 검색


https://www.valley.town/join

https://github.com/msitt/blpapi-python/blob/master/README.md
