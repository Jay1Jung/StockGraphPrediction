import pandas as pd



def granville_first_rule(cp: pd.Series, ma:pd.Series):
    # cp means closing price and ma means moving avg line

    # 이평선이 하락하다가 상승할때 주가가 이평선을 넘는 경우
    print(cp.head())
    print(ma.head())

    buy_signals = []


    for i in range(2,len(ma)) :

        ma_dec_inc = ma[i-1] < ma[i] and ma[i-2] > ma[i-1]

        cross_point = cp[i] > ma[i] and cp[i-1] <= ma[i-1]


        if ma_dec_inc and cross_point:
            buy_signals.append(cp.index[i])
    
    return buy_signals