from cloudquant.interfaces import Strategy
import time, datetime, random

class Gr8Script7440a7b776ad48b280810fd86a9748af(Strategy):
    __script_name__ = 'bftCopy1'
    
    qqqCHG=spyCHG=0;
    #tickerItrA = ['BKNG','GS','MS','CMG','DDS','ELV','EQIX','HUBS','MELI','MSTR','SWAV','SPY','QQQ'];
    tickerItrB = ['ADBE','ASML','AVGO','AZO','BIO','BKNG','BLK','GS','MS','COST','CMG','DDS','DECK','ELV','EQIX','FCNCA','FDS','FICO','FNGU','GWW','HUBS','HUM','IDXX','IIVI','INTU','KLAC','LRCX','MDB','MDGL','MELI','MPWR','MSCI','MSTR','MTD','NFLX','NOW','NVDA','ORLY','REGN','SAIA','SEDG','SMCI','SNPS','SOXX','SWAV','TDG','TMO','TSLA','ULTA','UNH','URI','SPY','QQQ'];
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in Gr8Script7440a7b776ad48b280810fd86a9748af.tickerItrB;
        #return symbol in []Gr8Script7440a7b776ad48b280810fd86a9748af.tickerItrB;
        # return md.stat.prev_close>50.00 and md.stat.atr>5 or symbol=="SPY" or symbol=="QQQ";
        
    def on_start(self, md, order, service, account):
    
        #if("+" in self.symbol):
        #     return;
        
        self.systemRevolver=[0];
        self.systemType=0;
        self.systemUP=[0];
        self.systemDOWN=[0];
        self.levelThree=[];
        self.ATR_scR=0; self.mot_scR=0; self.xxl_scR=0; self.ATR_scRp=0; self.mot_scRp=0; self.xxl_scRp=0;

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
        self.neutral=self.neutralized=self.allocationRate=self.orderSession=self.orderBalance=self.maxBidRTE=self.maxAskRTE=self.minBidRTE=self.minAskRTE=0;
        self.motion = md.stat.atr;
        self.p1 = self.motion*0.01;
        self.active = self.motion*1.5;
        self.zero = md.stat.prev_close;
        self.triggerHigh = self.motion-self.zero;
        self.triggerLow = self.zero-self.motion;
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(minutes=1), timer_id="motionDetected");
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=10), timer_id="status");
        
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
        print(self.motion, self.p1, self.active, self.zero, self.triggerHigh, self.triggerLow, self.chkATR)
        
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
        
        def printBars(_stage, _location, _currentRate, _mxSpr, _mnSpr):                
            print(_stage, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.__class__.spyCHG, self.__class__.qqqCHG, _currentRate, self.ATR_TypeB, self.motionA,  self.motionY, self.ATR_TypeA, self.motionB, self.motionX,  '212', self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), mxSpr, mnSpr, 212, self.orderSession, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            return
        
        def printAction(_action, _location, _currentRate, _scr, _scrP, _motion, _TRAJECTORY):
            print(_action, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.__class__.spyCHG, self.__class__.qqqCHG, _currentRate, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, _TRAJECTORY, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), _scr, _scrP, _motion, self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
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

        print(self.priceBook)
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
            
        if(self.key==1):
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
            print('status', status)
            self.levelThree.append(status)

            if(self.ebft<0):
                self.ebft+=(self.ATR_scR+self.mot_scR+self.xxl_scR)
                printAction('ebft(-)', currentLocation, currentRate, s, n, sAction, 'DOWN');
                
                self.bot+=self.neutral;
                self.sold+=self.ebft;
                self.orderSession+=1;
                self.orderBalance+=(self.ebft+self.neutral);
                self.allocationRate+=abs(self.ebft);
                self.orderSell.append([self.symbol, abs(self.ebft)]);
                self.orderBuy.append([self.symbol, self.neutral]);
                
                short_position = account[self.symbol].position.shares;
                print('\norder status', self.bot, self.sold, self.long, self.short);
                pendingOrderBook=account[self.symbol].pending.orders;
                pendingOrderUnit=len(pendingOrderBook);
                while(pendingOrderUnit>0):
                    pendingOrderUnit-=1;
                    caseOrder=pendingOrderBook[pendingOrderUnit];
                    if(caseOrder.shares<0):
                        print('SELL', caseOrder);
                        pass;
                    if(caseOrder.shares>0):
                        print('BUY', caseOrder);
                        pass;
                
                # BUY {"timestamp":"2023-07-12 09:37:00.005000","order_id":"{e259e7a5-1f39-457a-bb3f-0d00da87b5be}","order_algorithm":"{4ad20d14-aacb-4850-9efe-cfa92d154304}","instruction_id":"{e259e7a5-1f39-457a-bb3f-0d00da87b5be}","script_id":"{6cc61f33-5989-4d09-b351-0b4e2a11eacd}","exit_script":"{00000000-0000-0000-0000-000000000000}","price":420.3866382,"shares":6,"filled_shares":0,"flags":0,"intent_str":"decrease","expected_direction_str":"reduce","state":"P","clordid":"000005QKSIM","user_tag":2022,"symbol":"ELV","script_class_name":"Gr8Script6cc61f3359894d09b3510b4e2a11eacd","explanation":""}

                
                
                
                lvlDOWN=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
                lvlUP=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                                
                if(len(self.systemDOWN)>1):
                    print('CTR DOWN:', lvlDOWN, self.systemDOWN[-2])
                    long_bal=self.bot-self.long;
                    statusShort=self.short+self.long;
                    statusUpdate=0;
                    
                    statusUpdate=statusShort-self.orderBalance;
                    
                    if(statusShort*1.1>self.orderBalance):    
                        print('statusUpdate', long_bal, statusUpdate, long_bal, self.orderBalance,  self.sold, self.short, self.long, self.bot);
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1011, allow_multiple_pending=True);
                        statusUpdate=0;

                    if(short_position!=0 and long_bal*1.25>self.bot):
                        print('riskAdjust', long_bal, statusUpdate, long_bal, self.orderBalance,  self.sold, self.short, self.long, self.bot);
                        order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=long_bal, user_key=2021, allow_multiple_pending=True);
                        long_bal=0;
                        
                    print('\n systemDOWN', long_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                    if(lvlDOWN>=3 and lvlDOWN>self.systemDOWN[-2] and statusUpdate>0):
                        upDown = self.short+self.sold-self.bot;
                        print('system LOWER 1011:\t', long_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1112, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                        
                    if(lvlUP>0 and lvlUP>self.systemUP[-2] and account[self.symbol].position.shares!=0):
                        pxOne=md.L1.ask-self.p1;
                        print('system JUMP 2020:\t', long_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=(self.neutral-self.ebft), price=pxOne, user_key=2020, allow_multiple_pending=True);
                        pass;
                    elif(lvlUP>0 and lvlUP<self.systemUP[-2] and statusUpdate>0):
                        print('system LOWER 1110:\t', long_bal, statusUpdate, self.sold, self.short, self.long, self.bot);
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1110, allow_multiple_pending=True);
                        statusUpdate=0;
                        pass;
                    
                    if(short_position!=0 and long_bal>0 and self.neutral>0):
                        pxTwoBid=min(md.L1.bid, md.L1.last)-self.p1-self.p1;
                        print('cover2:\t', long_bal, statusUpdate, self.sold, self.short, self.long, self.bot, pxTwoBid);
                        order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=self.neutral, price=pxTwoBid, user_key=2022, allow_multiple_pending=True);
                        pass;
                        
                    if(lvlDOWN>=3 and lvlDOWN==self.systemDOWN[-2] and statusUpdate>0):
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=statusUpdate, user_key=1111);
                        statusUpdate=0;
                        pass;
                        
                printAction('ebft(-)EXCH', currentLocation, currentRate, s, n, sAction, 'DOWN');
                pass;
                
                if(abs(account[self.symbol].position.shares)!=0):
                    printAction('offer', currentLocation, currentRate, s, n, 212, 'DOWN'); 
                    #print('offer',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate,  1, -1, self.neutral, self.ebft, self.ebft+self.neutral, self.orderBalance);
                    self.orderBalance;
                    #tcLong = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(self.ebft), user_key=113, allow_multiple_pending=40);
                    pass;

            if(self.ebft>0):
                self.ebft+=(self.ATR_scRp+self.mot_scRp+self.xxl_scRp)
                printAction('ebft(+)', currentLocation, currentRate, s, n, nAction, 'UP'); 
                self.bot+=self.ebft;
                self.sold-=self.neutral;
                
                #self.neutral+=s;
                self.orderSession+=1; self.orderBalance+=self.ebft-self.neutral; self.allocationRate+=abs(self.ebft); 
                self.orderBuy.append([self.symbol, self.ebft]); self.orderSell.append([self.symbol, self.neutral]);
                lvlUP=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                if(lvlUP>=3):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=lvlUP, user_key=2011);
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
                
                if(self.orderBalance>0):
                    #crsLong = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='exit', price=self.pxOFFER, user_key=112, allow_multiple_pending=40);
                    printAction('SELL', currentLocation, currentRate, s, n, 212, 'UP'); 
                    #print('sell',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, 1, -1,     self.orderSession, self.orderBalance, QTY, self.orderBalance);
                    # 1 HOP
                    #order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='exit', user_key=2);
                
                if(self.orderBalance<0):
                    #crsShort = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=abs(QTY), price=self.pxBID, user_key=111, allow_multiple_pending=40);
                    printAction('BUY', currentLocation, currentRate, s, n, 212, 'UP'); 
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
            return;
        if(event.shares>0):
            self.long+=event.shares;
            return;
        return;
