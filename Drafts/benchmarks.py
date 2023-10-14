from cloudquant.interfaces import Strategy, Event
import ktgfunc

class Gr8Scriptab897b81ad8143bea94d1dee15cdde53(Strategy):
    __script_name__ = 'Gr8Script'

from cloudquant import Client
from cloudquant.interfaces import Strategy
import pandas as pd
import os
    
from pathlib import Path

# tickerItrAaRon=['SPY','QQQ','BITI','COIN','ACN','ADBE','ALB','ALGN','ALNY','AMP','ANET','ANSS','ARM','ASML','AVGO','BKNG','BLDR','BLK','BURL','CAR','CART','CAT','CDNS','CELH','CHTR','CI','CMG','COST','CRWD','CSL','CTAS','DE','DECK','DHR','DPZ','ELF','ELV','EPAM','EQIX','ETN','FDS','FNGU','FSLR','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','KLAC','LII','LLY','LMT','LRCX','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MKTX','MLM','MORN','MPWR','MRNA','MSCI','MSFT','MSTR','NFLX','NOC','NOW','NVDA','NXST','ODFL','OIH','ORLY','PANW','PAYC','PH','PODD','RBC','REGN','RH','ROK','ROP','SAIA','SEDG','SMCI','SNOW','SNPS','SOXX','SPGI','SWAV','SYK','TDG','TDY','TEAM','TMO','TSLA','ULTA','UNH','URI','VEEV','VGT','VRTX','WAT','WING','WST','ZS','ACN','ADBE','ALB','ALGN','ALNY','AMP','ANET','ANSS','ARM','ASML','AVGO','BKNG','BLDR','BLK','BURL','CAR','CART','CAT','CDNS','CELH','CHTR','CI','CMG','COST','CRWD','CSL','CTAS','DE','DECK','DHR','DPZ','ELF','ELV','EPAM','EQIX','ETN','FDS','FNGU','FSLR','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','KLAC','LII','LLY','LMT','LRCX','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MKTX','MLM','MORN','MPWR','MRNA','MSCI','MSFT','MSTR','NFLX','NOC','NOW','NVDA','NXST','ODFL','OIH','ORLY','PANW','PAYC','PH','PODD','RBC','REGN','RH','ROK','ROP','SAIA','SEDG','SMCI','SNOW','SNPS','SOXX','SPGI','SWAV','SYK','TDG','TDY','TEAM','TMO','TSLA','ULTA','UNH','URI','VEEV','VGT','VRTX','WAT','WING','WST','ZS','ACN','ADBE','ALB','ALGN','ALNY','AMP','ANET','ANSS','ARM','ASML','AVGO','BKNG','BLDR','BLK','BURL','CAR','CART','CAT','CDNS','CELH','CHTR','CI','CMG','COST','CRWD','CSL','CTAS','DE','DECK','DHR','DPZ','ELF','ELV','EPAM','EQIX','ETN','FDS','FNGU','FSLR','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','KLAC','LII','LLY','LMT','LRCX','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MKTX','MLM','MORN','MPWR','MRNA','MSCI','MSFT','MSTR','NFLX','NOC','NOW','NVDA','NXST','ODFL','OIH','ORLY','PANW','PAYC','PH','PODD','RBC','REGN','RH','ROK','ROP','SAIA','SEDG','SMCI','SNOW','SNPS','SOXX','SPGI','SWAV','SYK','TDG','TDY','TEAM','TMO','TSLA','ULTA','UNH','URI','VEEV','VGT','VRTX','WAT','WING','WST','ZS']  # noqa: E501
tickerItrAaRon=['MDB', 'EQIX']
observeTickers=[]
benchPTS = [0.00] * 14
observeBenchmark=[benchPTS,benchPTS,benchPTS,benchPTS]

