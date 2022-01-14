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

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        start_time = get_start_time("KRW-DOGE")
        end_time = start_time + datetime.timedelta(hours=4)

        if start_time < now < (end_time - datetime.timedelta(seconds=10)):
            target_price = get_target_price("KRW-BTC", 0.005)
            current_price = get_current_price("KRW-BTC")
            limit_price = get_limit_price("KRW-BTC", 0.5)
            
            target_price_DOGE = get_target_price("KRW-DOGE", 0.005)
            current_price = get_current_price("KRW-DOGE")
            limit_price = get_limit_price("KRW-DOGE", 0.5)
            
            if target_price < current_price < limit_price:
                krw = get_balance("KRW")
                dist_krw = (krw * 0.5) - 100
                left_krw = krw - dist_krw - 100
                if dist_krw > 5000:
                    upbit.buy_market_order("KRW-BTC", dist_krw*0.9995)
                    print('buy BTC')
                if left_krw > 5000:
                    upbit.buy_market_order("KRW-DOGE", left_krw*0.9995)
                    print('buy DOGE')
                    
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
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-DOGE")
        end_time = start_time + datetime.timedelta(hours=4)

        if start_time < now < (end_time - datetime.timedelta(seconds=10)):
            target_price = get_target_price("KRW-DOGE", 0.005)
            current_price = get_current_price("KRW-DOGE")
            limit_price = get_limit_price("KRW-DOGE", 0.5)
            if target_price < current_price < limit_price:
                krw = get_balance("KRW")
                if krw > 500:
                    upbit.buy_market_order("KRW-DOGE", krw*0.9995)
                    print('buy')
                    
        else:
            DOGE = get_balance("DOGE")
            if btc > 0.00001:
                upbit.sell_market_order("KRW-DOGE", DOGE*0.9995)
                print('selled')
                
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
