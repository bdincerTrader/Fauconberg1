from cloudquant.interfaces import Strategy
import time, datetime, random

class Gr8Script4193a445a9a444cd9b5300401f29d56a(Strategy):
    __script_name__ = 'gpsFauconberg'
    
    
    qqqCHG=spyCHG=0;
    #tickerItrA = ['BKNG','GS','MS','CMG','DDS','ELV','EQIX','HUBS','MELI','MSTR','SWAV','SPY','QQQ'];
    tickerItrB = ['ADBE','ASML','AVGO','AZO','BIO','BKNG','BLK','GS','MS','COST','CMG','DDS','DECK','ELV','EQIX','FCNCA','FDS','FICO','FNGU','GWW','HUBS','HUM','IDXX','IIVI','INTU','KLAC','LRCX','MDB','MDGL','MELI','MPWR','MSCI','MSTR','MTD','NFLX','NOW','NVDA','ORLY','REGN','SAIA','SEDG','SMCI','SNPS','SOXX','SWAV','TDG','TMO','TSLA','ULTA','UNH','URI','SPY','QQQ'];
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in Gr8Script4193a445a9a444cd9b5300401f29d56a.tickerItrB;
        #return symbol in []Gr8Script7440a7b776ad48b280810fd86a9748af.tickerItrB;
        # return md.stat.prev_close>50.00 and md.stat.atr>5 or symbol=="SPY" or symbol=="QQQ";
        
    def on_start(self, md, order, service, account):
    
        self.systemRevolver=[0];
        self.spyCHG=0;
        self.qqqCHG=0;
        self.closed=0;
        self.systemLong=0;
        self.systemShort=0;
        self.systemCheckA=0;
        self.motionPM=[0.00] * 106;
        self.orderPM=[0.00] * 44;
        self.sysOne=[];
        self.sysTwo=[];
        self.fileName=self.symbol+'.txt';
        self.sysOne.append(self.motionPM);
        self.sysTwo.append(self.orderPM);
        self.crrTrack=[0.00];
        self.systemItr=0;
        self.systemType=0;
        self.systemUP=[0];
        self.systemDOWN=[0];
        self.levelThree=[0];
        self.ATR_scR=0; self.mot_scR=0; self.xxl_scR=0; self.ATR_scRp=0; self.mot_scRp=0; self.xxl_scRp=0;
        self.satisfied=0;
        self.ATR_TypeA=0; self.ATR_TypeB=0; self.motionA=0.0; self.motionB=0.0; self.motionX=0.0; self.motionY=0.0;
        self.filledSell=0;
        self.netShortUnit=0;
        self.filledBuy=0;
        self.key=0;
        self.mktSpread=[0.00];
        self.mktTrades=[md.L1.last];
        self.priceBook=[md.L1.last];
        self.netShortPx=0;
        self.orderBuy=self.orderSell=self.avgAllocationRate=[];
        self.bot=self.sold=0;
        self.systemStatus=0;
        self.neutral=self.neutralized=self.allocationRate=self.orderSession=self.orderBalance=self.maxBidRTE=self.maxAskRTE=self.minBidRTE=self.minAskRTE=0;
        self.motion = md.stat.atr;
        self.p1 = self.motion*0.01;
        self.p5 = self.motion*0.15;
        self.active = self.motion*1.5;
        self.zero = md.stat.prev_close;
        self.triggerHigh = self.motion-self.zero;
        self.triggerLow = self.zero-self.motion;
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(minutes=1), timer_id="motionDetected");
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=10), timer_id="status");
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=3), timer_id = "eod")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=4), timer_id = "eod_pending")
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=5);
        self.chk_SPY=self.chk_QQQ = 0;
        self.chkATR=self.motion*.02;
        self.TradeDate=service.time_to_string(service.system_time)
        print(self.TradeDate)
        self.ask=self.bid=[];
        self.askRate=self.bidRate=[];
        self.ebft=0;
        self.mktTrades.append(self.zero);
        self.orderItr=0;
        print(self.motion, self.p1, self.p5, self.active, self.zero, self.triggerHigh, self.triggerLow, self.chkATR)
        
    def on_timer(self, event, md, order, service, account):
    
        if(event.timer_id=="status"):
            try:
                last=md.L1.last;
                bid=md.L1.bid;
                ask=md.L1.ask;
                
                if(last*1>0 and bid*1>0 and ask*1>0):
                    midRange=(last+bid+ask)/3;
                    self.priceBook.append(midRange);
                    return; 
            except:
                return;
            return;
            
        if(event.timer_id=="eod_pending"):
            order.cancel(self.symbol)
        
        if(event.timer_id=="eod"):
            if(account[self.symbol].position.shares<0):
                order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                pass;
            if(account[self.symbol].position.shares>0):
                order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                pass;
                
        if(self.systemStatus==1):
            self.satisfied=0;
            self.bot=self.filledBuy=0;
            self.sold=self.filledSell=0;
            self.orderSession=0;
            self.orderBalance=0;
            order.cancel(self.symbol);
            self.systemStatus=0;
            pass;

        if(self.systemCheckA==1):
            order.cancel(self.symbol);
            self.systemCheckA=0;

        def printBars(_stage, _location, _currentRate, _mxSpr, _mnSpr):                
            print(_stage, 'b', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.spyCHG, self.qqqCHG, _currentRate, self.ATR_TypeB, self.motionA,  self.motionY, self.ATR_TypeA, self.motionB, self.motionX,  '212', self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), mxSpr, mnSpr, 212, self.orderSession, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            return
        
        def printAction(_action, _location, _currentRate, _scr, _scrP, _motion, _TRAJECTORY):
            print(_action, 'a', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.spyCHG, self.qqqCHG, _currentRate, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, _TRAJECTORY, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), _scr, _scrP, _motion, self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            return

        def neutralSystem(block, brakeSystem, brakeIdx, chkPrints, currentLocation, currentRate, mxSpr, mnSpr):
            ft=0;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                ft-=1;
                self.sysOne[self.systemItr][block]=brakeIdx;
                printBars('pMax', brakeSystem, currentLocation, mxSpr, mnSpr);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                ft+=1;
                self.sysOne[self.systemItr][block+1]=brakeIdx;
                printBars('pMin', brakeSystem, currentLocation, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                ft-=1;
                self.sysOne[self.systemItr][block+2]=brakeIdx;
                printBars('nMax', brakeSystem, currentLocation, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                ft+=1;
                self.sysOne[self.systemItr][block+2]=brakeIdx;
                printBars('nMin', brakeSystem, currentLocation, mxSpr, mnSpr);
                pass;
            if(ft==0):
                self.neutral+=1;
                self.sysOne[self.systemItr][32]=self.neutral;
                printBars('FT_neutral', brakeSystem, currentLocation, mxSpr, mnSpr);
                pass;
            return ft;

        def marketSpread(b, a):
            self.key=1;
            #print('mk spr: ', self.symbol, b, a);
            if(((a+b)/2)>b and ((a+b)/2)<a):
                self.mktSpread.append(a-b);
            return self.mktSpread;
        
        self.neutral=0;
        self.systemItr+=1;
        #print(self.sysOne);
        self.sysOne.append(self.motionPM);
        currentBid = md.L1.bid;
        currentAsk = md.L1.ask;
        self.sysOne[self.systemItr][0]=0+self.systemItr;
        self.sysOne[self.systemItr][1]='timer';
        self.sysOne[self.systemItr][2]=self.symbol;
        self.sysOne[self.systemItr][3]=service.time_to_string(service.system_time);
        self.sysOne[self.systemItr][4]=event.timestamp;
        self.sysOne[self.systemItr][5]=self.orderSession;
        self.sysOne[self.systemItr][6]=self.zero;
        
        self.sysOne[self.systemItr][33]=self.p1;
        self.sysOne[self.systemItr][34]=self.p5;
        
        if(currentBid*1<self.motion):
            print('qCheckBID');
            return;
            
        if(currentAsk*1<self.motion):
            print('qCheckASK');
            return;
        
        self.systemType=0;
        self.ATR_scR=0; self.mot_scR=0; self.xxl_scR=0; 
        self.ATR_scRp=0; self.mot_scRp=0; self.xxl_scRp=0; 
        self.ATR_scR=0; self.mot_scR=0;
        self.motionA=0.0; self.motionB=0.0; self.ATR_TypeA=0.0; self.ATR_TypeB=0.0; self.motionX=0.0; self.motionY=0.0;        
        
        self.ask.append(currentAsk); 
        self.bid.append(currentBid); 
        
        ## check rate of chance in [currentLocation]
        currentLocation =  currentBid - self.zero; 
        currentRate = currentLocation/self.zero;
        self.sysOne[self.systemItr][1]='timer';
        self.sysOne[self.systemItr][7]=currentLocation;
        self.sysOne[self.systemItr][8]=currentRate;
        self.sysOne[self.systemItr][9]=currentLocation-self.sysOne[self.systemItr-1][7];
        
        i=0;rate=0;
        for accRate in self.sysOne:
            # print(accRate[9]);
            rate+=accRate[9];
            i+=1;
        
        avgCurrent=rate/i;
        self.crrTrack.append(avgCurrent)
        self.sysOne[self.systemItr][10]=avgCurrent;
        
        self.sysOne[self.systemItr][11]=max(self.crrTrack);
        self.sysOne[self.systemItr][12]=avgCurrent-self.sysOne[self.systemItr-1][10];
        
        # price book
        checkRate=0;i=0;
        for idx in self.priceBook:
            checkRate+=(idx-self.zero);
            i+=1;
        status=checkRate/i;
        self.levelThree.append(status);
        statusChg=status-self.levelThree[-2];
        
        if(len(self.priceBook)>2 and len(self.sysOne[self.systemItr])>2):
            self.sysOne[self.systemItr][19]=self.priceBook[-1];
            self.sysOne[self.systemItr][20]=self.priceBook[-1]-self.priceBook[-2];
            self.sysOne[self.systemItr][21]=self.priceBook[-1]-self.priceBook[-2]/self.priceBook[-2];
            self.sysOne[self.systemItr][22]=status;
            self.sysOne[self.systemItr][23]=statusChg;
        else:
            self.sysOne[self.systemItr][19]=0;
            self.sysOne[self.systemItr][20]=0;
            self.sysOne[self.systemItr][21]=0;
            self.sysOne[self.systemItr][22]=0;
            self.sysOne[self.systemItr][23]=0;
        
        ## TRIGGER. change in avg rate of change.
        
        if(statusChg>self.levelThree[-2]): self.sysOne[self.systemItr][24]=1; pass;
        else: self.sysOne[self.systemItr][24]=0; pass;                  
        self.sysOne[self.systemItr][25]=md.L1.bid;
        self.sysOne[self.systemItr][26]=md.L1.ask;

        chkSPY = ((md['SPY'].L1.bid) - (md['SPY'].stat.prev_close));
        chkSPYRTE = chkSPY/(md['SPY'].stat.prev_close);
        self.spyCHG=chkSPYRTE;
        chkQQQ = ((md['QQQ'].L1.bid) - (md['QQQ'].stat.prev_close));
        chkQQQRTE = chkQQQ/(md['QQQ'].stat.prev_close);
        self.qqqCHG=chkQQQRTE;

        if(self.symbol=='SPY'):
            self.spyCHG=currentLocation/self.zero;
            return;
        elif(self.symbol=='QQQ'):
            self.qqqCHG=currentLocation/self.zero;
            return;
        else: 
            self.chk_SPY = currentRate - self.spyCHG;
            self.chk_QQQ = currentRate - self.qqqCHG;
            pass;
        
        self.sysOne[self.systemItr][27]=self.chk_SPY;
        self.sysOne[self.systemItr][28]=self.chk_QQQ;
        self.sysOne[self.systemItr][29]=self.chk_SPY-self.sysOne[self.systemItr-1][27];
        self.sysOne[self.systemItr][30]=self.chk_QQQ-self.sysOne[self.systemItr-1][28];

        if(currentAsk-currentBid>self.motion):
            print('qCheck');
            return;

        #print(self.priceBook)
        self.priceBook.append((currentAsk+currentBid+self.mktTrades[-1])/3);
        self.ebft=0;
        
        if(currentLocation > self.motion):
            self.ebft+=1;
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread);
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];mnSpr=self.mktSpread[-1];
                pass;
                

            
            self.ATR_TypeA=1;
            self.ATR_scRp+=1;
            self.sysOne[self.systemItr][1]='ATR1';
            self.sysOne[self.systemItr][17]=mxSpr;
            self.sysOne[self.systemItr][18]=mnSpr;
            self.sysOne[self.systemItr][31]=self.ebft;
            self.sysOne[self.systemItr][66]=self.ATR_scRp;
            self.sysOne[self.systemItr][69]=1;

            printBars('ATR1', currentLocation, currentRate, mxSpr, mnSpr);
            # lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
            #pathA = '{}.{}'.format("ATRA", self.file_name);
            #service.write_file(pathA, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.spyCHG, self.qqqCHG, currentRate));
            if(currentBid+self.p1 > md.L1.daily_high):
                self.ATR_TypeA=1.1;
                self.ATR_scRp+=1;
                self.neutral+=1;
                self.ebft-=1;
                self.sysOne[self.systemItr][1]='ATR1.1';
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][32]=self.neutral;
                self.sysOne[self.systemItr][66]=self.ATR_scRp;
                self.sysOne[self.systemItr][70]=1;
                
                # lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price= self.pxBID, user_key=111, allow_multiple_pending=40);
                printBars('ATR1-B', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            pass;
            
        if(currentLocation > self.active):
            self.ebft+=1; 
            
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk); 

            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;

            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];mnSpr=self.mktSpread[-1];
                pass;

            self.ATR_TypeB=2;
            self.ATR_scRp+=1;
            
            self.sysOne[self.systemItr][1]='ATR2';
            self.sysOne[self.systemItr][17]=mxSpr;
            self.sysOne[self.systemItr][18]=mnSpr;
            self.sysOne[self.systemItr][31]=self.ebft;
            self.sysOne[self.systemItr][66]=self.ATR_scRp;
            self.sysOne[self.systemItr][71]=1;
            
            printBars('ATR2', currentLocation, currentRate, mxSpr, mnSpr);
            #pathB = '{}.{}'.format("ATRB", self.file_name);
            #service.write_file(pathB, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.spyCHG, self.qqqCHG, currentRate));
            # lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price= self.pxBID, user_key=111, allow_multiple_pending=40);
            if(currentBid+self.p1 > md.L1.daily_high):
                self.ATR_TypeB=2.1;
                self.ATR_scRp+=1;
                self.neutral+=1;
                self.ebft-=1;
                self.sysOne[self.systemItr][1]='ATR2.1';
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][32]=self.neutral;
                self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysOne[self.systemItr][66]=self.ATR_scRp;
                self.sysOne[self.systemItr][72]=1;
                printBars('ATR2B', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            pass;    

        if(currentLocation < -self.motion):
            self.ebft-=1;
            
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk); 
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;

            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;
                
            self.ATR_TypeB=3;
            self.ATR_scR-=1;
            
            self.sysOne[self.systemItr][1]='ATR3';
            self.sysOne[self.systemItr][17]=mxSpr;
            self.sysOne[self.systemItr][18]=mnSpr;
            self.sysOne[self.systemItr][31]=self.ebft;
            self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
            self.sysOne[self.systemItr][63]=self.ATR_scR;
            self.sysOne[self.systemItr][57]=1;
                
            printBars('ATR3', currentLocation, currentRate, mxSpr, mnSpr);
            #pathC = '{}.{}'.format("ATRC", self.file_name);
            #service.write_file(pathC, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.spyCHG, self.qqqCHG, currentRate));
                    
            if(currentAsk-self.p1 < md.L1.daily_low):
                self.ATR_TypeB=3.1;
                self.ATR_scR-=1;
                self.ebft+=1;
                self.neutral+=1;
                self.sysOne[self.systemItr][1]='ATR3.1';
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][32]=self.neutral;
                self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysOne[self.systemItr][63]=self.ATR_scR;
                self.sysOne[self.systemItr][58]=1;
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                printBars('ATR3-B', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            pass;
            
        if(currentLocation < -self.active):
            self.ebft-=1;
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk);
            
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;
                
            self.ATR_TypeB=4;
            self.ATR_scR-=1;
            self.sysOne[self.systemItr][1]='ATR4';
            self.sysOne[self.systemItr][17]=mxSpr;
            self.sysOne[self.systemItr][18]=mnSpr;
            self.sysOne[self.systemItr][31]=self.ebft;
            self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
            self.sysOne[self.systemItr][63]=self.ATR_scR;
            self.sysOne[self.systemItr][59]=1;
            
            printBars('ATR4', currentLocation, currentRate, mxSpr, mnSpr);
            #pathD = '{}.{}'.format("ATRD", self.file_name);
            #service.write_file(pathD, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.spyCHG, self.qqqCHG, currentRate));
            # offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)

            if(currentAsk-self.p1 < md.L1.daily_low):
                self.ATR_TypeB=4.1;
                self.ATR_scR-=1;
                self.ebft+=1;
                self.neutral+=1;
                
                self.sysOne[self.systemItr][1]='ATR4.1';
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][32]=self.neutral;
                self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysOne[self.systemItr][63]=self.ATR_scR;
                self.sysOne[self.systemItr][60]=1;
                
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                printBars('ATR4-B', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            pass;
            
        if(self.chk_SPY > 0.02):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;
                       
            if(currentRate<self.spyCHG):
                self.ebft-=1;
                self.motionA=5.1;
                self.mot_scR-=1;
                self.sysOne[self.systemItr][1]='5.1';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysOne[self.systemItr][62]=self.mot_scR;
                self.sysOne[self.systemItr][49]=1;
                printBars('motion5.1', currentLocation, currentRate, mxSpr, mnSpr);
                # offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                FT = neutralSystem(45, 5.1, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)

                if(self.chk_SPY > 0.04):
                    self.xxl_scR+=1;
                    self.ebft-=1;
                    self.neutral+=1;
                    self.sysOne[self.systemItr][1]='5.1b';
                    self.sysOne[self.systemItr][31]=self.ebft;
                    self.sysOne[self.systemItr][32]=self.neutral;
                    self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                    self.sysOne[self.systemItr][61]=self.xxl_scR;
                    self.sysOne[self.systemItr][50]=1;
                    printBars('motion5.1b', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(45, 5.11, 2, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)
                    pass;
                pass;
                
            if(currentRate>self.spyCHG):
                self.ebft+=1;
                self.motionA=5.2;
                self.mot_scRp+=1;
                self.sysOne[self.systemItr][1]='5.2';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysOne[self.systemItr][67]=self.mot_scRp;
                self.sysOne[self.systemItr][73]=1;
                printBars('motion5.2', currentLocation, currentRate, mxSpr, mnSpr);
                #lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
                FT = neutralSystem(81, 5.2, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)
                
                if(self.chk_SPY > 0.04):
                    self.xxl_scRp+=1;
                    self.ebft-=1;
                    self.neutral+=1;
                    self.sysOne[self.systemItr][1]='5.2b';
                    self.sysOne[self.systemItr][31]=self.ebft;
                    self.sysOne[self.systemItr][32]=self.neutral;
                    self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                    self.sysOne[self.systemItr][68]=self.xxl_scRp;
                    self.sysOne[self.systemItr][74]=1;
                    printBars('motion5-B', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(81, 5.21, 2, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)
                    pass;
                pass;
            pass;    
            
        if(self.chk_SPY < -0.02):
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk); 

            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;

            if(currentRate<self.spyCHG):
                self.ebft-=1;
                self.motionA=6.1;
                self.mot_scR-=1;
                self.sysOne[self.systemItr][1]='6.1';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysOne[self.systemItr][62]=self.mot_scR;
                self.sysOne[self.systemItr][51]=1;
                printBars('motion6.1', currentLocation, currentRate, mxSpr, mnSpr);
                FT = neutralSystem(41, 6.1, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)
                pass;
                
                if(self.chk_SPY < -0.04):
                    self.xxl_scR-=1;
                    self.neutral+=1;
                    self.ebft-=1;
                    self.sysOne[self.systemItr][1]='6.1b';
                    self.sysOne[self.systemItr][31]=self.ebft;
                    self.sysOne[self.systemItr][32]=self.neutral;
                    self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                    self.sysOne[self.systemItr][61]=self.xxl_scRp;
                    self.sysOne[self.systemItr][52]=1;
                    printBars('motion6.1b', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(41, 6.11, 2, chkPrints, currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass;
            
                
            if(currentRate>self.spyCHG):
                self.ebft+=1;
                self.motionA=6.2;
                self.mot_scRp+=1;
                self.sysOne[self.systemItr][1]='6.2';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysOne[self.systemItr][67]=self.mot_scRp;
                self.sysOne[self.systemItr][75]=1;
                printBars('motion6.2', currentLocation, currentRate, mxSpr, mnSpr);
                FT = neutralSystem(85, 6.2, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr);
                pass;
                
                if(self.chk_SPY < -0.04):
                    self.motionX=6.3;
                    self.xxl_scRp+=1;
                    self.neutral+=1;
                    self.ebft-=1;
                    self.sysOne[self.systemItr][1]='6.2b';
                    self.sysOne[self.systemItr][31]=self.ebft;
                    self.sysOne[self.systemItr][32]=self.neutral;
                    self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                    self.sysOne[self.systemItr][68]=self.xxl_scRp;
                    self.sysOne[self.systemItr][75]=1;
                    printBars('motion6-B', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(85, 6.21, 3, chkPrints, currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass;
            pass;
            
        if(self.chk_QQQ > 0.02):
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk); 
            mxSpr=mnSpr=chkPrints=0;
            
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;

            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
                
            if(currentRate<self.qqqCHG):
                self.ebft-=1;
                self.motionB=7.1;
                self.mot_scR-=1;
                printBars('motion7.1', currentLocation, currentRate, mxSpr, mnSpr);
                self.sysOne[self.systemItr][1]='7.1';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysOne[self.systemItr][62]=self.mot_scR;
                self.sysOne[self.systemItr][53]=1;
                FT = neutralSystem(37, 7.1, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)
                
                if(self.chk_QQQ > 0.04):
                    self.motionX=7.3;
                    self.xxl_scR-=1;
                    self.neutral+=1;
                    self.ebft-=1;
                    self.sysOne[self.systemItr][1]='7.1b';
                    self.sysOne[self.systemItr][31]=self.ebft;
                    self.sysOne[self.systemItr][32]=self.neutral;
                    self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                    self.sysOne[self.systemItr][61]=self.xxl_scR;
                    self.sysOne[self.systemItr][54]=1;
                    printBars('motion6-B', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(37, 7.11, 2, chkPrints, currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass;
                
            if(currentRate>self.qqqCHG):
                self.ebft+=1;
                self.motionB=7.2;
                self.mot_scRp+=1;
                self.sysOne[self.systemItr][1]='7.2';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysOne[self.systemItr][67]=self.mot_scRp;
                self.sysOne[self.systemItr][77]=1;
                printBars('motion7.2', currentLocation, currentRate, mxSpr, mnSpr);
                FT = neutralSystem(89, 7.2, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)
                
                if(self.chk_QQQ > 0.04):
                    self.motionY=7.3;
                    self.xxl_scRp+=1;
                    self.neutral+=1;
                    self.ebft-=1;
                    self.sysOne[self.systemItr][1]='7.2b';
                    self.sysOne[self.systemItr][31]=self.ebft;
                    self.sysOne[self.systemItr][32]=self.neutral;
                    self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                    self.sysOne[self.systemItr][68]=self.xxl_scRp;
                    self.sysOne[self.systemItr][78]=2;
                    printBars('motion6-B', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(89, 7.21, 2, chkPrints, currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass;
            pass; 
            
        if(self.chk_QQQ < -0.02):

            mxSpr=mnSpr=chkPrints=0;
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk); 

            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;
                
            if(currentRate<self.qqqCHG):
                self.ebft-=1;
                self.motionB=8.1;
                self.mot_scR-=1;
                self.sysOne[self.systemItr][1]='8.1';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysOne[self.systemItr][62]=self.mot_scR;
                self.sysOne[self.systemItr][55]=1;
                printBars('motion8.1', currentLocation, currentRate, mxSpr, mnSpr);
                FT = neutralSystem(33, 8.1, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)

                if(self.chk_QQQ < -0.04):
                    self.motionX=8.3;
                    self.xxl_scR-=1;
                    self.neutral+=1;
                    self.ebft-=1;
                    self.sysOne[self.systemItr][1]='8.1b';
                    self.sysOne[self.systemItr][31]=self.ebft;
                    self.sysOne[self.systemItr][32]=self.neutral;
                    self.sysOne[self.systemItr][64]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                    self.sysOne[self.systemItr][61]=self.xxl_scR;
                    self.sysOne[self.systemItr][56]=1;
                    printBars('motion8.1b', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(33, 8.11, 2, chkPrints, currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass;

            if(currentRate>self.qqqCHG):
                self.ebft+=1;
                self.motionB=8.2;
                self.mot_scRp+=1;
                self.sysOne[self.systemItr][1]='8.2';
                self.sysOne[self.systemItr][17]=mxSpr;
                self.sysOne[self.systemItr][18]=mnSpr;
                self.sysOne[self.systemItr][31]=self.ebft;
                self.sysOne[self.systemItr][65]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysOne[self.systemItr][67]=self.mot_scRp;
                self.sysOne[self.systemItr][79]=1;
                printBars('motion8.2', currentLocation, currentRate, mxSpr, mnSpr);
                FT = neutralSystem(93, 8.2, 1, chkPrints, currentLocation, currentRate, mxSpr, mnSpr)

                if(self.chk_QQQ < -0.04):
                    self.motionY=8.3;
                    self.xxl_scRp+=1;
                    self.neutral+=1;
                    printBars('motion8.2b', currentLocation, currentRate, mxSpr, mnSpr);
                    FTB = neutralSystem(93, 8.21, 2, chkPrints, currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass;
            pass;
            
        if(self.key==1 and event.timestamp<self.illiquid_time): 
            
            self.neutralized+=self.neutral;
            s=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
            n=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
            
            #print('ebft',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.spyCHG, self.qqqCHG, currentRate, s, n,  self.neutralized,   self.neutral, self.ebft, self.orderBalance);
            printAction('key', currentLocation, currentRate, s, n, 212, 'ACTION');
                                
            sAction=0;
            if(abs(self.ATR_scR+self.mot_scR+self.xxl_scR)<self.systemDOWN[-1]):
                sAction=3;
                pass;
            elif(abs(self.ATR_scR+self.mot_scR+self.xxl_scR)>self.systemDOWN[-1]):
                sAction=2;
                pass;
            elif(abs(self.ATR_scR+self.mot_scR+self.xxl_scR)==self.systemDOWN[-1]):
                sAction=1;
                pass;

            nAction=0;
            if(self.ATR_scRp+self.mot_scRp+self.xxl_scRp<self.systemUP[-1]):
                nAction=3;
                pass;
            elif(self.ATR_scRp+self.mot_scRp+self.xxl_scRp>self.systemUP[-1]):
                nAction=2;
                pass;
            elif(self.ATR_scRp+self.mot_scRp+self.xxl_scRp==self.systemUP[-1]):
                nAction=1;
                pass;
            self.systemUP.append(n);            
            self.systemDOWN.append(s);

            
            if(self.ebft<0 and s>=3):
            
                self.systemShort=1;
                
                # SHORT
                if(self.systemShort==1 and self.systemLong==1):
                    return;
                    
                self.orderItr+=1;
                self.sysTwo.append(self.orderPM);
                
                short_position = account[self.symbol].position.shares;
                self.ebft+=(self.ATR_scR+self.mot_scR+self.xxl_scR)
                printAction('ebft(-)', currentLocation, currentRate, s, n, sAction, 'DOWN');
                
                self.bot+=self.neutral;
                self.sold+=self.ebft;
                self.orderSession+=1;
                self.orderBalance+=(self.ebft+self.neutral);
                self.allocationRate+=abs(self.ebft)/self.orderSession;
                self.orderSell.append([self.symbol, abs(self.ebft)]);
                self.orderBuy.append([self.symbol, self.neutral]);
                
                lvlDOWN=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
                lvlUP=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                
                
                self.sysTwo[self.orderItr][0]=self.orderItr;
                self.sysTwo[self.orderItr][1]=self.systemItr;
                self.sysTwo[self.orderItr][2]=self.orderSession;
                self.sysTwo[self.orderItr][3]=self.symbol;
                self.sysTwo[self.orderItr][4]=self.ebft;
                self.sysTwo[self.orderItr][5]=self.neutral;
                self.sysTwo[self.orderItr][6]=self.orderBalance;
                self.sysTwo[self.orderItr][7]=self.bot;
                self.sysTwo[self.orderItr][8]=self.sold;
                self.sysTwo[self.orderItr][9]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysTwo[self.orderItr][10]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysTwo[self.orderItr][11]=account[self.symbol].position.shares;
                self.sysTwo[self.orderItr][12]=self.filledBuy;
                self.sysTwo[self.orderItr][13]=self.filledSell;
                
                spot1=spot2=spot3=spot4=spot5=spot6=spot7=spot8=0;
                
                if(len(self.levelThree)>2):
                    spot1=self.levelThree[-1];
                    spot2=self.levelThree[-2];
                    spot3=self.levelThree[-3];
                    spot4=sum(self.levelThree[-3:])/3;
                    
                    spot5=self.priceBook[-1];
                    spot6=self.priceBook[-2];
                    spot7=self.priceBook[-3];
                    spot8=sum(self.priceBook[-3:])/3;
                    print('\n[-]ebft','ct', 'session', 'position', 'tkr', 'prior', 'gps', 'clear','bid', 'last', 'ask', 'ebft', 'neutral', 'allocationRate', '[-]','[-L]','[+]','[+L]','long_bal', 'statusShort','statusUpdate', 'gps', 'b', 's', 'B','S','[rate]','[rate-1]','[rate-2]','[rateAVG]','[n]','[n-1]','[n-2]','[n_AVG]');
                    print('down0.0', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                    pass;
                    
                # SHORT  
                if(account[self.symbol].unrealized_pl.entry_pl>5000):
                    return order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                    
                if(account[self.symbol].unrealized_pl.entry_pl>2500):
                    return order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                    
                if(account.realized_mtm_pl>2000):
                    if(abs(account[self.symbol].position.shares)>0):
                        return order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                    
                print('down0.1', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                
                # SHORT  
                pendingOrderBook=account[self.symbol].pending.orders;
                pendingOrderUnit=len(pendingOrderBook);
                self.sysTwo[self.orderItr][14]=pendingOrderUnit;
                shrtVal=buyVal=0;
                sellShrs=buyShrs=0;
                while(pendingOrderUnit>0):
                    pendingOrderUnit-=1;
                    caseOrder=pendingOrderBook[pendingOrderUnit];
                    if(caseOrder.shares<0):
                        self.sysTwo[self.orderItr][15]+=1;
                        self.sysTwo[self.orderItr][16]+=caseOrder.shares;
                        self.sysTwo[self.orderItr][17]+=(caseOrder.price*caseOrder.shares);
                        shrtVal+=(caseOrder.price*caseOrder.shares);
                        sellShrs+=caseOrder.shares;
                        pass;
                        
                    if(caseOrder.shares>0):
                        self.sysTwo[self.orderItr][23]+=1;
                        self.sysTwo[self.orderItr][24]+=caseOrder.shares;
                        self.sysTwo[self.orderItr][25]+=(caseOrder.price*caseOrder.shares);
                        buyVal+=(caseOrder.price*caseOrder.shares);
                        buyShrs+=caseOrder.shares;
                        pass;
                
                if(sellShrs!=0):
                    self.sysTwo[self.orderItr][18]=sellShrs;
                    self.sysTwo[self.orderItr][19]=shrtVal;
                    self.sysTwo[self.orderItr][20]=shrtVal/sellShrs;
                    self.sysTwo[self.orderItr][21]=self.sysTwo[self.orderItr][17]-shrtVal;
                    self.sysTwo[self.orderItr][22]=self.sysTwo[self.orderItr][16]-sellShrs;
                    pass;

                if(buyShrs!=0):
                    self.sysTwo[self.orderItr][26]=buyShrs;
                    self.sysTwo[self.orderItr][27]=buyVal;
                    self.sysTwo[self.orderItr][28]=buyVal/buyShrs;
                    self.sysTwo[self.orderItr][29]=buyVal-self.sysTwo[self.orderItr][25];
                    self.sysTwo[self.orderItr][30]=buyShrs-self.sysTwo[self.orderItr][24];
                    pass;
                
                
                self.sysTwo[self.orderItr][31]=md.L1.bid;
                self.sysTwo[self.orderItr][32]=md.L1.ask;
                self.sysTwo[self.orderItr][33]=md.L1.last;
                

                          
                # SHORT                          
                if(len(self.systemDOWN)>1 and s>=4):
                    long_bal=self.bot-self.filledBuy;
                    statusShort=self.filledSell+self.filledBuy;
                    statusUpdate=0;
                    statusUpdate=statusShort-self.orderBalance+self.filledBuy-self.satisfied;
                
                    # SHORT
                    self.sysTwo[self.orderItr][34]=long_bal;
                    self.sysTwo[self.orderItr][35]=statusShort;
                    self.sysTwo[self.orderItr][36]=statusUpdate;
                    self.sysTwo[self.orderItr][37]=self.bot+self.sold;
                    self.sysTwo[self.orderItr][38]=self.filledBuy+self.sold;
                    self.sysTwo[self.orderItr][39]=account[self.symbol].position.mtm_price;
                    self.sysTwo[self.orderItr][40]=self.satisfied;
                    self.sysTwo[self.orderItr][41]=account.realized_mtm_pl;
                    self.sysTwo[self.orderItr][42]=account.unrealized_entry_pl;
                    
                    print('down1.0', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                    
                    if(statusShort*1.1>self.orderBalance):
                        # ADJUST NET SHORT.
                        #
                        print('down1.1', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1011, allow_multiple_pending=True);
                        statusUpdate=0;
                        pxGeneric=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric, user_key=2023, allow_multiple_pending=True);
                        pass;
                        
                    if(short_position!=0 and long_bal*1.5>self.bot):
                        print('down1.2', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # ADJUST BUY v. SELL
                        # short
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=long_bal, user_key=999, allow_multiple_pending=True);
                        long_bal=0;
                        pass;
                        

                    if(lvlDOWN>=3 and lvlDOWN>self.systemDOWN[-2] and statusUpdate>0):
                        print('down1.3', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # RATE OF CHANGE.
                        # short
                        upDown = self.filledSell+self.sold-self.bot;
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1112, allow_multiple_pending=True);
                        statusUpdate=0;
                        pxGeneric=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric, user_key=2023, allow_multiple_pending=True);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric-(self.p1*10), user_key=2023, allow_multiple_pending=True);
                        pass;
                        
                    elif(lvlDOWN>=3 and lvlDOWN==self.systemDOWN[-2]):
                        print('down1.4', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        # PLATEAU - MARKET MAKE
                        # short
                        pxLowerAsk=min(md.L1.ask, md.L1.last)+self.p1;
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=-self.ebft, price=pxLowerAsk, user_key=1010, allow_multiple_pending=True);
                        pxLowerBid=min(md.L1.bid, md.L1.last)-(self.p1*1);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxLowerBid, user_key=2022, allow_multiple_pending=True);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxLowerBid-(self.p1*10), user_key=2023, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                        
                    if(lvlDOWN>=3 and lvlUP>0 and lvlUP>self.systemUP[-2] and account[self.symbol].position.shares!=0):
                        print('down1.5', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # HOP
                        # short
                        pxOne=min(md.L1.bid, md.L1.last)-self.p1;
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxOne, user_key=2020, allow_multiple_pending=True);
                        
                        pxLowerAsk=max(md.L1.ask, md.L1.last)+self.p1;
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=(self.neutral-self.ebft), price=pxLowerAsk, user_key=1010, allow_multiple_pending=True);
                        pass;
                    elif(lvlDOWN>=3 and lvlUP>0 and lvlUP<self.systemUP[-2] and statusUpdate>0):
                        print('down1.6', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # RATE OF CHANGE - NET SHORT.
                        # short
                        
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1110, allow_multiple_pending=True);
                        pxLower=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=(self.neutral-self.ebft)*2, price=pxLower, user_key=2023, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                    
                    if(short_position!=0 and long_bal>0 and self.neutral>0):
                        print('down1.7', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        # PLATEAU - MARKET MAKE - NEUTRAL.
                        # short
                        
                        pxTwoBid=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral, price=pxTwoBid, user_key=2022, allow_multiple_pending=True);
                        
                        pxTwoAsk=max(md.L1.ask, md.L1.last)+(self.p1*2);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=-self.ebft, price=pxTwoAsk, user_key=1000, allow_multiple_pending=True);
                        pass;
                        
                    if(lvlDOWN>=3 and lvlDOWN==self.systemDOWN[-2] and statusUpdate>0):
                        print('down1.8', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.filledBuy), (self.filledSell+self.filledBuy), ((self.filledSell+self.filledBuy)-self.orderBalance+self.filledBuy-self.satisfied), self.orderBalance, self.bot, self.sold, self.filledBuy, self.filledSell,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # PLATEAU - MARKET MAKE - NET SHORT.
                        # short
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1111);
                        pxOneBid=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=(self.neutral-self.ebft)*2, price=pxTwoBid, user_key=2022, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                    pass;
                    
                printAction('ebft(-)EXCH', currentLocation, currentRate, s, n, sAction, 'DOWN');
                
                str0=str(service.time_to_string(service.system_time))+",";
                for units in self.sysTwo[self.orderItr]:
                    str0+=str(units)+",";
                service.write_file(self.fileName,'{}'.format(str0));
                pass;
            
            
            if(self.ebft>0 and n>=3):
                self.systemLong=1;
                
                if(self.systemShort==1 and self.systemLong==1):
                    self.switchSystem(event, md, order, service, account);
                    return;
                    
                self.orderItr+=1;
                self.sysTwo.append(self.orderPM);
                self.ebft+=(self.ATR_scRp+self.mot_scRp+self.xxl_scRp)
                printAction('ebft(+)', currentLocation, currentRate, s, n, nAction, 'UP'); 
                self.bot+=self.ebft;
                self.sold-=self.neutral;
                
                #self.neutral+=s;
                self.orderSession+=1; 
                self.orderBalance+=(self.ebft-self.neutral); 
                self.allocationRate+=abs(self.ebft); 
                self.orderBuy.append([self.symbol, self.ebft]); 
                self.orderSell.append([self.symbol, self.neutral]);
                # self.orderBalance-=(-self.satisfied)
                lvlDOWN=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
                lvlUP=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                
                self.sysTwo[self.orderItr][0]=self.orderItr;
                self.sysTwo[self.orderItr][1]=self.systemItr;
                self.sysTwo[self.orderItr][2]=self.orderSession;
                self.sysTwo[self.orderItr][3]=self.symbol;
                self.sysTwo[self.orderItr][4]=self.ebft;
                self.sysTwo[self.orderItr][5]=self.neutral;
                self.sysTwo[self.orderItr][6]=self.orderBalance;
                self.sysTwo[self.orderItr][7]=self.bot;
                self.sysTwo[self.orderItr][8]=self.sold;
                self.sysTwo[self.orderItr][9]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysTwo[self.orderItr][10]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysTwo[self.orderItr][11]=account[self.symbol].position.shares;
                self.sysTwo[self.orderItr][12]=self.filledBuy;
                self.sysTwo[self.orderItr][13]=self.filledSell;



                # ONE SHOT DASH
                
                if(account[self.symbol].unrealized_pl.entry_pl>200):
                    self.closed=0;
                    return order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=666, allow_multiple_pending=True);

                if(lvlUP>=6 and lvlUP>self.systemUP[-2]):
                    self.closed=1;
                    return order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=100, user_key=2020, allow_multiple_pending=True);
                else:
                    return;
                
                if(self.closed==1):
                    return;
                    
                    

                if(self.orderSession==1):
                    self.orderBalance+=100;
                    return order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=100, user_key=2020, allow_multiple_pending=True);

                # CAPTURE SPREADS.
                if(account[self.symbol].unrealized_pl.entry_pl>5000):
                    return order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=666, allow_multiple_pending=True);
                    
                if(account[self.symbol].unrealized_pl.entry_pl>2500):
                    return order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=666, allow_multiple_pending=True);

                pendingOrderBook=account[self.symbol].pending.orders;
                pendingOrderUnit=len(pendingOrderBook);
                self.sysTwo[self.orderItr][14]=pendingOrderUnit;
                
                    
                pendingOrderBook=account[self.symbol].pending.orders;
                pendingOrderUnit=len(pendingOrderBook);
                self.sysTwo[self.orderItr][14]=pendingOrderUnit;
                shrtVal=buyVal=0;
                sellShrs=buyShrs=0;
                while(pendingOrderUnit>0):
                    pendingOrderUnit-=1;
                    caseOrder=pendingOrderBook[pendingOrderUnit];
                    if(caseOrder.shares<0):
                        self.sysTwo[self.orderItr][15]+=1;
                        self.sysTwo[self.orderItr][16]+=caseOrder.shares;
                        self.sysTwo[self.orderItr][17]+=(caseOrder.price*caseOrder.shares);
                        shrtVal+=(caseOrder.price*caseOrder.shares);
                        sellShrs+=caseOrder.shares;
                        pass;
                        
                    if(caseOrder.shares>0):
                        self.sysTwo[self.orderItr][23]+=1;
                        self.sysTwo[self.orderItr][24]+=caseOrder.shares;
                        self.sysTwo[self.orderItr][25]+=(caseOrder.price*caseOrder.shares);
                        buyVal+=(caseOrder.price*caseOrder.shares);
                        buyShrs+=caseOrder.shares;
                        pass;
                
                if(sellShrs!=0):
                    self.sysTwo[self.orderItr][18]=sellShrs;
                    self.sysTwo[self.orderItr][19]=shrtVal;
                    self.sysTwo[self.orderItr][20]=shrtVal/sellShrs;
                    self.sysTwo[self.orderItr][21]=self.sysTwo[self.orderItr][17]-shrtVal;
                    self.sysTwo[self.orderItr][22]=self.sysTwo[self.orderItr][16]-sellShrs;
                    pass;

                if(buyShrs!=0):
                    self.sysTwo[self.orderItr][26]=buyShrs;
                    self.sysTwo[self.orderItr][27]=buyVal;
                    self.sysTwo[self.orderItr][28]=buyVal/buyShrs;
                    self.sysTwo[self.orderItr][29]=buyVal-self.sysTwo[self.orderItr][25];
                    self.sysTwo[self.orderItr][30]=buyShrs-self.sysTwo[self.orderItr][24];
                    pass;
                
                
                self.sysTwo[self.orderItr][31]=md.L1.bid;
                self.sysTwo[self.orderItr][32]=md.L1.ask;
                self.sysTwo[self.orderItr][33]=md.L1.last;
                
                long_position = account[self.symbol].position.shares-100;
                if(len(self.systemUP)>1 and n>=6):
                    statusLong=self.orderBalance-(self.filledSell+self.filledBuy);
                    statusUpdate=0;
                    statusUpdate=-statusLong;

                    self.sysTwo[self.orderItr][34]='short_bal';
                    self.sysTwo[self.orderItr][35]=statusLong;
                    self.sysTwo[self.orderItr][36]=statusUpdate;
                    self.sysTwo[self.orderItr][37]=self.bot+self.sold;
                    self.sysTwo[self.orderItr][38]=self.filledBuy+self.sold;
                    self.sysTwo[self.orderItr][39]=account[self.symbol].position.mtm_price;
                    self.sysTwo[self.orderItr][40]=self.satisfied;
                    self.sysTwo[self.orderItr][41]=account.realized_mtm_pl;
                    self.sysTwo[self.orderItr][42]=account.unrealized_entry_pl;
                    
                    if(long_position<self.orderBalance and statusLong>0):
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=max(abs(self.satisfied), statusLong) , user_key=2121, allow_multiple_pending=True);
                        statusLong=0;
                        if(statusUpdate>self.orderBalance*1.25):
                            offerPx=max(md.L1.ask, md.L1.last)+(self.p5);
                            #order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=offerPx, user_key=999, allow_multiple_pending=True);
                            offerPxB=offerPx+(self.p5)+(self.p5);
                            order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=offerPxB, user_key=999, allow_multiple_pending=True);
                            pass;
                        pass;
                    elif(statusUpdate<self.orderBalance*1.5 and statusUpdate>0):
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=statusUpdate, user_key=999, allow_multiple_pending=True);
                        pass;
                    
                    if(lvlUP>=3 and lvlUP>self.systemUP[-2] and statusLong>0):
                        pxLowerBid=min(md.L1.bid, md.L1.last)-self.p1;
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=(self.ebft+self.neutral)*3, price=pxLowerBid, user_key=2121, allow_multiple_pending=True);
                        
                        if(account[self.symbol].position.shares>(self.ebft)*3):
                            pxGeneric=max(md.L1.ask, md.L1.last)+(self.p5)+(self.p5);
                            order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric, user_key=999, allow_multiple_pending=True);
                            pass;
                        pass;
                    elif(lvlUP>=3 and lvlUP==self.systemUP[-2]):
                        pxLowerBid=min(md.L1.bid, md.L1.last)-self.p5;
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.ebft+1, price=pxLowerBid, user_key=2121, allow_multiple_pending=True);
                        
                        if(account[self.symbol].position.shares>(self.ebft)*3):
                            pxHigherAsk=max(md.L1.ask, md.L1.last)+self.p5;
                            #order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxHigherAsk, user_key=999, allow_multiple_pending=True);
                            order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxHigherAsk+self.p1, user_key=999, allow_multiple_pending=True);
                            pass;
                        pass;

                    if(lvlDOWN>0 and lvlDOWN>self.systemDOWN[-2] and account[self.symbol].position.shares!=0):
                        pxOne=min(md.L1.bid, md.L1.last)-self.p5;
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.ebft, price=pxOne, user_key=2121, allow_multiple_pending=True);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.neutral+self.ebft, price=pxOne-self.p1, user_key=2121, allow_multiple_pending=True);
                        
                        if(account[self.symbol].position.shares>self.ebft*2):
                            pxLowerAsk=min(md.L1.ask, md.L1.last)+(self.p5)+(self.p5);
                            #order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxLowerAsk, user_key=999, allow_multiple_pending=True);
                            order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxLowerAsk+self.p5, user_key=999, allow_multiple_pending=True);
                            pass;
                        pass;
                    elif(lvlDOWN>0 and lvlDOWN<self.systemDOWN[-2] and statusLong>0):
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=statusLong, user_key=2121, allow_multiple_pending=True);
                        statusLong=0;
                        pxLower=max(md.L1.ask, md.L1.last)+(self.p1);
                        if(account[self.symbol].position.shares>(self.ebft)*2):
                            #order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=(self.neutral+self.ebft)*2, price=pxLower, user_key=999, allow_multiple_pending=True);
                            pxLowerB=pxLower+(self.p5);
                            order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=(self.neutral+self.ebft)*2, price=pxLowerB, user_key=999, allow_multiple_pending=True);
                            pass;
                        pass;
                        
                    if(long_position!=0 and statusUpdate>0 and self.neutral>0): 
                        pxTwoBid=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.ebft, price=pxTwoBid, user_key=2022, allow_multiple_pending=True);
                        pxTwoAsk=max(md.L1.ask, md.L1.last)+(self.p5);
                        if(account[self.symbol].position.shares>(self.neutral+self.ebft)*4):
                            #order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=(self.neutral+self.ebft)*2, price=pxTwoAsk, user_key=1111, allow_multiple_pending=True);
                            pxLowerB=pxTwoAsk+(self.p5);
                            order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=(self.neutral+self.ebft)*2, price=pxTwoAsk, user_key=999, allow_multiple_pending=True);
                            pass;
                        pass;
                        
                    if(lvlUP>=3 and lvlUP==self.systemUP[-2] and statusLong>0):
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=abs(statusLong)+1, user_key=2121, allow_multiple_pending=True);
                        statusLong=0;
                        pxOneAsk=max(md.L1.ask, md.L1.last)+(self.p5);
                        if(account[self.symbol].position.shares>self.neutral):
                            order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+3, price=pxOneAsk, user_key=999, allow_multiple_pending=True);
                            statusLong=0;
                            pass;
                        pass;

                printAction('ebft(+)EXCH', currentLocation, currentRate, s, n, nAction, 'UP');    
                
                str0=str(service.time_to_string(service.system_time))+",";
                for units in self.sysTwo[self.orderItr]:
                    str0+=str(units)+",";
                service.write_file(self.fileName,'{}'.format(str0));
                pass;
            
            if(self.orderSession>0):
                self.avgAllocationRate.append([int(self.allocationRate/self.orderSession)]);
                pass;
                
            if(self.orderSession>0 and self.ebft==0):
                checkPriceA=max(md.L1.bid, md.L1.ask, md.L1.last);
                checkPriceB=min(md.L1.bid, md.L1.ask, md.L1.last);
                checkMid=(checkPriceA+checkPriceB)/2;
                    
                self.orderItr+=1;
                self.sysTwo.append(self.orderPM);
                self.sysTwo[self.orderItr][0]=self.orderItr;
                self.sysTwo[self.orderItr][1]=self.systemItr;
                self.sysTwo[self.orderItr][2]=self.orderSession;
                self.sysTwo[self.orderItr][3]=self.symbol;
                self.sysTwo[self.orderItr][4]=self.ebft;
                self.sysTwo[self.orderItr][5]=self.neutral;
                self.sysTwo[self.orderItr][6]=self.orderBalance;
                self.sysTwo[self.orderItr][7]=self.bot;
                self.sysTwo[self.orderItr][8]=self.sold;
                self.sysTwo[self.orderItr][9]=self.ATR_scR+self.mot_scR+self.xxl_scR;
                self.sysTwo[self.orderItr][10]=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                self.sysTwo[self.orderItr][11]=account[self.symbol].position.shares;
                self.sysTwo[self.orderItr][12]=self.filledBuy;
                self.sysTwo[self.orderItr][13]=self.filledSell;
                pendingOrderBook=account[self.symbol].pending.orders;
                pendingOrderUnit=len(pendingOrderBook);
                self.sysTwo[self.orderItr][14]=pendingOrderUnit;
                
                pendingOrderBook=account[self.symbol].pending.orders;
                pendingOrderUnit=len(pendingOrderBook);
                self.sysTwo[self.orderItr][14]=pendingOrderUnit;
                shrtVal=buyVal=0;
                sellShrs=buyShrs=0;
                while(pendingOrderUnit>0):
                    pendingOrderUnit-=1;
                    caseOrder=pendingOrderBook[pendingOrderUnit];
                    if(caseOrder.shares<0):
                        self.sysTwo[self.orderItr][15]+=1;
                        self.sysTwo[self.orderItr][16]+=caseOrder.shares;
                        self.sysTwo[self.orderItr][17]+=(caseOrder.price*caseOrder.shares);
                        shrtVal+=(caseOrder.price*caseOrder.shares);
                        sellShrs+=caseOrder.shares;
                        pass;
                        
                    if(caseOrder.shares>0):
                        self.sysTwo[self.orderItr][23]+=1;
                        self.sysTwo[self.orderItr][24]+=caseOrder.shares;
                        self.sysTwo[self.orderItr][25]+=(caseOrder.price*caseOrder.shares);
                        buyVal+=(caseOrder.price*caseOrder.shares);
                        buyShrs+=caseOrder.shares;
                        pass;
                
                if(sellShrs!=0):
                    self.sysTwo[self.orderItr][18]=sellShrs;
                    self.sysTwo[self.orderItr][19]=shrtVal;
                    self.sysTwo[self.orderItr][20]=shrtVal/sellShrs;
                    self.sysTwo[self.orderItr][21]=self.sysTwo[self.orderItr][17]-shrtVal;
                    self.sysTwo[self.orderItr][22]=self.sysTwo[self.orderItr][16]-sellShrs;
                    pass;

                if(buyShrs!=0):
                    self.sysTwo[self.orderItr][26]=buyShrs;
                    self.sysTwo[self.orderItr][27]=buyVal;
                    self.sysTwo[self.orderItr][28]=buyVal/buyShrs;
                    self.sysTwo[self.orderItr][29]=buyVal-self.sysTwo[self.orderItr][25];
                    self.sysTwo[self.orderItr][30]=buyShrs-self.sysTwo[self.orderItr][24];
                    pass;
                
                
                self.sysTwo[self.orderItr][31]=md.L1.bid;
                self.sysTwo[self.orderItr][32]=md.L1.ask;
                self.sysTwo[self.orderItr][33]=md.L1.last;
                
                self.sysTwo[self.orderItr][34]=0;
                self.sysTwo[self.orderItr][35]=0;
                self.sysTwo[self.orderItr][36]=0;
                self.sysTwo[self.orderItr][37]=self.bot+self.sold;
                self.sysTwo[self.orderItr][38]=self.filledBuy+self.sold;
                self.sysTwo[self.orderItr][39]=account[self.symbol].position.mtm_price;
                self.sysTwo[self.orderItr][40]=self.satisfied;
                self.sysTwo[self.orderItr][41]=account.realized_mtm_pl;
                self.sysTwo[self.orderItr][42]=account.unrealized_entry_pl;
                
                
                str0=str(service.time_to_string(service.system_time))+",";
                for units in self.sysTwo[self.orderItr]:
                    str0+=str(units)+",";
                service.write_file(self.fileName,'{}'.format(str0));
                
                if(checkMid<md.L1.bid*0.97 or checkMid>md.L1.bid*1.03 or checkMid<md.L1.ask*0.97 or checkMid>md.L1.ask*1.03 or checkMid>md.L1.last*1.03 or checkMid<md.L1.last*0.97):
                    return;
                    
                if(self.systemShort==1 and self.systemLong==1):
                    self.systemLong=0;
                    self.systemShort=0;
                    return;
                    
                    if(self.orderBalance<0 or account[self.symbol].position.shares<0):
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=999, allow_multiple_pending=True);
                        self.systemStatus=1;
                        return;
                    
                    if(self.orderBalance>0 or account[self.symbol].position.shares>0):
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=999, allow_multiple_pending=True);
                        self.systemStatus=1;
                        return;
                pass;
                
                if(account.unrealized_entry_pl>500 or account.unrealized_entry_pl<500):
                    checkPriceA=max(md.L1.bid, md.L1.ask, md.L1.last);
                    checkPriceB=min(md.L1.bid, md.L1.ask, md.L1.last);
                    checkMid=(checkPriceA+checkPriceB)/2;
                    
                    if(checkMid<md.L1.bid*0.98 or checkMid>md.L1.bid*1.02 or checkMid<md.L1.ask*0.98 or checkMid>md.L1.ask*1.02 or checkMid>md.L1.last*1.02 or checkMid<md.L1.last*0.98):
                        return;
                    
                    if(account[self.symbol].position.shares>0):
                        if(account[self.symbol].position.mtm_price<checkMid):
                            self.systemCheckA=1;
                            order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=999, allow_multiple_pending=True);
                            return;
                            
                    if(account[self.symbol].position.shares<0):
                        if(account[self.symbol].position.mtm_price>checkMid):
                            self.systemCheckA=1;
                            order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=999, allow_multiple_pending=True);
                            return;
                    pass;

    def switchSystem(self, event, md, order, service, account):
        self.systemLong=0;
        self.systemShort=0;
                    
        if(self.orderBalance<0 or account[self.symbol].position.shares<0):
            order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=666, allow_multiple_pending=True);
            self.systemStatus=1;
            pass;
                    
        if(self.orderBalance>0 or account[self.symbol].position.shares>0):
            order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=666, allow_multiple_pending=True);
            self.systemStatus=1;
            pass;
        return;
                

    def on_fill(self, event, md, order, service, account):
        if(event.shares<0):
            self.filledSell+=event.shares;
            self.netShortPx+=event.price;
            self.netShortUnit+=1;
            print('xxxSOLD', event.shares, event.price, self.filledBuy, self.bot, self.satisfied, self.orderBalance, event.user_tag, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  self.spyCHG, self.qqqCHG, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            pass;
        if(event.shares>0):
            self.filledBuy+=event.shares;
            print('xxxxBOT', event.shares, event.price, self.filledBuy, self.bot, self.satisfied, self.orderBalance, event.user_tag, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  self.spyCHG, self.qqqCHG, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            pass;
        if(event.user_tag==999):
            print('xxxx999', event.shares, event.price, self.filledBuy, self.bot, self.satisfied, self.orderBalance, event.user_tag, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  self.spyCHG, self.qqqCHG, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            self.satisfied+=event.shares;
            pass;
        return;