for foraTICKER in tickerItrAaRon:
    oneBar = client.get_bars(foraTICKER, start_date='2019-11-19', bar_length='minute', end_date='2019-11-20')  # noqa: E501
    dfOne = oneBar.reset_index()
    i=vwap_TTL_CTR=vwap_PCT_CTR=spr_TTL_CTR=spr_PCT_CTR=ct_TTL_CTR=ct_PCT_CTR=0
    
    for index, row in dfOne.iterrows():

        if(row['vwap'] > 0):
            stampA = str(row['timestamp'])
            HRminSEC = stampA[11:]
            YRmoDT = stampA[:10]
            if(len(observeTickers)>1):
                if(observeTickers[-1][2]!=YRmoDT):
                    i=vwap_TTL_CTR=vwap_PCT_CTR=spr_TTL_CTR=spr_PCT_CTR=ct_TTL_CTR=ct_PCT_CTR=0
                    observeTickers.append([i, foraTICKER, YRmoDT, HRminSEC, row['vwap'],  row['spread'], row['count'], row['bidvol'], row['askvol'], row['volume'], row['open'], row['close'], row['low'], row['high'], row['avgdelta']])  # noqa: E501
                    pass
                else:
                    # CHECK VWAP
                    vwap_PX1_CHG = observeTickers[-1][4]-observeTickers[-2][4]
                    vwap_PCT_CHG = vwap_PX1_CHG/observeTickers[-2][4]
                    vwap_TTL_CTR += vwap_PX1_CHG
                    vwap_PCT_CTR += vwap_PCT_CHG
                    vwap_AVG_PTS = vwap_TTL_CTR/i
                    vwap_AVG_RTE = vwap_PCT_CTR/i
                    vwap_WGT_CHG = vwap_PX1_CHG/vwap_AVG_PTS+0.0000001
                    vwap_WGT_RTE = vwap_PCT_CHG/vwap_AVG_RTE+0.0000001
                    # CHECK SPREAD
                    spr_PX1_CHG = observeTickers[-1][5]-observeTickers[-2][5]
                    spr_PCT_CHG = spr_PX1_CHG/observeTickers[-2][5]
                    spr_TTL_CTR += spr_PX1_CHG
                    spr_PCT_CTR += spr_PCT_CHG
                    spr_AVG_CHG = spr_TTL_CTR/i
                    spr_AVG_RTE = spr_PCT_CTR/i
                    spr_WGT_CHG = spr_PX1_CHG/spr_AVG_CHG+0.0000001
                    spr_WGT_RTE = spr_PCT_CHG/spr_AVG_RTE+0.0000001
                    # CHECK CT
                    ct_CT1_CHG = observeTickers[-1][6]-observeTickers[-2][6]
                    ct_PCT_CHG = ct_CT1_CHG/observeTickers[-2][6]
                    ct_TTL_CTR += ct_CT1_CHG
                    ct_PCT_CTR += ct_PCT_CHG
                    ct_AVG_CHG = ct_TTL_CTR/i
                    ct_AVG_RTE = ct_PCT_CTR/i
                    ct_WGT_CHG = ct_CT1_CHG/ct_AVG_CHG+0.0000001
                    ct_WGT_RTE = ct_PCT_CHG/ct_AVG_RTE+0.0000001

                # PH SET AT ONSET    
                if(foraTICKER=="SPY"):
                    observeBenchmark[0].append([i, foraTICKER, YRmoDT, HRminSEC, row['vwap'],  row['spread'], row['count'], row['bidvol'], row['askvol'], row['volume'], row['open'], row['close'], row['low'], row['high'], row['avgdelta']])  # noqa: E501
                elif(foraTICKER=="QQQ"):
                    observeBenchmark[1].append([i, foraTICKER, YRmoDT, HRminSEC, row['vwap'],  row['spread'], row['count'], row['bidvol'], row['askvol'], row['volume'], row['open'], row['close'], row['low'], row['high'], row['avgdelta']])  # noqa: E501
                elif(foraTICKER=="BITI"):
                    observeBenchmark[2].append([i, foraTICKER, YRmoDT, HRminSEC, row['vwap'],  row['spread'], row['count'], row['bidvol'], row['askvol'], row['volume'], row['open'], row['close'], row['low'], row['high'], row['avgdelta']])  # noqa: E501
                elif(foraTICKER=="COIN"):
                    observeBenchmark[3].append([i, foraTICKER, YRmoDT, HRminSEC, row['vwap'],  row['spread'], row['count'], row['bidvol'], row['askvol'], row['volume'], row['open'], row['close'], row['low'], row['high'], row['avgdelta']])  # noqa: E501
                


            else:
                observeTickers.append([i, foraTICKER, YRmoDT, HRminSEC, row['vwap'],  row['spread'], row['count'], row['bidvol'], row['askvol'], row['volume'], row['open'], row['close'], row['low'], row['high'], row['avgdelta']])  # noqa: E501
                pass


            print(observeTickers[-1])
            posStringArgument=""
            for informationCenter in observeTickers[-1]:
                posStringArgument+=str(informationCenter)+" , "

            j=0
            while(j<4):
                for informationBench in observeBenchmark[j][-1]:
                    posStringArgument+=str(informationBench)+" , "
                j+=1
            posStringArgument+="\n"
            with open('C:\\Users\\bdincer\\Kite12\\dataCenter\\file.txt', "a") as myfile:
                myfile.write(posStringArgument)

            i+=1



            # Path('C:\\Users\\bdincer\\Kite12\\dataCenter\\file.txt').write_text(posStringArgument)
            # Path('C:\\Users\\bdincer\\Kite12\\dataCenter\\file.txt').write_text(observeTickers[-1][0],observeTickers[-1][1],observeTickers[-1][2],observeTickers[-1][3],observeTickers[-1][4],\
            #                                                                    observeTickers[-1][5],observeTickers[-1][6],observeTickers[-1][7],observeTickers[-1][8],observeTickers[-1][9],\
            #                                                                    observeTickers[-1][10],observeTickers[-1][11],observeTickers[-1][12],observeTickers[-1][13],observeTickers[-1][14])
    
#     data_top = oneBar.head(30)
#     print(foraTICKER)
#     print(data_top)=
# print(data_top)
# dfOne = oneBar.reset_index()
# for index, row in dfOne.iterrows():
#     print(dir(row))
# print(len(dfOne))
# print(dir(oneBar))
# print(oneBar)


# submission = client.submit(
#     strategy=strategy_name,               # with "CQ" prefix and no dashes
#     symbols=['__ALL_MULTI__'],            # or like ['SPY', 'IBM', 'HP'] etc.
#     start_date='2019-11-19',              # ISO dates ONLY
#     end_date='2019-11-20',
#     start_time=['09:30:00', '15:57:00'],  # These also accept comma-delimited
#     end_time=['09:31:00', '16:00:00'],    #  strings of times.
#     name='test_submit',
#     description='from_CQAI',              # The submission name on the webpage
#     email=True,                           # Email on completion
#     options={'fast_simulation': False,
#              'python_version': '3.6beta'},      # Use python 3.6 (if available)
#     strategy_params={'ATR': 60})                # Strateegy-specific parameters
