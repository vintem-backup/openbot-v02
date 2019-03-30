# coding: utf-8

import dateparser
import pytz
from datetime import datetime
from binance.client import Client
import time
import os
import sys
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Float
from elasticsearch_dsl.connections import connections
from datetime import datetime
import time
from binance.client import Client

#code from sammchardy.github.io/binance



def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)










def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms












def get_historical_klines(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Binance
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
    """
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 500

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    start_ts = date_to_milliseconds(start_str)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data






def get_historical_klines_from_ts(symbol, interval, start_ts, end_ts=None):
    """Get Historical Klines from Binance from timestamp in milliseconds
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_ts: Start timestamp
    :type start_ts: float
    :param end_ts: optional - end date timestamp
    :type end_ts: float
    :return: list of OHLCV values
    """

    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 500

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    #start_ts = date_to_milliseconds(start_str)

    # if an end time was passed convert it
    #end_ts = None
    #if end_str:
    #    end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data

def create_marketdata(host,symbol,interval,start_str,end_str=None):
    """ Creates an Elasticsearch index for a certain (symbol) Binance asset
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param host: Elasticsearch host server e.g localhost:9200
    :type host: str
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
     """
    client = Client("","")
    
    hist = client.get_historical_klines(symbol,interval,start_str,end_str) 
    del hist[-1]
    
    #es = Elasticsearch(hosts=[host])
    connections.create_connection(hosts=[host])
    
    class Candle(Document):
        Open = Float()
        High = Float()
        Low = Float()
        Close = Float()
        Volume = Float()
        Close_time = Float()
        Quote_asset_vol = Float()
        N_of_trades = Float()
        Taker_buy_base_asset_vol = Float()
        Taker_buy_quote_asset_vol = Float()
    
        class Index:
            #name =  'marketdata' + '-' + symbol.lower() + '-' + interval + '-' 'binance'

            name =  'marketdata-' + symbol.lower() + '-' + interval + '-binance'

    
        def save(self, **kwargs):
            return super(Candle, self).save(**kwargs)
        
    
    Candle().init()
        

    for i in range(0,len(hist)): #Indexing 'hist'
        candle = Candle(meta={'id': hist[i][0]})
        candle.Open = float(hist[i][1])
        candle.High = float(hist[i][2])
        candle.Low = float(hist[i][3])
        candle.Close = float(hist[i][4])
        candle.Volume = float(hist[i][5])
        candle.Close_time = hist[i][6]
        candle.Quote_asset_vol = float(hist[i][7])
        candle.N_of_trades = float(hist[i][8])
        candle.Taker_buy_base_asset_vol = float(hist[i][9])
        candle.Taker_buy_quote_asset_vol = float(hist[i][10])
    
        candle.save()

def update_marketdata(host,indexName):
    """ Updates marketdata of binance assets stored in an elasticsearch Index.
    :param host: Elasticsearch host server e.g localhost:9200
    :type host: str
    :param indexName: Elasticsearch Index e.g marketdata-btcusdt-1m-binance
    :type host: str
    :return: list of OHLCV values
    """
    
    symbol = indexName.split(sep='-')[1].upper()
    interval = indexName.split(sep='-')[2]
    es = Elasticsearch(hosts=[host])
    connections.create_connection(hosts=[host])
    

    lastCandleStored = es.search(index=indexName, size = 1, sort = "_id:desc")
    close_time = int(lastCandleStored['hits']['hits'][0]['_source']['Close_time'])
    hist_new = get_historical_klines_from_ts(symbol,interval,close_time)
    del hist_new[-1] # drop unfinished candle. A if may be needed here.
    if len(hist_new):
        
        class Candle(Document):
            Open = Float()
            High = Float()
            Low = Float()
            Close = Float()
            Volume = Float()
            Close_time = Float()
            Quote_asset_vol = Float()
            N_of_trades = Float()
            Taker_buy_base_asset_vol = Float()
            Taker_buy_quote_asset_vol = Float()
    
            class Index:
                #name =  'marketdata' + '-' + symbol.lower() + '-' + interval + '-' 'binance'
                name =  'marketdata-' + symbol.lower() + '-' + interval + '-binance'                

            def save(self, **kwargs):
                return super(Candle, self).save(**kwargs)                  
            
        for i in range(0,len(hist_new)): #Indexing 'hist_new'
            candle = Candle(meta={'id': hist_new[i][0]})
            candle.Open = float(hist_new[i][1])
            candle.High = float(hist_new[i][2])
            candle.Low = float(hist_new[i][3])
            candle.Close = float(hist_new[i][4])
            candle.Volume = float(hist_new[i][5])
            candle.Close_time = hist_new[i][6]
            candle.Quote_asset_vol = float(hist_new[i][7])
            candle.N_of_trades = float(hist_new[i][8])
            candle.Taker_buy_base_asset_vol = float(hist_new[i][9])
            candle.Taker_buy_quote_asset_vol = float(hist_new[i][10])
    
            candle.save()


def live_update_marketdata(host,indexName):
    
    symbol = indexName.split(sep='-')[1].upper()
    interval = indexName.split(sep='-')[2]
    intervalInSeconds = interval_to_milliseconds(interval)/1000
    es = Elasticsearch(hosts=[host])
    i=0    
    while True:
        #print('i:',i)
        update_marketdata(host,indexName)
        #print('Banco de dados atualizados.')
        if i==0:
            time.sleep(4) # is there any need for this at all?
            i=1
        else:
            time.sleep(1) # is there any need for this at all?
        lastCandle = es.search(index=indexName, size = 1, sort = "_id:desc")
        lastCandle_Open_inSeconds = float(lastCandle['hits']['hits'][0]['_id'])/1000
        #print('OpenTime do Ultimo Candle no Bd: ',lastCandle_Open_inSeconds)
        wait = lastCandle_Open_inSeconds + intervalInSeconds*2 - time.time() 
        #print('Espera: ',wait)
        time.sleep(wait) 
        while True:
            openedCandle_Open = float(get_historical_klines(symbol,interval,'2 minutes ago UTC')[-1][0]) #Mod 
            if (lastCandle_Open_inSeconds + 120)*1000 == openedCandle_Open: #mod
                break
            else:
                time.sleep(1)
            


