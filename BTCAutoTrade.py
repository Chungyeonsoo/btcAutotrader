#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import time
import pyupbit
import datetime

access = "jXgPJ1jbfQBzFIhHoFUh9ZIue2Qx3xbfxK8xAtz8"          # 본인 값으로 변경
secret = "doJrpomV6oxsnlP2mNjkIOHklt7NNBFuHjpakaBv"   

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes240", count=2)
    target_price = df.iloc[0]['low'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_limit_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes240", count=2)
    limit_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return limit_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes240", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
btc_total = float(upbit.get_balances()[1]['balance']) * float(upbit.get_balances()[1]['avg_buy_price'])
doge_total = float(upbit.get_balances()[2]['balance']) * float(upbit.get_balances()[2]['avg_buy_price'])
balance_sum = btc_total + doge_total + float(upbit.get_balances()[0]['balance'])
                                     
btc_per = btc_total / balance_sum
doge_per = doge_total / balance_sum

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        start_time = get_start_time("KRW-DOGE")
        end_time = start_time + datetime.timedelta(hours=4)

        if start_time < now < (end_time - datetime.timedelta(seconds=10)):
            target_price = get_target_price("KRW-BTC", 0.01)
            current_price = get_current_price("KRW-BTC")
            limit_price = get_limit_price("KRW-BTC", 0.5)
            
            target_price_DOGE = get_target_price("KRW-DOGE", 0.01)
            current_price_DOGE = get_current_price("KRW-DOGE")
            limit_price_DOGE = get_limit_price("KRW-DOGE", 0.5)
            
            if target_price < current_price < limit_price and btc_per < 0.49:
                amount_krw = balance_sum * 0.49 - btc_total
                if amount_krw > 5000:
                    upbit.buy_market_order("KRW-BTC", amount_krw*0.9995)
                    print('buy BTC')
                    btc_total = float(upbit.get_balances()[1]['balance']) * float(upbit.get_balances()[1]['avg_buy_price'])
                    doge_total = float(upbit.get_balances()[2]['balance']) * float(upbit.get_balances()[2]['avg_buy_price'])
                    balance_sum = btc_total + doge_total + float(upbit.get_balances()[0]['balance'])
                                     
                    btc_per = btc_total / balance_sum
                    doge_per = doge_total / balance_sum
                    
            if target_price_DOGE < current_price_DOGE < limit_price_DOGE and doge_per < 0.49:
                amount_krw = balance_sum * 0.49 - doge_total
                if amount_krw > 5000:
                    upbit.buy_market_order("KRW-DOGE", amount_krw*0.9995)
                    print('buy DOGE')
                    btc_total = float(upbit.get_balances()[1]['balance']) * float(upbit.get_balances()[1]['avg_buy_price'])
                    doge_total = float(upbit.get_balances()[2]['balance']) * float(upbit.get_balances()[2]['avg_buy_price'])
                    balance_sum = btc_total + doge_total + float(upbit.get_balances()[0]['balance'])
                                     
                    btc_per = btc_total / balance_sum
                    doge_per = doge_total / balance_sum

                    
        else:
            btc = get_balance("BTC")
            doge = get_balance("DOGE")
            
            if btc > 0.00001:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                print('BTC sold')
            if doge > 1:
                upbit.sell_market_order("KRW-DOGE", DOGE*0.9995)
                print('DOGE sold')
                
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)  
