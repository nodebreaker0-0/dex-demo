#!/usr/bin/env python
import urllib
#import threading
import urllib.parse
import requests
import json
import time
import random


Url = "http://127.0.0.1:1317/api"
keyid= "dex-demo2"
keypw= "wptjs1234"
mktid = "1"



def trade():
    derivative_price = 800
    while 1:

        rand = int(random.random()*10 - 5)
        if rand < 0 :
            rand = -rand*rand
        else:
            rand = rand*rand
        derivative_price += rand

        # data = oracle()
        data = oracle_fake(derivative_price)
        #data.reverse
        #data_sort = data.reverse()
        #print(data[0])
        for i in range(len(data)):
            global_price = str(round(data[i]['price']))
            global_price += "000000000000000000"
            #global_quantit = str(data[i]['size'])
            global_quantit = str(round(data[i]['size']))
            global_quantit += "000000000000000000"
            post_type = data[i]['side']
            if post_type == "Buy" :
                ret = buyOrder(global_price,global_quantit)
                print(ret)
            elif post_type == "Sell":
                ret = sellOrder(global_price,global_quantit)
                print(ret)
            else:
                print(ret)

def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/json",
        'cache-control': "no-cache",
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Cookie': cookie
    }   
    if add_to_headers:
        headers.update(add_to_headers)
    #postdata = urllib.parse.urlencode(params)
    api_url = Url + url
    response = requests.get(api_url, params, headers=headers)
    res = response.content
    try:

        if response.status_code == 200 or 204:
            return json.loads(res)
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" %(response.text,e))
        return

def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "*/*",
        "Content-type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Cookie': cookie
    }
    if add_to_headers:
        headers.update(add_to_headers)
    #postdata = urllib.parse.urlencode(params).encode("utf-8")
    api_url = Url + url
    response = requests.post(api_url, params, headers=headers)
    res = response.content
    try:

        if response.status_code == 200 or 204:
            return json.loads(res)
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" %(response.text,e))
        return

def buyOrder( price, quantity):
    path = '/v1/exchange/orders'
    params = {
        'market_id': mktid,
        'direction': "BID",
        'price': price,
        'quantity': quantity,
        'type': "LIMIT",
        'time_in_force': 600,
    }
    #t = threading.Thread(target=http_post_request, args=(path, json.dumps(params)))
    #t.start()
    #time.sleep(0.1)
    return http_post_request(path, json.dumps(params))

def sellOrder( price, quantity):
    path = '/v1/exchange/orders'
    params = {
        'market_id': mktid,
        'direction': "ASK",
        'price': price,
        'quantity': quantity,
        'type': "LIMIT",
        'time_in_force': 600,
    }
    #t = threading.Thread(target=http_post_request, args=(path, json.dumps(params)))
    #t.start()
    #time.sleep(0.1)
    return http_post_request(path, json.dumps(params))

def login():
    global cookie
    headers = {
        "Accept": "*/*",
        "Content-type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Origin': 'http://127.0.0.0:1317'
    }
    login_form = {
        'username':keyid, 
        'password':keypw
    }
    login_req = json.dumps(login_form)
    url = "http://127.0.0.1:1317/api/v1/auth/login"
    response = requests.post(url, login_req,headers=headers)
    cookie = response.headers.get('Set-Cookie')
    return

def oracle():
    headers = {
        "Content-type": "application/json",
        'cache-control': "no-cache",
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    url = "https://www.bitmex.com/api/v1/orderBook/L2?symbol=XBT&depth=25"
    response = requests.get(url,verify=False,headers=headers)
    data = response.content
    try:
        if response.status_code == 200:
            return json.loads(data)
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" %(response.text,e))
        return

def oracle_fake(price):
    


    orderbook = []
    for i in range(0,2):
        orderbook.append(
            {
            "symbol": "XBTUSD",
            "id": 8799190000,
            "side": "Sell",
            "size": int(random.random()*10+1),
            "price": price + i
            },
        )
    for i in range(0,2):
        orderbook.append(
            {
            "symbol": "XBTUSD",
            "id": 8799190000,
            "side": "Buy",
            "size": int(random.random()*10+1),
            "price": price - i
            },
        )
    return orderbook

if __name__ == "__main__":

        login()
        trade()

