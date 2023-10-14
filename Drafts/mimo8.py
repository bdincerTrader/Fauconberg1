from cloudquant.interfaces import Strategy
import time, datetime, random

class Gr8Scriptac8077fd131647b7a7ee64fee0e9cbda(Strategy):
    __script_name__ = 'gpsFauconberg'
    
    qqqCHG=spyCHG=0;
    #tickerItrA = ['BKNG','GS','MS','CMG','DDS','ELV','EQIX','HUBS','MELI','MSTR','SWAV','SPY','QQQ'];
    tickerItrB = ['ADBE','ASML','AVGO','AZO','BIO','BKNG','BLK','GS','MS','COST','CMG','DDS','DECK','ELV','EQIX','FCNCA','FDS','FICO','FNGU','GWW','HUBS','HUM','IDXX','IIVI','INTU','KLAC','LRCX','MDB','MDGL','MELI','MPWR','MSCI','MSTR','MTD','NFLX','NOW','NVDA','ORLY','REGN','SAIA','SEDG','SMCI','SNPS','SOXX','SWAV','TDG','TMO','TSLA','ULTA','UNH','URI','SPY','QQQ'];
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in Gr8Scriptac8077fd131647b7a7ee64fee0e9cbda.tickerItrB;
        #return symbol in []Gr8Script7440a7b776ad48b280810fd86a9748af.tickerItrB;
        # return md.stat.prev_close>50.00 and md.stat.atr>5 or symbol=="SPY" or symbol=="QQQ";
        
    def on_start(self, md, order, service, account):
    
        self.systemRevolver=[0];
        self.systemType=0;
        self.systemUP=[0];
        self.systemDOWN=[0];
        self.levelThree=[];
        self.ATR_scR=0; self.mot_scR=0; self.xxl_scR=0; self.ATR_scRp=0; self.mot_scRp=0; self.xxl_scRp=0;
        self.satisfied=0;
        self.ATR_TypeA=0; self.ATR_TypeB=0; self.motionA=0.0; self.motionB=0.0; self.motionX=0.0; self.motionY=0.0;
        self.short=0;
        self.netShortUnit=0;
        self.long=0;
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
        self.p5 = self.motion*0.05;
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
        self.qty=1;
        result = datetime.datetime.strptime(self.TradeDate,'%Y-%m-%d %H:%M:%S.%f')
        print(result)
        result.strftime("%b %d %Y %H:%M:%S")
        #print(result)
        print(result.strftime("%Y-%d %H:%M:%S"), self.symbol)
        self.file_name = '{}--{}.csv'.format(self.symbol, result.strftime("%Y-%m-%d"))
        self.axcelFileDate=result.strftime("%Y-%m-%d")+self.symbol;
        self.ebft=0;
        self.crAskPts=self.crAskDt=self.crBidPts=self.crBidDt=0.00;
        self.mktTrades.append(self.zero);
        self.pxOFFER=self.zero+self.active+self.active;
        self.pxBID=self.zero-self.active-self.active;
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
            if(account[self.symbol].position.shares>0):
                order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                
        if(self.systemStatus==1):
            print('\n\n\n\n \t\t\t SYSTEM STATUS UPDATE \n\n', self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ATR_TypeB, self.motionA,  self.motionY, self.ATR_TypeA, self.motionB, self.motionX, self.orderSession, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance)
            self.satisfied=0;
            self.bot=0;
            self.sold=0;
                
            order.cancel(self.symbol);
            self.systemStatus=0;
        
        def printBars(_stage, _location, _currentRate, _mxSpr, _mnSpr):                
            print(_stage, 'b', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.__class__.spyCHG, self.__class__.qqqCHG, _currentRate, self.ATR_TypeB, self.motionA,  self.motionY, self.ATR_TypeA, self.motionB, self.motionX,  '212', self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), mxSpr, mnSpr, 212, self.orderSession, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            return
        
        def printAction(_action, _location, _currentRate, _scr, _scrP, _motion, _TRAJECTORY):
            print(_action, 'a', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.__class__.spyCHG, self.__class__.qqqCHG, _currentRate, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, _TRAJECTORY, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), _scr, _scrP, _motion, self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            return

        def marketSpread(b, a):
            self.key=1;
            #print('mk spr: ', self.symbol, b, a);
            if(((a+b)/2)>b and ((a+b)/2)<a):
                self.mktSpread.append(a-b);
            return self.mktSpread;
        
        self.neutral=0;
        currentBid = md.L1.bid;
        currentAsk = md.L1.ask;
        
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
        
        currentLocation =  currentBid - self.zero; 
        currentRate = currentLocation/self.zero;

        chkSPY = ((md['SPY'].L1.bid) - (md['SPY'].stat.prev_close));
        chkSPYRTE = chkSPY/(md['SPY'].stat.prev_close);
        self.__class__.spyCHG=chkSPYRTE;
        chkQQQ = ((md['QQQ'].L1.bid) - (md['QQQ'].stat.prev_close));
        chkQQQRTE = chkQQQ/(md['QQQ'].stat.prev_close);
        self.__class__.qqqCHG=chkQQQRTE;
        
        
        if(self.symbol=='SPY'):
            self.__class__.spyCHG=currentLocation/self.zero;
            return;
        elif(self.symbol=='QQQ'):
            self.__class__.qqqCHG=currentLocation/self.zero;
            return;
        else: 
            self.chk_SPY = currentRate - self.__class__.spyCHG;
            self.chk_QQQ = currentRate - self.__class__.qqqCHG;
            pass;
        
        
        if(currentAsk-currentBid>self.motion):
            print('qCheck');
            return;

        #print(self.priceBook)
        self.priceBook.append((currentAsk+currentBid+self.mktTrades[-1])/3);

        self.ebft=0;
        if(currentLocation > self.motion):
            FT=0;
            FBT=0;
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
            printBars('ATR1', currentLocation, currentRate, mxSpr, mnSpr);
            # lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
            #pathA = '{}.{}'.format("ATRA", self.file_name);
            #service.write_file(pathA, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            if(currentBid+self.p1 > md.L1.daily_high):
                self.ATR_TypeA=1.1;
                self.ATR_scRp+=1;
                self.ebft-=1;
                self.neutral+=1;
                # lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price= self.pxBID, user_key=111, allow_multiple_pending=40);
                printBars('ATR1-B', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            pass;
            
        if(currentLocation > self.active):
            FT=0;FBT=0; self.ebft+=1; 
            
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
            printBars('ATR2', currentLocation, currentRate, mxSpr, mnSpr);
            #pathB = '{}.{}'.format("ATRB", self.file_name);
            #service.write_file(pathB, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            # lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price= self.pxBID, user_key=111, allow_multiple_pending=40);
            if(currentBid+self.p1 > md.L1.daily_high):
                self.ATR_TypeB=2.1;
                self.ATR_scRp+=1;
                self.ebft-=1;
                self.neutral+=1;
                #lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price= self.pxBID, user_key=111, allow_multiple_pending=40);
                printBars('ATR2B', currentLocation, currentRate, mxSpr, mnSpr);
                #print('ATR2B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
            pass;

        if(currentLocation < -self.motion):
            FT=0;FBT=0; 
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
            printBars('ATR3', currentLocation, currentRate, mxSpr, mnSpr);
            #pathC = '{}.{}'.format("ATRC", self.file_name);
            #service.write_file(pathC, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
                    
            if(currentAsk-self.p1 < md.L1.daily_low):
                self.ATR_TypeB=3.1;
                self.ATR_scR-=1;
                self.ebft+=1;
                self.neutral+=1;
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                printBars('ATR3-B', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            pass;
            
        if(currentLocation < -self.active):
            FT=0;FBT=0;
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
            printBars('ATR4', currentLocation, currentRate, mxSpr, mnSpr);
            
            #pathD = '{}.{}'.format("ATRD", self.file_name);
            #service.write_file(pathD, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            # offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)

            if(currentAsk-self.p1 < md.L1.daily_low):
                self.ATR_TypeB=4.1;
                self.ATR_scR-=1;
                self.ebft+=1;
                self.neutral+=1;
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                printBars('ATR4-B', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            pass;
            
        if(self.chk_SPY > 0.02):
            FT=0;
            FBT=0;
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
                       
            if(currentRate<self.__class__.spyCHG):
            
                self.ebft-=1;
                self.motionA=5.1;
                self.mot_scR-=1;
                printBars('motion5.1', currentLocation, currentRate, mxSpr, mnSpr);
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                pass;
                
            if(currentRate>self.__class__.spyCHG):
                self.ebft+=1;
                self.motionA=5.2;
                self.mot_scRp+=1;
                printBars('motion5.2', currentLocation, currentRate, mxSpr, mnSpr);
                #lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('pMax5', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('pMin5', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('nMax5', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('nMin5', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
                
            if(FT==0):
                self.neutral+=1;
                printBars('m5_FT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                pass;

            if(self.chk_SPY > 0.04):
                mxSpr=mnSpr=0;
                if(len(self.mktSpread)>2):
                    mxSpr=max(self.mktSpread); 
                    mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                    pass;
                else:
                    mxSpr=self.mktSpread[-1];
                    mnSpr=self.mktSpread[-1];
                    pass;
    
                chkPrints=0;
                if(len(self.mktTrades)>2):
                    chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                    pass;

                self.xxl_scR-=1;
                self.xxl_scRp+=1;
                self.neutral+=1;
                printBars('motion5-B', currentLocation, currentRate, mxSpr, mnSpr);
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('pMax5b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('pMin5b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('nMax5b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('nMax5b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                if(FBT==0):
                    self.neutral+=1;
                    printBars('m5_FBT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass; 
            pass;
            
        if(self.chk_SPY < -0.02):
            
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk); 
            FT=0;FBT=0; 
            
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

            if(currentRate<self.__class__.spyCHG):
                self.ebft-=1;
                self.motionA=6.1;
                self.mot_scR-=1;
                printBars('motion6.1', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(currentRate>self.__class__.spyCHG):
                self.ebft+=1;
                self.motionA=6.2;
                self.mot_scRp+=1;
                printBars('motion6.2', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('pMax6', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('pMin6', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('nMax6', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('nMin6', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(FT==0):
                self.neutral+=1;
                printBars('m6_FT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                pass;

            if(self.chk_SPY < -0.04):
            
                mxSpr=mnSpr=0;
                if(len(self.mktSpread)>2):
                    mxSpr=max(self.mktSpread); 
                    mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                    pass;
                else:
                    mxSpr=self.mktSpread[-1];
                    mnSpr=self.mktSpread[-1];
                    pass;
                
                self.motionX=6.3;
                self.xxl_scR-=1;
                self.xxl_scRp+=1;
                self.neutral+=1;
                
                printBars('motion6-B', currentLocation, currentRate, mxSpr, mnSpr);
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    self.ebft-=1;
                    printBars('pMax6b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('pMin6b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('nMax6b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('nMax6b', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;

                if(FBT==0):
                    self.neutral+=1;
                    printBars('m6_FBT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                    pass;
                pass;
            pass;
            
        if(self.chk_QQQ > 0.02):
            mxSpr=mnSpr=0;
            
            if(len(self.mktSpread)>2):
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;

            FT=0;
            FBT=0;
            
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk); 

            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
           
            if(currentRate<self.__class__.qqqCHG):
                self.ebft-=1;
                self.motionB=7.1;
                self.mot_scR-=1;
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                printBars('motion7.1', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
                
            if(currentRate>self.__class__.qqqCHG):
                self.ebft+=1;
                self.motionB=7.2;
                self.mot_scRp+=1;
                #lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
                printBars('motion7.2', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
   
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('pMax7', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('pMin7', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('nMax7', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('nMax7', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            if(FT==0):
                self.neutral+=1;
                printBars('m7_FT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                pass;
            
            if(self.chk_QQQ > 0.04):
            
                mxSpr=mnSpr=0;
                
                if(len(self.mktSpread)>2):
                    # print(self.mktSpread);
                    mxSpr=max(self.mktSpread); 
                    mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                    pass;
                else:
                    mxSpr=self.mktSpread[-1];
                    mnSpr=self.mktSpread[-1];
                    pass;
                    
                self.xxl_scR-=1;
                self.xxl_scRp+=1;
                self.neutral+=1;
                
                printBars('motion7-B', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion7-B',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('pMax7b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMax7b',     service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     self.neutral, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('pMin7b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMin7b',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  self.neutral, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('nMax7b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMax7b',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  self.neutral, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('nMin7b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMin7b',     service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  self.neutral, self.ebft, self.orderBalance);
                    pass;
                if(FBT==0):
                    self.neutral+=1;
                    printBars('m7_FBT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('m7_FBT_neutral',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT, self.neutral, self.ebft, self.orderBalance);
                    pass;
                pass;
            pass;
            
        if(self.chk_QQQ < -0.02):
            FT=0;FBT=0;
            
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk); 
            chkPrints=0;

            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            
            if(len(self.mktSpread)>2):
                # print(self.mktSpread);
                mxSpr=max(self.mktSpread); 
                mnSpr=min(xs for xs in self.mktSpread if xs != 0)
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;
                
            if(currentRate<self.__class__.qqqCHG):
                self.ebft-=1;
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                self.motionB=8.1;
                self.mot_scR-=1;
                printBars('motion8.1', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion8.1',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
            if(currentRate>self.__class__.qqqCHG):
                self.ebft+=1;
                self.motionB=8.2;
                self.mot_scRp+=1;
                printBars('motion8.2', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion8.2',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('pMax8', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMax8',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('pMin8', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMin8',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('nMax8', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMax8',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('nMin8', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMin8',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
            if(FT==0):
                self.neutral+=1;
                printBars('m8_FT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                #print('m8_FT_neutral',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
                
            if(self.chk_QQQ < -0.04):
                self.motionY=8.3;
                self.xxl_scR-=1;
                self.xxl_scRp+=1;
                self.neutral+=1;
                printBars('motion8-B', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion8-B',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
        
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('pMax8b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMax8b',     service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('pMin8b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMin8b',     service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('nMax8b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMax8b',     service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('nMin8b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMin8b',     service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;
                if(FBT==0):
                    self.neutral+=1;
                    printBars('m8_FBT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('m8_FBT_neutral',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                    pass;
                pass;
            pass;
            
        if(self.key==1 and event.timestamp<self.illiquid_time): 
            self.neutralized+=self.neutral;
            s=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
            n=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
            
            #print('ebft',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, s, n,  self.neutralized,   self.neutral, self.ebft, self.orderBalance);
            printAction('key', currentLocation, currentRate, s, n, 212, 'ACTION');
                                
            sAction=0;
            if(abs(self.ATR_scR+self.mot_scR+self.xxl_scR)<self.systemDOWN[-1]):
                sAction=3;
            elif(abs(self.ATR_scR+self.mot_scR+self.xxl_scR)>self.systemDOWN[-1]):
                sAction=2;
            elif(abs(self.ATR_scR+self.mot_scR+self.xxl_scR)==self.systemDOWN[-1]):
                sAction=1;

            nAction=0;
            if(self.ATR_scRp+self.mot_scRp+self.xxl_scRp<self.systemUP[-1]):
                nAction=3;
            elif(self.ATR_scRp+self.mot_scRp+self.xxl_scRp>self.systemUP[-1]):
                nAction=2;
            elif(self.ATR_scRp+self.mot_scRp+self.xxl_scRp==self.systemUP[-1]):
                nAction=1;
            self.systemUP.append(n);            
            self.systemDOWN.append(s);
            
            checkRate=0;
            i=0;
            for idx in self.priceBook:
                checkRate+=(idx-self.zero);
                i+=1;
            status=checkRate/i;
            self.levelThree.append(status);

            if(self.ebft<0):
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
                
                spot1=spot2=spot3=spot4=0;
                spot5=spot6=spot7=spot8=0;
            
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
                    print('down0.0', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                
                if(account[self.symbol].unrealized_pl.entry_pl>2500):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                    return
                    
                if(account[self.symbol].unrealized_pl.entry_pl>5000):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                    return
                
                
                print('down0.1', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                
                pendingOrderBook=account[self.symbol].pending.orders;
                pendingOrderUnit=len(pendingOrderBook);
                if(pendingOrderUnit!=0):
                    print('\n\n ORDER BOOK')
                while(pendingOrderUnit>0):
                    pendingOrderUnit-=1;
                    caseOrder=pendingOrderBook[pendingOrderUnit];
                    if(caseOrder.shares<0):
                        print('offers', 'short', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);#print('SELLORDER', caseOrder);
                        pass;
                    if(caseOrder.shares>0):
                        print('bids', 'long', self.orderSession, caseOrder.timestamp, caseOrder.price, caseOrder.shares, caseOrder.user_tag, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short, spot1,spot2,spot3,spot4);
                        
                        #print('BUYORDER', caseOrder);
                        pass;
                
                lvlDOWN=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
                lvlUP=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                                
                if(len(self.systemDOWN)>1):
                
                    long_bal=self.bot-self.long;
                    statusShort=self.short+self.long;
                    statusUpdate=0;
                    statusUpdate=statusShort-self.orderBalance+self.long-self.satisfied;
                    
                    print('down1.0', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                    
                    if(statusShort*1.1>self.orderBalance):
                    
                        # ADJUST NET SHORT.
                        #
                        print('down1.1', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1011, allow_multiple_pending=True);
                        statusUpdate=0;
                        pxGeneric=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric, user_key=2023, allow_multiple_pending=True);
                        pass;
                        
                    if(short_position!=0 and long_bal*1.5>self.bot):
                        print('down1.2', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # ADJUST BUY v. SELL
                        #
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=long_bal, user_key=999, allow_multiple_pending=True);
                        long_bal=0;
                        pass;
                        

                    if(lvlDOWN>=3 and lvlDOWN>self.systemDOWN[-2] and statusUpdate>0):
                        print('down1.3', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # RATE OF CHANGE.
                        #
                        upDown = self.short+self.sold-self.bot;
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1112, allow_multiple_pending=True);
                        statusUpdate=0;
                        pxGeneric=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric, user_key=2023, allow_multiple_pending=True);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric-(self.p1*10), user_key=2023, allow_multiple_pending=True);
                        pass;
                        
                    elif(lvlDOWN>=3 and lvlDOWN==self.systemDOWN[-2]):
                        print('down1.4', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        # PLATEAU - MARKET MAKE
                        # 
                        pxLowerAsk=min(md.L1.ask, md.L1.last)+self.p1;
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=-self.ebft, price=pxLowerAsk, user_key=1010, allow_multiple_pending=True);
                        pxLowerBid=min(md.L1.bid, md.L1.last)-(self.p1*1);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxLowerBid, user_key=2022, allow_multiple_pending=True);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxLowerBid-(self.p1*10), user_key=2023, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                        
                    if(lvlDOWN>=3 and lvlUP>0 and lvlUP>self.systemUP[-2] and account[self.symbol].position.shares!=0):
                        print('down1.5', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # HOP
                        #
                        pxOne=min(md.L1.bid, md.L1.last)-self.p1;
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral+1, price=pxOne, user_key=2020, allow_multiple_pending=True);
                        
                        pxLowerAsk=max(md.L1.ask, md.L1.last)+self.p1;
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=(self.neutral-self.ebft), price=pxLowerAsk, user_key=1010, allow_multiple_pending=True);
                        pass;
                    elif(lvlDOWN>=3 and lvlUP>0 and lvlUP<self.systemUP[-2] and statusUpdate>0):
                        print('down1.6', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # RATE OF CHANGE - NET SHORT.
                        #
                        
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1110, allow_multiple_pending=True);
                        pxLower=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=(self.neutral-self.ebft)*2, price=pxLower, user_key=2023, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                    
                    if(short_position!=0 and long_bal>0 and self.neutral>0):
                        print('down1.7', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        # PLATEAU - MARKET MAKE - NEUTRAL.
                        # 
                        pxTwoBid=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral, price=pxTwoBid, user_key=2022, allow_multiple_pending=True);
                        
                        pxTwoAsk=max(md.L1.ask, md.L1.last)+(self.p1*2);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=-self.ebft, price=pxTwoAsk, user_key=1000, allow_multiple_pending=True);
                        pass;
                        
                    if(lvlDOWN>=3 and lvlDOWN==self.systemDOWN[-2] and statusUpdate>0):
                        print('down1.8', self.orderBalance, self.orderSession, short_position, self.symbol, currentLocation, self.satisfied, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.ebft, self.neutral, self.allocationRate, (self.ATR_scR+self.mot_scR+self.xxl_scR),self.systemDOWN[-2],(self.ATR_scRp+self.mot_scRp+self.xxl_scRp),self.systemUP[-2], (self.bot-self.long), (self.short+self.long), ((self.short+self.long)-self.orderBalance+self.long-self.satisfied), self.orderBalance, self.bot, self.sold, self.long, self.short,spot1,spot2,spot3,spot4,spot5,spot6,spot7,spot8);
                        
                        # PLATEAU - MARKET MAKE - NET SHORT.
                        #
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1111);
                        pxOneBid=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=(self.neutral-self.ebft)*2, price=pxTwoBid, user_key=2022, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                        
                printAction('ebft(-)EXCH', currentLocation, currentRate, s, n, sAction, 'DOWN');
                
                if(abs(account[self.symbol].position.shares)!=0):
                    printAction('offer', currentLocation, currentRate, s, n, 212, 'DOWN'); 
                    #print('offer',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate,  1, -1, self.neutral, self.ebft, self.ebft+self.neutral, self.orderBalance);
                    #tcLong = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(self.ebft), user_key=113, allow_multiple_pending=40);
                    pass;
                pass;
                
            if(self.ebft>0):
                self.ebft+=(self.ATR_scRp+self.mot_scRp+self.xxl_scRp)
                printAction('ebft(+)', currentLocation, currentRate, s, n, nAction, 'UP'); 
                self.bot+=self.ebft;
                self.sold-=self.neutral;
                
                #self.neutral+=s;
                self.orderSession+=1; self.orderBalance+=self.ebft-self.neutral; self.allocationRate+=abs(self.ebft); 
                self.orderBuy.append([self.symbol, self.ebft]); 
                self.orderSell.append([self.symbol, self.neutral]);
                
                lvlDOWN=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
                lvlUP=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                
                # CAPTURE SPREADS.
                if(account[self.symbol].unrealized_pl.entry_pl>5000):
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                    # order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=999, allow_multiple_pending=True);
                    return
                
                long_position = account[self.symbol].position.shares;
                #print('\norder status LONG', self.symbol, self.bot, self.sold, self.long, self.short, long_position, self.p5, self.p1);
                if(len(self.systemUP)>1):
                    #print('CTR UP:', lvlUP, self.systemUP[-2])
                    short_bal=-self.sold+self.short;
                    statusLong=-self.short+self.long;
                    statusUpdate=0;
                    statusUpdate=self.orderBalance-self.long-self.short-self.satisfied;
                    #print('SERIES A --- statusUpdate LONG', short_bal, statusLong, statusUpdate, self.orderBalance, self.bot, self.sold, self.long, self.short, long_position, self.satisfied);
                    
                    if(statusLong*1.1>self.orderBalance and statusUpdate>0):
                        #print('SERIES B --- update LONG', short_bal, statusLong, statusUpdate, self.orderBalance, self.bot, self.sold, self.long, self.short, long_position, self.satisfied);
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=statusUpdate, user_key=2121, allow_multiple_pending=True);
                        statusUpdate=0;
                        offerPx=max(md.L1.ask, md.L1.last)+(self.p1*2);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.neutral+1, price=offerPx, user_key=999, allow_multiple_pending=True);
                        offerPxB=offerPx+self.p5;
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.neutral+self.ebft, price=offerPxB, user_key=999, allow_multiple_pending=True);
                        pass;
                        
                    if(long_position!=0 and short_bal>-self.sold*0.25):
                        #print('SERIES C --- update SHORT', short_bal, statusLong, statusUpdate, self.orderBalance, self.bot, self.sold, self.long, self.short, long_position);
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=abs(short_bal), user_key=1011, allow_multiple_pending=True);
                        short_bal=0;
                        pass;
                    
                    #print('\n systemUP', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot, statusLong, long_position);

                    if(lvlUP>=3 and lvlUP>self.systemUP[-2] and statusUpdate>0):
                        downUP = self.long+self.bot+self.sold;
                        #print('system HIGHER 1112:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=statusUpdate, user_key=2121, allow_multiple_pending=True);
                        statusUpdate=0;
                        
                        pxGeneric=max(md.L1.ask, md.L1.last)+(self.p1*2);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric, user_key=999, allow_multiple_pending=True);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxGeneric+(self.p1*10), user_key=999, allow_multiple_pending=True);
                        pass;
                    elif(lvlUP>=3 and lvlUP==self.systemUP[-2]):
                        #print('system HIGHER 101:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        pxLowerBid=min(md.L1.bid, md.L1.last)+self.p1;
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.ebft, price=pxLowerBid, user_key=2121, allow_multiple_pending=True);
                        
                        pxHigherAsk=max(md.L1.ask, md.L1.last)+self.p5;
                        #print('cover 101:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot, pxLowerBid);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.neutral+1, price=pxHigherAsk, user_key=2010, allow_multiple_pending=True);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.neutral+1, price=pxHigherAsk+self.p1, user_key=2010, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;

                    if(lvlDOWN>0 and lvlDOWN>self.systemDOWN[-2] and account[self.symbol].position.shares!=0):
                        pxLowerAsk=min(md.L1.ask, md.L1.last)+self.p1;
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+self.ebft, price=pxLowerAsk, user_key=1010, allow_multiple_pending=True);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral+1, price=pxLowerAsk+self.p5, user_key=1010, allow_multiple_pending=True);
                        
                        pxOne=min(md.L1.bid, md.L1.last)-self.p5;
                        #print('system JUMP 2020:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.ebft, price=pxOne, user_key=2121, allow_multiple_pending=True);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.neutral+self.ebft, price=pxOne-self.p1, user_key=2121, allow_multiple_pending=True);
                        pass;
                        
                    elif(lvlDOWN>0 and lvlDOWN<self.systemDOWN[-2] and statusUpdate>0):
                        #print('system drop 2020:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=statusUpdate, user_key=2121, allow_multiple_pending=True);
                        statusUpdate=0;
                        
                        pxLower=max(md.L1.ask, md.L1.last)+(self.p1);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=(self.neutral+self.ebft)*2, price=pxLower, user_key=1111, allow_multiple_pending=True);
                        pxLowerB=pxLower+(self.p5);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=(self.neutral+self.ebft)*2, price=pxLowerB, user_key=999, allow_multiple_pending=True);
                        pass;
                        
                    if(long_position!=0 and short_bal>0 and self.neutral>0): 
                        pxTwoBid=min(md.L1.bid, md.L1.last)-(self.p1*2);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.ebft, price=pxTwoBid, user_key=2022, allow_multiple_pending=True);
                        #print('offload 2:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot, pxTwoBid);
                        pxTwoAsk=max(md.L1.ask, md.L1.last)+(self.p5);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral, price=pxTwoAsk, user_key=999, allow_multiple_pending=True);
                        pxTwoAskB=pxTwoAsk+self.p5;
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral, price=pxTwoAskB, user_key=999, allow_multiple_pending=True);
                        pass;
                        
                    if(lvlUP>=3 and lvlUP==self.systemUP[-2] and statusUpdate>0):
                        #print('system 1111:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=statusUpdate, user_key=2121, allow_multiple_pending=True);
                        statusUpdate=0;
                        pxOneAsk=max(md.L1.ask, md.L1.last)+(self.p5);
                        #print('offload:\t', short_bal, statusUpdate, self.sold, self.short, self.long, self.bot, pxOneBid);
                        order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=self.neutral, price=pxOneAsk, user_key=999, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                        
                printAction('ebft(+)EXCH', currentLocation, currentRate, s, n, nAction, 'UP');    
                
                if(abs(account[self.symbol].position.shares)!=0):
                    printAction('bid', currentLocation, currentRate, s, n, 212, 'UP'); 
                    #print('bid',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, 1, -1, self.ebft, self.neutral, self.ebft-self.neutral, self.orderBalance);
                    #self.orderBalance;
                    #tcShort = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(self.ebft), user_key=103);
                    pass;
                pass;
                
            if(self.orderSession>0):
                self.avgAllocationRate.append([int(self.allocationRate/self.orderSession)]);
                pass;
                
            if(self.orderSession>0 and self.ebft==0):
                QTY=0;
                if(account[self.symbol].position.shares!=0): QTY=account[self.symbol].position.shares; pass;
                else: QTY=self.orderBalance; pass;
                conversion = abs(account[self.symbol].position.shares);
                
                if(self.orderBalance>0 and account[self.symbol].position.shares>0):
                    #crsLong = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='exit', price=self.pxOFFER, user_key=112, allow_multiple_pending=40);
                    printAction('SELLXXXX', currentLocation, currentRate, s, n, 212, 'DOWN'); 
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=999, allow_multiple_pending=True);
                    self.systemStatus=1;
                    #print('sell',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, 1, -1,     self.orderSession, self.orderBalance, QTY, self.orderBalance);
                    # 1 HOP
                    #order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='exit', user_key=2);
                
                if(self.orderBalance<0 and abs(account[self.symbol].position.shares)>0):
                    #crsShort = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=abs(QTY), price=self.pxBID, user_key=111, allow_multiple_pending=40);
                    printAction('BUYXXXXX', currentLocation, currentRate, s, n, 212, 'UP');
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares)+1, user_key=999, allow_multiple_pending=True);
                    self.systemStatus=1;
                    
                    #print('buy',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, 1, -1, self.orderSession, self.orderBalance, QTY, self.orderBalance);
                    # 1 HOP
                    #order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='exit', user_key=1);
                self.orderBalance=0;
                pass;
            pass;
        pass;
        
    def on_fill(self, event, md, order, service, account):
        if(event.shares<0):
            self.short+=event.shares;
            self.netShortPx+=event.price;
            self.netShortUnit+=1;
            print('xxxSOLD', event.shares, event.price, self.long, self.bot, self.satisfied, self.orderBalance, event.user_tag, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  self.__class__.spyCHG, self.__class__.qqqCHG, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            pass;
        if(event.shares>0):
            self.long+=event.shares;
            print('xxxxBOT', event.shares, event.price, self.long, self.bot, self.satisfied, self.orderBalance, event.user_tag, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  self.__class__.spyCHG, self.__class__.qqqCHG, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            pass;
        if(event.user_tag==999):
            print('xxxx999', event.shares, event.price, self.long, self.bot, self.satisfied, self.orderBalance, event.user_tag, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  self.__class__.spyCHG, self.__class__.qqqCHG, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            self.satisfied+=event.shares;
            pass;
        return;
