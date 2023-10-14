from cloudquant.interfaces import Strategy, Event

#https://archive.org/details/arxiv-1106.5040/page/n15/mode/2up


class gaspardata(Strategy):
    __script_name__ = 'gaspardata'
   
    bpRisk=50000; cycl=5; askRTE=1.0026; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; plUpperBand=bpRisk*.01; plLowerBand=-bpRisk*.01; plBandMult=bpRisk*.01; 

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'GS'

    def on_start(self, md, order, service, account):
        self.itr=-1;
        self.status=0;
        self.cover=0;
        self.idxLoop=-1;
        self.dataPt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMS =[]
        self.sections=[0.00] * 10
        self.dataBookSections =[]
        self.dataBookMSB =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMSC =[[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.fileName=self.symbol+"Data-x1.txt"
        #self.fileNameThree=self.symbol+"file3-1x1.txt"
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(minutes=1), timer_id="Allocate")
        # ATR over 10 days based on an underlying 250 days of TR (True Range). USE TA Lib# 21 day avg vol.
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;

    def on_timer(self, event, md, order, service, account):
        self.idxLoop+=1;
        qualityCheck=0;
        bidPx=md.L1.bid;
        askPx=md.L1.ask;
        lstPx=md.L1.last;
        hiPx = md.L1.daily_high;
        loPx= md.L1.daily_low;
        midPX=max(askPx,bidPx);
        if(bidPx!=0 and askPx!=0):
            midPX=bidPx+((askPx-bidPx)/2);
        else:
            qualityCheck=1;
            
        mdRange=max(hiPx,loPx);
        if(hiPx!=0 and loPx!=0):
            mdRange=loPx+((hiPx-loPx)/2);
        else:
            qualityCheck=1;
            
        lstBid=max(lstPx,bidPx);
        if(lstPx!=0 and bidPx!=0):
            lstBid=lstPx+(lstPx-bidPx);
        else:
            qualityCheck=1;

        lstAsk=max(lstPx, askPx);
        if(lstPx!=0 and askPx!=0):
            lstAsk=lstPx+(lstPx-askPx);
        else:
            qualityCheck=1;
            
        lstMid=max(lstPx, midPX);
        if(lstPx!=0 and midPX!=0):
            lstMid=lstPx+(lstPx-midPX);
        else:
            qualityCheck=1;
            
        self.dataPt.append([self.symbol, qualityCheck, self.itr, md.L1.exchange, md.L1.ask_exchange, md.L1.bid_exchange, lstPx, bidPx, askPx, hiPx, loPx,  self._prev_close, md.L1.closing_trade, self._atr, hiPx-loPx, askPx-bidPx, midPX, mdRange,lstBid,lstAsk,lstMid])
        
        if(self.idxLoop<40):
            return;
        
        
        barA=md.bar.minute(start=-44, end=None, include_empty=False, include_extended=True, bar_size=1, today_only=True)
        barM=md.bar.minute(start=-32, end=None, include_empty=False, include_extended=True, bar_size=1, today_only=True)
        barPoints=[0.00] * 280
        rangeMS = min(len(barM.timestamp), len(barM.askvol), len(barM.bidvol), len(barM.bvwap), len(barM.close), len(barM.count), len(barM.high), len(barM.low), len(barM.open), len(barM.spread), len(barM.volume))
        rangeM=rangeMS-1;
        rangeDT=len(self.dataPt[-1]);
        
        RATE_CHK=249;
        offset=-rangeM;
        for idx in range(0, rangeM, 1):
            self.dataBookMS.append(barPoints);
            self.dataBookSections.append(self.sections);
            
            self.itr+=1;
            
            self.dataBookMS[self.itr][0]=self.symbol;
            self.dataBookMS[self.itr][1]=idx+1;
            self.dataBookMS[self.itr][2]=self.itr;
            self.dataBookMS[self.itr][3]=barA.timestamp[idx];
            self.dataBookMS[self.itr][4]=barA.askvol[idx];
            self.dataBookMS[self.itr][5]=barA.bidvol[idx]; 
            self.dataBookMS[self.itr][6]=barA.bvwap[idx];
            self.dataBookMS[self.itr][7]=barA.close[idx];
            self.dataBookMS[self.itr][8]=barA.open[idx];
            self.dataBookMS[self.itr][9]=barA.high[idx];
            self.dataBookMS[self.itr][10]=barA.low[idx];
            self.dataBookMS[self.itr][11]=barA.count[idx];
            self.dataBookMS[self.itr][12]=barA.spread[idx];
            self.dataBookMS[self.itr][13]=barA.volume[idx];
            self.dataBookMS[self.itr][14]=barA.high[idx]-barA.low[idx];
            self.dataBookMS[self.itr][15]=barA.close[idx]-barA.open[idx];
            self.dataBookMS[self.itr][16]=max(barA.bvwap[idx], barA.close[idx], barA.open[idx], barA.high[idx]);

            # self.dataBookMS[self.itr][50]=self.dataPt[-1+offset][1];
            
            print('[self.itr][offset][self.idxLoop]',self.itr,offset,self.idxLoop)
            
            bSeries=17;                                                                                    #BID
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][bSeries]=self.dataPt[_idx][7];
                bSeries+=1;
            self.dataBookMS[self.itr][26]=max(self.dataBookMS[self.itr][17:26])
            self.dataBookMS[self.itr][27]=min(self.dataBookMS[self.itr][17:26])
            self.dataBookMS[self.itr][RATE_CHK+4]=sum(self.dataBookMS[self.itr][17:26])/9;
            print('[17:27]\t BID  PRICE\t\t', bSeries, self.dataBookMS[self.itr][RATE_CHK+4], self.dataBookMS[self.itr][17:28]); 
            
            lSeries=28;                                                                                    #LAST
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][lSeries]=self.dataPt[_idx][6];
                lSeries+=1;
            self.dataBookMS[self.itr][37]=max(self.dataBookMS[self.itr][28:37])
            self.dataBookMS[self.itr][38]=min(self.dataBookMS[self.itr][28:37])
            self.dataBookMS[self.itr][RATE_CHK+5]=sum(self.dataBookMS[self.itr][28:37])/9;
            print('[28:38]\t LAST PRICE\t\t', lSeries, self.dataBookMS[self.itr][RATE_CHK+5], self.dataBookMS[self.itr][28:39]);
            
            aSeries=39;                                                                                    #ASK
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][aSeries]=self.dataPt[_idx][8];
                aSeries+=1;
            self.dataBookMS[self.itr][48]=max(self.dataBookMS[self.itr][39:48])
            self.dataBookMS[self.itr][49]=min(self.dataBookMS[self.itr][39:48])
            self.dataBookMS[self.itr][RATE_CHK+6]=sum(self.dataBookMS[self.itr][39:48])/9;
            print('[39:49]\t ASK  PRICE\t\t', aSeries, self.dataBookMS[self.itr][RATE_CHK+6], self.dataBookMS[self.itr][39:50]); 
            
            mSeries=51;                                                                                    #MIDPX
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][mSeries]=self.dataPt[_idx][16];
                mSeries+=1;
            self.dataBookMS[self.itr][60]=max(self.dataBookMS[self.itr][51:60])
            self.dataBookMS[self.itr][61]=min(self.dataBookMS[self.itr][51:60])
            self.dataBookMS[self.itr][RATE_CHK+7]=sum(self.dataBookMS[self.itr][51:60])/9;
            print('[51:61]\t MID  PRICE\t\t', mSeries, self.dataBookMS[self.itr][RATE_CHK+7], self.dataBookMS[self.itr][51:62]); 

            baSeries=62;                                                                                    #BID ASK SPREAD $
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][baSeries]=self.dataPt[_idx][15];
                baSeries+=1;
            self.dataBookMS[self.itr][71]=max(self.dataBookMS[self.itr][62:71])
            self.dataBookMS[self.itr][72]=min(self.dataBookMS[self.itr][62:71])
            self.dataBookMS[self.itr][RATE_CHK+8]=sum(self.dataBookMS[self.itr][62:71])/9;
            print('[62:72]\t BA   SPREAD\t\t', baSeries, self.dataBookMS[self.itr][RATE_CHK+8], self.dataBookMS[self.itr][62:73]); 
            
            hSeries=73;                                                                                        #HIGH
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][hSeries]=barA.high[_idx];
                hSeries+=1;
            self.dataBookMS[self.itr][82]=max(self.dataBookMS[self.itr][73:82])
            self.dataBookMS[self.itr][83]=min(self.dataBookMS[self.itr][73:82])
            self.dataBookMS[self.itr][RATE_CHK+9]=sum(self.dataBookMS[self.itr][73:82])/9;
            print('[73:83]\t INTERVAL HIGH\t\t', hSeries, self.dataBookMS[self.itr][RATE_CHK+9], self.dataBookMS[self.itr][73:84]);
            
            lSeries=84;                                                                                        #LOW
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][lSeries]=barA.low[_idx];
                lSeries+=1;
            self.dataBookMS[self.itr][93]=max(self.dataBookMS[self.itr][84:93])
            self.dataBookMS[self.itr][94]=min(self.dataBookMS[self.itr][84:93])
            self.dataBookMS[self.itr][RATE_CHK+10]=sum(self.dataBookMS[self.itr][84:93])/9;
            print('[84:94]\t INTERVAL LOW:\t\t', lSeries, self.dataBookMS[self.itr][RATE_CHK+10], self.dataBookMS[self.itr][84:95]);

            hlSeries=95;                                                                                    # High_LOW SPREAD $
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][hlSeries]=self.dataPt[_idx][14];
                hlSeries+=1;
            self.dataBookMS[self.itr][104]=max(self.dataBookMS[self.itr][95:104])
            self.dataBookMS[self.itr][105]=min(self.dataBookMS[self.itr][95:104])
            self.dataBookMS[self.itr][RATE_CHK+11]=sum(self.dataBookMS[self.itr][95:104])/9;
            print('[95:105]\t H_L  SPREAD:\t', hlSeries, self.dataBookMS[self.itr][RATE_CHK+11], self.dataBookMS[self.itr][95:106]);
            
            r1=106;                                                                                        #Range 1
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][r1]=self.dataPt[_idx][17];
                r1+=1;
            self.dataBookMS[self.itr][115]=max(self.dataBookMS[self.itr][106:115])
            self.dataBookMS[self.itr][116]=min(self.dataBookMS[self.itr][106:115])
            self.dataBookMS[self.itr][RATE_CHK+12]=sum(self.dataBookMS[self.itr][106:115])/9;
            print('[106:116]\t Range 1:\t', r1, self.dataBookMS[self.itr][RATE_CHK+12], self.dataBookMS[self.itr][106:117]);
            
            r2=117;                                                                                        #Range 2
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][r2]=self.dataPt[_idx][18];
                r2+=1;
            self.dataBookMS[self.itr][126]=max(self.dataBookMS[self.itr][117:126])
            self.dataBookMS[self.itr][127]=min(self.dataBookMS[self.itr][117:126])
            self.dataBookMS[self.itr][RATE_CHK+13]=sum(self.dataBookMS[self.itr][117:126])/9;
            print('[117:127]\t Range 2:\t', r2, self.dataBookMS[self.itr][RATE_CHK+13], self.dataBookMS[self.itr][117:128]);
            
            r3=128;                                                                                        #Range 3
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][r3]=self.dataPt[_idx][19];
                r3+=1;
            self.dataBookMS[self.itr][137]=max(self.dataBookMS[self.itr][128:137])
            self.dataBookMS[self.itr][138]=min(self.dataBookMS[self.itr][128:137])
            self.dataBookMS[self.itr][RATE_CHK+14]=sum(self.dataBookMS[self.itr][128:137])/9;
            print('[117:138]\t Range 3:\t', r3, self.dataBookMS[self.itr][RATE_CHK+14], self.dataBookMS[self.itr][128:139]);
            
            r4=139;                                                                                        #Range 4
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][r4]=self.dataPt[_idx][20];
                r4+=1;
            self.dataBookMS[self.itr][148]=max(self.dataBookMS[self.itr][139:148])
            self.dataBookMS[self.itr][149]=min(self.dataBookMS[self.itr][139:148])
            self.dataBookMS[self.itr][RATE_CHK+15]=sum(self.dataBookMS[self.itr][139:148])/9;
            print('[139:149]\t Range 4:\t', r4, self.dataBookMS[self.itr][RATE_CHK+15], self.dataBookMS[self.itr][139:150]);
            
            d1=150;                                                                                        #DEMAND
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][d1]=(self.dataPt[_idx][7]+self.dataPt[_idx][6])/2;
                d1+=1;
            self.dataBookMS[self.itr][159]=max(self.dataBookMS[self.itr][150:159])
            self.dataBookMS[self.itr][160]=min(self.dataBookMS[self.itr][150:159])
            self.dataBookMS[self.itr][RATE_CHK+16]=sum(self.dataBookMS[self.itr][150:159])/9;
            print('[150:160]\t DEMAND MKT\t', d1, self.dataBookMS[self.itr][RATE_CHK+16], self.dataBookMS[self.itr][150:161]);
            
            d2=161;                                                                                        #SUPPLY
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][d2]=(self.dataPt[_idx][8]+self.dataPt[_idx][6])/2;
                d2+=1;
            self.dataBookMS[self.itr][170]=max(self.dataBookMS[self.itr][161:170])
            self.dataBookMS[self.itr][171]=min(self.dataBookMS[self.itr][161:170])
            self.dataBookMS[self.itr][RATE_CHK+17]=sum(self.dataBookMS[self.itr][161:170])/9;
            print('[161:171]\t SUPPLY MKT\t', d2, self.dataBookMS[self.itr][RATE_CHK+17], self.dataBookMS[self.itr][161:172]);
            
            d3=172;                                                                                        #SUPPLY/DEMAND SPREAD $
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][d3]=self.dataBookMS[self.itr][d3-11]-self.dataBookMS[self.itr][d3-22];
                d3+=1;
            self.dataBookMS[self.itr][181]=max(self.dataBookMS[self.itr][172:181])
            self.dataBookMS[self.itr][182]=min(self.dataBookMS[self.itr][172:181])
            self.dataBookMS[self.itr][RATE_CHK+18]=sum(self.dataBookMS[self.itr][172:181])/9;
            print('[172:182]\t MARKET SPREAD $\t', d3, self.dataBookMS[self.itr][RATE_CHK+18], self.dataBookMS[self.itr][172:183]);
            
            d4=183;                                                                                        #SUPPLY/DEMAND SPREAD %
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][d4]=self.dataBookMS[self.itr][d4-11]/self.dataBookMS[self.itr][d4-33];
                d4+=1;
            self.dataBookMS[self.itr][192]=max(self.dataBookMS[self.itr][183:192])
            self.dataBookMS[self.itr][193]=min(self.dataBookMS[self.itr][183:192])
            self.dataBookMS[self.itr][RATE_CHK+19]=sum(self.dataBookMS[self.itr][183:192])/9;
            print('[183:193]\t MARKET SPREAD %\t', d4, self.dataBookMS[self.itr][RATE_CHK+19], self.dataBookMS[self.itr][183:194]);
            
            b1=194;                                                                                        #BID CHG $
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][b1]=self.dataPt[_idx][7]-self.dataPt[_idx-1][7];
                b1+=1;
            self.dataBookMS[self.itr][203]=max(self.dataBookMS[self.itr][194:203])
            self.dataBookMS[self.itr][204]=min(self.dataBookMS[self.itr][194:203])
            self.dataBookMS[self.itr][RATE_CHK+20]=sum(self.dataBookMS[self.itr][194:203])/9;
            print('[194:204]\t CHG BID $\t', b1, self.dataBookMS[self.itr][RATE_CHK+20], self.dataBookMS[self.itr][194:205]);

            b2=205;                                                                                        #BID CHG %
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][b2]=self.dataBookMS[self.itr][b2-11]/self.dataPt[_idx][7];
                b2+=1;
                
            self.dataBookMS[self.itr][214]=max(self.dataBookMS[self.itr][205:214])
            self.dataBookMS[self.itr][215]=min(self.dataBookMS[self.itr][205:214])
            self.dataBookMS[self.itr][RATE_CHK+21]=sum(self.dataBookMS[self.itr][205:214])/9;
            print('[205:215]\t CHG BID %\t', b2, self.dataBookMS[self.itr][RATE_CHK+21], self.dataBookMS[self.itr][205:216]);
            
            
            chkBID=self.dataBookMS[self.itr][269]*100000
            
            if(chkBID>0):
                self.dataBookMS[self.itr][276]=1;
                self.dataBookMS[self.itr][277]=0;
                self.dataBookMS[self.itr][278]=0;
            elif(chkBID<0):
                self.dataBookMS[self.itr][277]=1;
                self.dataBookMS[self.itr][276]=0;
            
            if(self.dataBookMS[self.itr][277]==0):
                self.dataBookMS[self.itr][278]==0;
            else:
                self.dataBookMS[self.itr][278]=self.dataBookMS[self.itr-1][278]+1;

            
            
            a1=216;                                                                                        #ASK CHG $
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][a1]=self.dataPt[_idx][8]-self.dataPt[_idx-1][8];
                a1+=1;
            self.dataBookMS[self.itr][225]=max(self.dataBookMS[self.itr][216:225])
            self.dataBookMS[self.itr][226]=min(self.dataBookMS[self.itr][216:225])
            self.dataBookMS[self.itr][RATE_CHK+22]=sum(self.dataBookMS[self.itr][216:225])/9;
            print('[216:226]\t CHG ASK $\t', a1, self.dataBookMS[self.itr][RATE_CHK+22], self.dataBookMS[self.itr][216:227]);
            

            
            a2=227;                                                                                        #ASK CHG %
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][a2]=self.dataBookMS[self.itr][a2-11]/self.dataPt[_idx][8];
                a2+=1;
            self.dataBookMS[self.itr][236]=max(self.dataBookMS[self.itr][227:236])
            self.dataBookMS[self.itr][237]=min(self.dataBookMS[self.itr][227:236])
            self.dataBookMS[self.itr][RATE_CHK+23]=sum(self.dataBookMS[self.itr][227:236])/9;
            print('[227:237]\t CHG ASK %\t', a2, self.dataBookMS[self.itr][RATE_CHK+23], self.dataBookMS[self.itr][227:238]);
            
            
            chkSUM=self.dataBookMS[self.itr][271]*100000
            
            if(chkSUM>0):
                self.dataBookMS[self.itr][273]=1;
                self.dataBookMS[self.itr][274]=0;
                self.dataBookMS[self.itr][275]=0;
            elif(chkSUM<0):
                self.dataBookMS[self.itr][274]=1;
                self.dataBookMS[self.itr][273]=0;
            
            if(self.dataBookMS[self.itr][274]==0):
                self.dataBookMS[self.itr][275]==0;
            else:
                self.dataBookMS[self.itr][275]=self.dataBookMS[self.itr-1][275]+1;
                    
                    
            
            ba1=238;                                                                                        #BID ASK SPREAD %
            for _idx in range(offset+1, offset-8, -1):
                self.dataBookMS[self.itr][ba1]=(self.dataPt[_idx][8]-self.dataPt[_idx][7])/self.dataPt[_idx][8];
                ba1+=1;
            self.dataBookMS[self.itr][247]=max(self.dataBookMS[self.itr][238:247])
            self.dataBookMS[self.itr][248]=min(self.dataBookMS[self.itr][238:247])
            self.dataBookMS[self.itr][RATE_CHK+3]=sum(self.dataBookMS[self.itr][238:247])/9;
            print('[238:248]\t BID ASK SPREAD %\t', ba1, self.dataBookMS[self.itr][RATE_CHK+3], self.dataBookMS[self.itr][238:249]);
            

            self.dataBookMS[self.itr][279]=self.dataBookMS[self.itr][275]+self.dataBookMS[self.itr][278]
            
            
            if(self.dataBookMS[self.itr][275]==7):
                self.status=0;
                px7=md.L1.bid-0.00009;
                offer15 = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=7, price=md.L1.ask*1.07, allow_multiple_pending=40)
                
            if(self.dataBookMS[self.itr][275]==8):
                self.status=0;
                px8=md.L1.bid-0.00009;
                offer15 = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=8, price=md.L1.ask*1.07, user_key=8, allow_multiple_pending=40)
            
            #if(self.status==1):
            #    order.cancel(self.symbol);
            #    self.status=0;
            if(self.dataBookMS[self.itr][273]==1 and self.dataBookMS[self.itr-1][274]==1):
                purchase = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=1, price=md.L1.bid*.97, user_key=151, allow_multiple_pending=40);
            
            
            if(md.L1.ask<account[self.symbol].position.mtm_price and self.cover==1 and account[self.symbol].position.shares<0):
                self.status+=1;
                cvrPrice=md.L1.ask+0.0009
                maskUp = order.algo_buy(self.symbol, algorithm='7a6228ad-dc9d-4377-8b2e-99e8ebb90152', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), price=cvrPrice, user_key=151, allow_multiple_pending=40);
            
            #if(self.status==1 and account[self.symbol].position.shares<0):
            #    cvrPrice=md.L1.ask-0.0009
            #    maskUp = order.algo_buy(self.symbol, algorithm='f3b4beac-a70b-4953-97e0-fd7d2a0f7ee0', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), price=cvrPrice, user_key=151, allow_multiple_pending=40);
            
            #if(self.dataBookMS[self.itr][273]==1 and self.dataBookMS[self.itr-1][274]==1 and account[self.symbol].position.shares<0):
            #    print('cover')
            #    self.status=1;
            #    #cvrPrice=min(md.L1.ask, md.L1.last)+0.00009;
                
                
                
                
            
            
            #if(self.dataBookMS[self.itr][275]+self.dataBookMS[self.itr][278]==15):
            #    px15=md.L1.bid-0.001;
            #    offer15 = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=150, price=px15, user_key=15, allow_multiple_pending=40)
                
            
            if(self.idxLoop>10 and idx==rangeM-2):
                break;
                str0=str(self.itr)+",";
                for units in self.dataBookMS[self.itr]:
                    str0+=str(units)+",";
                str0+='\n';
                service.write_file(self.fileName,'{}'.format(str0))  
                break;
                
                # CONDITIONS [ 221 : 224 ]
                hl_spr=0; i=0; crSpr=0; mxSpr=0;sxSpr=self.dataBookMS[idx][14];
                for x in self.dataBookMS:
                    crSpr=self.dataBookMS[i][14];
                    hl_spr+=self.dataBookMS[i][14];
                    i+=1;
                    if(crSpr>mxSpr): mxSpr=crSpr; pass;
                    if(crSpr<sxSpr): sxSpr=crSpr; pass;

                avgSpr=hl_spr/i;
                print('avgSpr, mxSpr, sxSpr, self.dataBookMS[self.itr][14]')
                print(avgSpr, mxSpr, sxSpr, self.dataBookMS[self.itr][14])
                
                if(self.dataBookMS[self.itr][14]==mxSpr): self.dataBookMS[self.itr][221]=1; pass;
                if(self.dataBookMS[self.itr][14]==sxSpr): self.dataBookMS[self.itr][222]=-1; pass;
                if(self.dataBookMS[self.itr][14]<avgSpr): self.dataBookMS[self.itr][223]=-1; pass;
                if(self.dataBookMS[self.itr][14]>avgSpr): self.dataBookMS[self.itr][224]=1; pass;

                # CONDITIONS [ 150 : 173 ]
                if(self.dataBookMS[self.itr][139]==self.dataBookMS[self.itr][148]): self.dataBookMS[self.itr][150]=1;pass;
                elif(self.dataBookMS[self.itr][139]==self.dataBookMS[self.itr][149]): self.dataBookMS[self.itr][151]=-1;pass;
                if(self.dataBookMS[self.itr][128]==self.dataBookMS[self.itr][137]): self.dataBookMS[self.itr][152]=1;pass;
                elif(self.dataBookMS[self.itr][128]==self.dataBookMS[self.itr][138]): self.dataBookMS[self.itr][153]=-1;pass;
                if(self.dataPt[-1][18]==self.dataBookMS[self.itr][126]): self.dataBookMS[self.itr][154]=1;pass;
                elif(self.dataPt[-1][18]==self.dataBookMS[self.itr][127]): self.dataBookMS[self.itr][155]=-1;pass;
                if(self.dataPt[-1][17]==self.dataBookMS[self.itr][115]): self.dataBookMS[self.itr][156]=1;pass;
                elif(self.dataPt[-1][17]==self.dataBookMS[self.itr][116]): self.dataBookMS[self.itr][157]=-1;pass;
                spr2 = md.L1.daily_high-md.L1.daily_low;
                if(spr2>=self.dataBookMS[self.itr][104]): self.dataBookMS[self.itr][158]=1;pass;
                elif(spr2<=self.dataBookMS[self.itr][105]): self.dataBookMS[self.itr][159]=-1;pass;
                if(self.dataBookMS[self.itr][10]>=self.dataBookMS[self.itr][93]): self.dataBookMS[self.itr][160]=1;pass;
                elif(self.dataBookMS[self.itr][10]<=self.dataBookMS[self.itr][94]): self.dataBookMS[self.itr][161]=-1;pass;
                if(self.dataBookMS[self.itr][9]==self.dataBookMS[self.itr][82]): self.dataBookMS[self.itr][162]=1;pass;
                elif(self.dataBookMS[self.itr][9]==self.dataBookMS[self.itr][83]): self.dataBookMS[self.itr][163]=-1;pass;
                if(self.dataPt[-1][15]==self.dataBookMS[self.itr][71]): self.dataBookMS[self.itr][164]=1;pass;
                elif(self.dataPt[-1][15]==self.dataBookMS[self.itr][72]): self.dataBookMS[self.itr][165]=-1;pass;
                if(self.dataPt[-1][16]==self.dataBookMS[self.itr][60]): self.dataBookMS[self.itr][166]=1;pass;
                elif(self.dataPt[-1][16]==self.dataBookMS[self.itr][61]): self.dataBookMS[self.itr][167]=-1;pass;
                if(self.dataPt[-1][8]==self.dataBookMS[self.itr][48]): self.dataBookMS[self.itr][168]=1;pass;
                elif(self.dataPt[-1][8]==self.dataBookMS[self.itr][49]): self.dataBookMS[self.itr][169]=-1;pass;
                if(self.dataPt[-1][6]==self.dataBookMS[self.itr][37]): self.dataBookMS[self.itr][170]=1;pass;
                elif(self.dataPt[-1][6]==self.dataBookMS[self.itr][38]): self.dataBookMS[self.itr][171]=-1;pass;
                if(self.dataPt[-1][7]==self.dataBookMS[self.itr][26]): self.dataBookMS[self.itr][172]=1;pass;
                elif(self.dataPt[-1][7]==self.dataBookMS[self.itr][27]): self.dataBookMS[self.itr][173]=-1;pass;

                # CONDITIONS [ 181 : 191]
                chkA=[0,0,0,0,0,0,0];
                for idxA in range(-2, -10, -1):
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][7]): chkA[0]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][9]): chkA[1]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][16]): chkA[2]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][17]): chkA[3]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][18]): chkA[4]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][19]): chkA[5]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][20]): chkA[6]+=1;pass;
                iA=0;
                for idA in range(174, 181, 1):
                    self.dataBookMS[self.itr][idA]=chkA[iA];
                    iA+=1;
                    
                chkB=[0,0,0,0,0,0,0,0,0,0];
                for bIdx in range(-2, -10, -1):
                    if(self.dataPt[bIdx][6]>self.dataPt[bIdx-1][6]): chkB[0]+=1;pass;
                    if(self.dataPt[bIdx][7]>self.dataPt[bIdx-1][7]): chkB[1]+=1;pass;
                    if(self.dataPt[bIdx][8]>self.dataPt[bIdx-1][8]): chkB[2]+=1;pass;
                    if(self.dataPt[bIdx][14]>self.dataPt[bIdx-1][14]): chkB[3]+=1;pass;
                    if(self.dataPt[bIdx][15]>self.dataPt[bIdx-1][15]): chkB[4]+=1;pass;
                    if(self.dataPt[bIdx][16]>self.dataPt[bIdx-1][16]): chkB[5]+=1;pass;
                    if(self.dataPt[bIdx][17]>self.dataPt[bIdx-1][17]): chkB[6]+=1;pass;
                    if(self.dataPt[bIdx][18]>self.dataPt[bIdx-1][18]): chkB[7]+=1;pass;
                    if(self.dataPt[bIdx][19]>self.dataPt[bIdx-1][19]): chkB[8]+=1;pass;
                    if(self.dataPt[bIdx][20]>self.dataPt[bIdx-1][20]): chkB[9]+=1;pass;
                    
                idB=0;
                for idBin in range(181, 191, 1):
                    self.dataBookMS[self.itr][idBin]=chkB[idB];
                    idB+=1;
                # CONDITIONS [ 191 : 200]
                self.dataBookMS[self.itr][191]=(self.dataPt[-1][6]-self.dataPt[-2][6])/self.dataPt[-1][6];
                self.dataBookMS[self.itr][192]=(self.dataPt[-1][7]-self.dataPt[-2][7])/self.dataPt[-1][7];
                self.dataBookMS[self.itr][193]=(self.dataPt[-1][8]-self.dataPt[-2][8])/self.dataPt[-1][8];
                self.dataBookMS[self.itr][194]=(self.dataPt[-1][14]-self.dataPt[-2][14])/self.dataPt[-1][14];
                self.dataBookMS[self.itr][195]=(self.dataPt[-1][15]-self.dataPt[-2][15])/self.dataPt[-1][15]; 
                self.dataBookMS[self.itr][196]=(self.dataPt[-1][16]-self.dataPt[-2][16])/self.dataPt[-1][16];              
                self.dataBookMS[self.itr][197]=(self.dataPt[-1][17]-self.dataPt[-2][17])/self.dataPt[-1][17];
                self.dataBookMS[self.itr][198]=(self.dataPt[-1][18]-self.dataPt[-2][18])/self.dataPt[-1][18];
                self.dataBookMS[self.itr][199]=(self.dataPt[-1][19]-self.dataPt[-2][19])/self.dataPt[-1][19];
                self.dataBookMS[self.itr][200]=(self.dataPt[-1][20]-self.dataPt[-2][20])/self.dataPt[-1][20];
            
                    
                # CONDITIONS [ 211 : 220]
                iA0, iA1, iA2 = 0,0,0;
                iB0, iB1, iB2 = 0,0,0;
                iC0, iC1, iC2 = 0,0,0;
                iD0, iD1, iD2 = 0,0,0;
                iE0, iE1, iE2 = 0,0,0;
                iF0, iF1, iF2 = 0,0,0;
                iG0, iG1, iG2 = 0,0,0;
                iH0, iH1, iH2 = 0,0,0;
                iJ0, iJ1, iJ2 = 0,0,0;
                iK0, iK1, iK2 = 0,0,0;
                for idTen in range(-2, -10, -1):
                    iA0+=self.dataPt[idTen][6];
                    iA1+=(self.dataPt[idTen][6]-self.dataPt[idTen-1][6]);
                    print(iA1)
                    iA2+=(iA1/iA0);
                    iB0+=self.dataPt[idTen][7];
                    iB1+=(self.dataPt[idTen][7]-self.dataPt[idTen-1][7]);
                    iB2+=(iB1/iB0);
                    iC0+=self.dataPt[idTen][8];
                    iC1+=(self.dataPt[idTen][8]-self.dataPt[idTen-1][8]);
                    iC2+=(iC1/iC0);
                    iD0+=self.dataPt[idTen][14];
                    iD1+=(self.dataPt[idTen][14]-self.dataPt[idTen-1][14]);
                    iD2+=(iD1/iD0);                    
                    iE0+=self.dataPt[idTen][15];
                    iE1+=(self.dataPt[idTen][15]-self.dataPt[idTen-1][15]);
                    iE2+=(iE1/iE0);
                    iF0+=self.dataPt[idTen][16];
                    iF1+=(self.dataPt[idTen][16]-self.dataPt[idTen-1][16]);
                    iF2+=(iF1/iF0);
                    iG0+=self.dataPt[idTen][17];
                    iG1+=(self.dataPt[idTen][17]-self.dataPt[idTen-1][17]);
                    iG2+=(iG1/iG0);
                    iH0+=self.dataPt[idTen][18];
                    iH1+=(self.dataPt[idTen][18]-self.dataPt[idTen-1][18]);
                    iH2+=(iH1/iH0);
                    iJ0+=self.dataPt[idTen][19];
                    iJ1+=(self.dataPt[idTen][19]-self.dataPt[idTen-1][19]);
                    iJ2+=(iJ0/iJ0);
                    iK0+=self.dataPt[idTen][20];
                    iK1+=(self.dataPt[idTen][20]-self.dataPt[idTen-1][20]);
                    iK2+=(iK1/iK0);

                self.dataBookMS[self.itr][201]=iA2;
                self.dataBookMS[self.itr][202]=iB2;
                self.dataBookMS[self.itr][203]=iC2;
                self.dataBookMS[self.itr][204]=iD2;
                self.dataBookMS[self.itr][205]=iE2;
                self.dataBookMS[self.itr][206]=iF2;
                self.dataBookMS[self.itr][207]=iG2;
                self.dataBookMS[self.itr][208]=iH2;
                self.dataBookMS[self.itr][209]=iJ0;
                self.dataBookMS[self.itr][210]=iK2;

                print('chk RATES')
                for chkRate in range(211, 221, 1):
                    print(self.dataBookMS[self.itr][chkRate-20])
                    print(self.dataBookMS[self.itr][chkRate-10])
                    if(self.dataBookMS[self.itr][chkRate-20]>self.dataBookMS[self.itr][chkRate-10]): self.dataBookMS[self.itr][chkRate]=1; pass;


                str0=str(self.itr)+",";
                for units in self.dataBookMS[self.itr]:
                    str0+=str(units)+",";
                str0+='\n';
                service.write_file(self.fileName,'{}'.format(str0))  
                break;

            elif(self.idxLoop>10):             

                str4=str(self.itr)+",";
                for units in self.dataBookMS[self.itr]:
                    str4+=str(units)+",";
                service.write_file(self.fileName,'{}'.format(str4));
                offset+=1;
                
            elif(self.idxLoop>100000):
                
                
                if(self.dataBookMS[self.itr][139]==self.dataBookMS[self.itr][148]): self.dataBookMS[self.itr][150]=1;pass;
                elif(self.dataBookMS[self.itr][139]==self.dataBookMS[self.itr][149]): self.dataBookMS[self.itr][151]=-1;pass;
                if(self.dataBookMS[self.itr][128]==self.dataBookMS[self.itr][137]): self.dataBookMS[self.itr][152]=1;pass; 
                elif(self.dataBookMS[self.itr][128]==self.dataBookMS[self.itr][138]): self.dataBookMS[self.itr][153]=-1;pass;
                if(self.dataBookMS[self.itr][117]==self.dataBookMS[self.itr][126]): self.dataBookMS[self.itr][154]=1;pass;
                elif(self.dataBookMS[self.itr][117]==self.dataBookMS[self.itr][127]): self.dataBookMS[self.itr][155]=-1;pass;
                if(self.dataBookMS[self.itr][106]==self.dataBookMS[self.itr][115]): self.dataBookMS[self.itr][156]=1;pass;
                elif(self.dataBookMS[self.itr][106]==self.dataBookMS[self.itr][116]): self.dataBookMS[self.itr][157]=-1;pass;
                
                
                #CHK
                # self.dataBookMS[-1][73]-self.dataBookMS[-1][84]
                if(self.dataBookMS[-1][73]-self.dataBookMS[-1][84]>=self.dataBookMS[self.itr][104]): self.dataBookMS[self.itr][158]=1;pass;
                elif(self.dataBookMS[-1][73]-self.dataBookMS[-1][84]<=self.dataBookMS[self.itr][105]): self.dataBookMS[self.itr][159]=-1;pass;
                
                
                # CHECK
                print(self.itr, self.dataBookMS[self.itr][95], self.dataBookMS[self.itr][104])
                
                if(self.dataBookMS[self.itr][10]>=self.dataBookMS[self.itr][93]): self.dataBookMS[self.itr][160]=1;pass;
                elif(self.dataBookMS[self.itr][10]<=self.dataBookMS[self.itr][94]): self.dataBookMS[self.itr][161]=-1;pass;
                if(self.dataBookMS[self.itr][9]>=self.dataBookMS[self.itr][82]): self.dataBookMS[self.itr][162]=1;pass;
                elif(self.dataBookMS[self.itr][9]<=self.dataBookMS[self.itr][83]): self.dataBookMS[self.itr][163]=-1;pass;
                
                if(self.dataPt[-1+offset][15]==self.dataBookMS[self.itr][71]): self.dataBookMS[self.itr][164]=1;pass;
                elif(self.dataPt[-1+offset][15]==self.dataBookMS[self.itr][72]): self.dataBookMS[self.itr][165]=-1;pass;
                
                if(self.dataPt[-1+offset][16]==self.dataBookMS[self.itr][60]): self.dataBookMS[self.itr][166]=1;pass;
                elif(self.dataPt[-1+offset][16]==self.dataBookMS[self.itr][61]): self.dataBookMS[self.itr][167]=-1;pass;
                
                if(self.dataPt[-1+offset][8]==self.dataBookMS[self.itr][48]): self.dataBookMS[self.itr][168]=1;pass;
                elif(self.dataPt[-1+offset][8]==self.dataBookMS[self.itr][49]): self.dataBookMS[self.itr][169]=-1;pass;
                
                if(self.dataPt[-1+offset][6]==self.dataBookMS[self.itr][37]): self.dataBookMS[self.itr][170]=1;pass;
                elif(self.dataPt[-1+offset][6]==self.dataBookMS[self.itr][38]): self.dataBookMS[self.itr][171]=-1;pass;
                
                if(self.dataPt[-1+offset][7]==self.dataBookMS[self.itr][26]): self.dataBookMS[self.itr][172]=1;pass;
                elif(self.dataPt[-1+offset][7]==self.dataBookMS[self.itr][27]): self.dataBookMS[self.itr][173]=-1;pass;

                rangeF=max(-idx, -10)
                chkA=[0,0,0,0,0,0,0];
                for idxA in range(-2+offset, rangeF+offset, -1):
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][7]):
                        chkA[0]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][9]):
                        chkA[1]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][16]):
                        chkA[2]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][17]):
                        chkA[3]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][18]):
                        chkA[4]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][19]):
                        chkA[5]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][20]):
                        chkA[6]+=1;
                        
                iA=0;
                for idA in range(174, 181, 1):
                    self.dataBookMS[self.itr][idA]=chkA[iA];
                    iA+=1;

                chkB=[0,0,0,0,0,0,0,0,0,0];
                for bIdx in range(-2+offset, rangeF+offset+1, -1):
                    if(self.dataPt[bIdx][6]>self.dataPt[bIdx-1][6]): chkB[0]+=1;pass;
                    if(self.dataPt[bIdx][7]>self.dataPt[bIdx-1][7]): chkB[1]+=1;pass;
                    if(self.dataPt[bIdx][8]>self.dataPt[bIdx-1][8]): chkB[2]+=1;pass;
                    if(self.dataPt[bIdx][14]>self.dataPt[bIdx-1][14]): chkB[3]+=1;pass;
                    if(self.dataPt[bIdx][15]>self.dataPt[bIdx-1][15]): chkB[4]+=1;pass;
                    if(self.dataPt[bIdx][16]>self.dataPt[bIdx-1][16]): chkB[5]+=1;pass;
                    if(self.dataPt[bIdx][17]>self.dataPt[bIdx-1][17]): chkB[6]+=1;pass;
                    if(self.dataPt[bIdx][18]>self.dataPt[bIdx-1][18]): chkB[7]+=1;pass;
                    if(self.dataPt[bIdx][19]>self.dataPt[bIdx-1][19]): chkB[8]+=1;pass;
                    if(self.dataPt[bIdx][20]>self.dataPt[bIdx-1][20]): chkB[9]+=1;pass;
                    
                idB=0;
                for idBin in range(181, 191, 1):
                    self.dataBookMS[self.itr][idBin]=chkB[idB];
                    idB+=1;

                if(idx>2 and len(self.dataPt[-9+offset])>2):
                    self.dataBookMS[self.itr][191]=(self.dataPt[-1+offset][6]-self.dataPt[-2+offset][6])/self.dataPt[-1+offset][6];
                    self.dataBookMS[self.itr][192]=(self.dataPt[-1+offset][7]-self.dataPt[-2+offset][7])/self.dataPt[-1+offset][7];
                    self.dataBookMS[self.itr][193]=(self.dataPt[-1+offset][8]-self.dataPt[-2+offset][8])/self.dataPt[-1+offset][8];
                    self.dataBookMS[self.itr][194]=(self.dataPt[-1+offset][14]-self.dataPt[-2+offset][14])/self.dataPt[-1+offset][14];
                    self.dataBookMS[self.itr][195]=(self.dataPt[-1+offset][15]-self.dataPt[-2+offset][15])/self.dataPt[-1+offset][15]; 
                    self.dataBookMS[self.itr][196]=(self.dataPt[-1+offset][16]-self.dataPt[-2+offset][16])/self.dataPt[-1+offset][16];              
                    self.dataBookMS[self.itr][197]=(self.dataPt[-1+offset][17]-self.dataPt[-2+offset][17])/self.dataPt[-1+offset][17];
                    self.dataBookMS[self.itr][198]=(self.dataPt[-1+offset][18]-self.dataPt[-2+offset][18])/self.dataPt[-1+offset][18];
                    self.dataBookMS[self.itr][199]=(self.dataPt[-1+offset][19]-self.dataPt[-2+offset][19])/self.dataPt[-1+offset][19];
                    self.dataBookMS[self.itr][200]=(self.dataPt[-1+offset][20]-self.dataPt[-2+offset][20])/self.dataPt[-1+offset][20];
                    
                    iA0, iA1, iA2 = 0,0,0;
                    iB0, iB1, iB2 = 0,0,0;
                    iC0, iC1, iC2 = 0,0,0;
                    iD0, iD1, iD2 = 0,0,0;
                    iE0, iE1, iE2 = 0,0,0;
                    iF0, iF1, iF2 = 0,0,0;
                    iG0, iG1, iG2 = 0,0,0;
                    iH0, iH1, iH2 = 0,0,0;
                    iJ0, iJ1, iJ2 = 0,0,0;
                    iK0, iK1, iK2 = 0,0,0;
                    
                    for itmC in range(-1+offset, -9+offset, -1):
                        iA0+=self.dataPt[itmC][6];
                        iA1+=self.dataPt[itmC][6]-self.dataPt[itmC-1][6];
                        iA2+=(iA1/iA0);
                        iB0+=self.dataPt[itmC][7];
                        iB1+=self.dataPt[itmC][7]-self.dataPt[itmC-1][7];
                        iB2+=(iB1/iB0);
                        iC0+=self.dataPt[itmC][8];
                        iC1+=self.dataPt[itmC][8]-self.dataPt[itmC-1][8];
                        iC2+=(iC1/iC0);
                        iD0+=self.dataPt[itmC][14];
                        iD1+=self.dataPt[itmC][14]-self.dataPt[itmC-1][14];
                        iD2+=(iD1/iD0);
                        iE0+=self.dataPt[itmC][15];
                        iE1+=self.dataPt[itmC][15]-self.dataPt[itmC-1][15];
                        iE2+=(iE1/iE0); 
                        iF0+=self.dataPt[itmC][16];
                        iF1+=self.dataPt[itmC][16]-self.dataPt[itmC-1][16];
                        iF2+=(iF1/iF0);
                        iG0+=self.dataPt[itmC][17];
                        iG1+=self.dataPt[itmC][17]-self.dataPt[itmC-1][17];
                        iG2+=(iG1/iG0);
                        iH0+=self.dataPt[itmC][18];
                        iH1+=self.dataPt[itmC][18]-self.dataPt[itmC-1][18];
                        iH2+=(iH1/iH0);
                        iJ0+=self.dataPt[itmC][19];
                        iJ1+=self.dataPt[itmC][19]-self.dataPt[itmC-1][19];
                        iJ2+=(iJ1/iJ0);
                        iK0+=self.dataPt[itmC][20];
                        iK1+=self.dataPt[itmC][20]-self.dataPt[itmC-1][20];
                        iK2+=(iK1/iK0);

                    self.dataBookMS[self.itr][201]=iA2;
                    self.dataBookMS[self.itr][202]=iB2;
                    self.dataBookMS[self.itr][203]=iC2;
                    self.dataBookMS[self.itr][204]=iD2;
                    self.dataBookMS[self.itr][205]=iE2;
                    self.dataBookMS[self.itr][206]=iF2;
                    self.dataBookMS[self.itr][207]=iG2;
                    self.dataBookMS[self.itr][208]=iH2;
                    self.dataBookMS[self.itr][209]=iJ2;
                    self.dataBookMS[self.itr][210]=iK2;

                    print('chk 211, 221, 1')
                    for chkRate in range(211, 221, 1):
                        print(self.dataBookMS[self.itr][chkRate-20])
                        print(self.dataBookMS[self.itr][chkRate-10])
                        if(self.dataBookMS[self.itr][chkRate-20]>self.dataBookMS[self.itr][chkRate-10]): self.dataBookMS[self.itr][chkRate]=1; pass;
                    pass;
                                
                #bar data section
                #chkHi.append(self.dataBookMS[self.itr+offset][9]);
                #iH=73;
                #for hoteX in range(-2, -11, -1):
                #    self.dataBookMS[self.itr][iH]=self.dataBookMS[self.itr+offset][9];
                #    chkHi.append(self.dataBookMS[self.itr+offset][9]);
                #    iH+=1;
                #self.dataBookMS[self.itr][82]=max(chkHi);
                #self.dataBookMS[self.itr][83]=min(chkHi);
                #
                #chkLo.append(self.dataBookMS[self.itr+offset][10]);
                #iH=84;
                #for hoteX in range(-2, -11, -1):
                #    self.dataBookMS[self.itr][iH]=self.dataBookMS[self.itr+offset][10];
                #    chkLo.append(self.dataPt[hoteX+offset][10]);
                #    iH+=1;
                #self.dataBookMS[self.itr][93]=max(chkLo)
                #self.dataBookMS[self.itr][94]=min(chkLo)
                
        #barB=md.bar.minute(start=-20, end=None, include_empty=False, include_extended=True, bar_size=2, today_only=True)        
        #rangeMSB = min(len(barB.timestamp), len(barB.askvol), len(barB.bidvol), len(barB.bvwap), len(barB.close), len(barB.count), len(barB.high), len(barB.low), len(barB.open), len(barB.spread), len(barB.volume))
        #for idxB in range(0, rangeMSB, 1):
        #    self.dataBookMSB.append([self.symbol, 20,  self.itr, barB.timestamp[idxB], barB.askvol[idxB], barB.bidvol[idxB], barB.bvwap[idxB], barB.close[idxB], barB.open[idxB], barB.high[idxB], barB.low[idxB], barB.count[idxB], barB.spread[idxB], barB.volume[idxB], barB.high[idxB]-barB.low[idxB], barB.close[idxB]-barB.open[idxB], max(barB.bvwap[idxB], barB.close[idxB], barB.open[idxB], barB.high[idxB]) , self.dataPt[-1][7]])
        #    if(idxB!=0):
        #        self.dataBookMSB[idxB][17]=self.dataBookMSB[idxB][whatever] and self.dataBookMSB[idxB-1][whatever] 
        #
        #print(len(self.dataBookMS[self.itr]))#print("STR2")#str2=str(self.itr-1);#for units in self.dataBookMS[self.itr-1]: #    str2+=str(units)+","; #str2+='\n';#print(str2)
    def on_fill(self, event, md, order, service, account):
        if(account[self.symbol].position.shares==0):
            self.cover=0;
            pass
        #if(event.user_tag==15):
        #    cvrPrice=event.price*0.999;
        #    cvr15 = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=150, price=cvrPrice, user_key=151, allow_multiple_pending=40);
        #if(event.user_tag==7):
        #    cvrPrice=event.price*0.999;
        #    cvr7 = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=70, price=cvrPrice, user_key=157, allow_multiple_pending=40);
        #if(event.user_tag==8):
        #    cvrPrice=event.price*0.999;
        #    cvr7 = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=80, price=cvrPrice, user_key=158, allow_multiple_pending=40);
    def on_finish(self, md, order, service, account):
        print(self.status)
        filenameDT=self.symbol+"-DT.txt"
        #strLoop=self.symbol+"\n"
        #print('onFinish')
        #print(len(self.dataBookMS))
        #print('start\t', strLoop)
        #print(self.dataBookMS[-1])
        #print(self.dataBookMS[-2])
        #print(self.dataBookMS[-3])
        #for aLoop in self.dataBookMS:
        #    print('aloop\t', aLoop)
        #    if(type(aLoop)!='int'):
        #        for diLoop in aLoop:
        #            strLoop+=str(diLoop)+", "
        #    strLoop+="\n"
        #service.write_file(filenameDT, '{}'.format(strLoop))
