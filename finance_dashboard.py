# finance_dashboard.py
import streamlit as st
import yfinance as yf
import pandas as pd

# 🎯 나의 자산 입력 (여기 숫자만 바꾸면 됩니다!)
stock_holdings = {
    'AAPL': 10,  # Apple 주식 10주
    'TSLA': 5,   # Tesla 5주
    'VOO': 3     # 뮤추얼펀드(ETF) 3주
}
cash_balance = 1500.00  # 현금
savings_balance = 5000.00  # 예금

# 📈 주식 가격 가져오기 (1일 간격)
@st.cache_data(ttl=60)
def fetch_prices(tickers):
    data = {}
    for ticker in tickers:
        price = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
        data[ticker] = round(price, 2)
    return data

st.title("📊 내 자산 현황 대시보드")

tickers = list(stock_holdings.keys())
prices = fetch_prices(tickers)

# 💰 자산 계산
asset_data = []
total = 0

for ticker, shares in stock_holdings.items():
    value = shares * prices[ticker]
    asset_data.append({'Asset': ticker, 'Value': value})
    total += value

asset_data.append({'Asset': 'Savings', 'Value': savings_balance})
asset_data.append({'Asset': 'Cash', 'Value': cash_balance})
total += savings_balance + cash_balance

# 📋 표로 보기
df = pd.DataFrame(asset_data)
df['% Allocation'] = round(df['Value'] / total * 100, 2)

st.subheader("📋 자산 목록")
st.dataframe(df)

# 🧁 파이 차트로 보기
st.subheader("📈 자산 비율 (파이차트)")
st.plotly_chart(
    {
        "data": [{
            "labels": df["Asset"],
            "values": df["Value"],
            "type": "pie",
            "hole": 0.4
        }],
        "layout": {"title": "자산 분포"}
    }
)
