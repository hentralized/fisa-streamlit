import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
import talib
import streamlit.components.v1 as components
import datetime

# 대표 사이트 명
st.title(' 🏦 우리 FISA 증권 🏦')

# Streamlit 제목 설정
st.subheader('💵 실시간 주식 종목 분석')
# 사용자로부터 종목명, 종목코드 또는 티커 입력 받기
ticker_input = st.text_input('🧐 종목코드 또는 종목 티커를 입력하세요:', 'AAPL')

# 주식 데이터를 FinanceDataReader를 통해 가져오기
data = None
tradingview_ticker = ''

# 사용자가 입력한 티커가 숫자형(한국 주식)인 경우
if ticker_input.isdigit():
    ticker = ticker_input  # 숫자형 티커는 한국 주식
    # 예시로, 숫자형 티커를 TradingView에서 지원되는 심볼로 변환 (직접 매핑하거나, 예시 코드로 처리)
    if ticker == "005930":  # 예: 삼성전자의 경우 KRX:005930을 TradingView에서 사용하기
        tradingview_ticker = "KRX:005930"
    else:
        st.warning("이 티커는 TradingView에서 지원되지 않습니다.")
else:
    ticker = ticker_input
    tradingview_ticker = ticker  # 외국 주식 티커 그대로 사용

# 해당 종목에 대한 데이터를 FinanceDataReader에서 가져오기
if tradingview_ticker:
    data = fdr.DataReader(ticker, start='2024-01-01')

# TradingView 차트 삽입
st.subheader('📊 Technical Overview')
if tradingview_ticker:
    tradingview_widget = f"""
    <iframe src="https://www.tradingview.com/widgetembed/?symbol={tradingview_ticker}&theme=dark&style=1&timezone=Asia/Seoul&withdateranges=1&hide_side_toolbar=1&allow_symbol_change=1&save_image=1&studies=[]&locale=kr" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
    """
    components.html(tradingview_widget, height=650)

# 사용자로부터 Bollinger Bands 및 RSI 설정 받기
bollinger_period = st.slider('Bollinger Bands 기간 설정', 10, 50, 20)
rsi_period = st.slider('RSI 기간 설정', 10, 50, 14)

# Bollinger Bands 계산
if data is not None:
    data['upper_band'], data['middle_band'], data['lower_band'] = talib.BBANDS(data['Close'], timeperiod=bollinger_period, nbdevup=2, nbdevdn=2, matype=0)
    # RSI 계산
    data['rsi'] = talib.RSI(data['Close'], timeperiod=rsi_period)

    # 실시간 주가 표시
    st.subheader('💁🏻 실시간 주가')
    st.write(f'현재가: {data.iloc[-1]["Close"]}')
    st.write(f'전날 종가: {data.iloc[-2]["Close"]}')
    st.write(f'최고가: {data["Close"].max()}')
    st.write(f'최저가: {data["Close"].min()}')

    # 과거 데이터 표시
    st.subheader('💁🏻 종목 히스토리')
    st.dataframe(data, width=1200)

    # Bollinger Bands와 RSI 기반 의견
    bollinger_opinion = ''
    rsi_opinion = ''

    # Bollinger Bands 상단/하단 터치 판단
    if data['Close'].iloc[-1] > data['upper_band'].iloc[-1]:
        bollinger_opinion = '하락 가능성 (상단 터치)'
    elif data['Close'].iloc[-1] < data['lower_band'].iloc[-1]:
        bollinger_opinion = '상승 여력 가능성 (하단 터치)'

    # RSI 판단
    if data['rsi'].iloc[-1] > 70:
        rsi_opinion = '과매도 (하락 가능성)'
    elif data['rsi'].iloc[-1] < 30:
        rsi_opinion = '과매도 (상승 여력 가능성)'

    # 종합 분석
    st.subheader('💁🏻 종합 분석 결과')

    st.write(f'현재 주식 가격에 대한 Bollinger Bands 의견: {bollinger_opinion}')
    st.write(f'현재 주식 가격에 대한 RSI 의견: {rsi_opinion}')

    # 매수/매도 및 공매도 데이터 가져오기 함수
    def get_trade_data(ticker):
        data = fdr.DataReader(ticker, start='2024-01-01')
        return data

    # 최근 한달간 매수/매도 및 공매도 데이터 가져오기
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)
    trade_data = get_trade_data(ticker)

    institution_buy = trade_data['Volume'].sum()
    institution_sell = trade_data['Volume'].sum() * 0.5
    individual_buy = trade_data['Volume'].sum() * 0.5
    individual_sell = trade_data['Volume'].sum() * 0.4
    short_selling = trade_data['Volume'].sum() * 0.1

    # 종합 분석
    if institution_buy > institution_sell and individual_buy > individual_sell:
        opinion = '매수 의견'
        opinion_description = '기관과 개인 투자자 모두 최근 한달간 매수량이 매도량을 초과하므로, 해당 종목의 주식 가격 상승 가능성이 높다고 판단됩니다.'
    elif institution_sell > institution_buy and individual_sell > individual_buy:
        opinion = '매도 의견'
        opinion_description = '기관과 개인 투자자 모두 최근 한달간 매도량이 매수량을 초과하므로, 해당 종목의 주식 가격 하락 가능성이 높다고 판단됩니다.'
    else:
        opinion = '중립 의견'
        opinion_description = '기관과 개인 투자자의 매수량과 매도량이 비슷하므로, 해당 종목의 주식 가격이 변동 없이 안정적인 상태일 가능성이 높습니다.'

    # 종합 분석 결과 표시
    st.write(f'기관의 최근 한달간 총 매수량: {institution_buy}')
    st.write(f'기관의 최근 한달간 총 매도량: {institution_sell}')
    st.write(f'개인투자자의 최근 한달간 총 매수량: {individual_buy}')
    st.write(f'개인투자자의 최근 한달간 총 매도량: {individual_sell}')
    st.write(f'공매도 현황: {short_selling}')
    st.write(f'현재 주식 가격에 대한 의견: {opinion}')
    st.write(f'의견 설명: {opinion_description}')
