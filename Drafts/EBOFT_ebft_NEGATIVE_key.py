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


        self.ATR_scR=0; self.mot_scR=0; self.xxl_scR=0; self.ATR_scRp=0; self.mot_scRp=0; self.xxl_scRp=0;
        
        
        self.ATR_TypeA=0; self.ATR_TypeB=0; self.motionA=0.0; self.motionB=0.0; self.motionX=0.0; self.motionY=0.0;
        
        self.key=0;
        self.mktSpread=[0.00];
        self.mktTrades=[md.L1.last];
        self.priceBook=[md.L1.last];
        
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
    
        def printBars(_stage, _location, _currentRate, _mxSpr, _mnSpr):                
            print(_stage, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.__class__.spyCHG, self.__class__.qqqCHG, _currentRate, self.ATR_TypeA, self.ATR_TypeB, self.motionA, self.motionB, self.motionX, self.motionY, '212', self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), mxSpr, mnSpr, self.orderSession, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
            return
        
        def printAction(_action, _location, _currentRate, _scr, _scrP, _TRAJECTORY):
            print(_action, service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  _location, self.__class__.spyCHG, self.__class__.qqqCHG, _currentRate, self.ATR_scR, self.mot_scR, self.xxl_scR, self.ATR_scRp, self.mot_scRp, self.xxl_scRp, _TRAJECTORY, self.priceBook[-1], (self.priceBook[-1]-self.priceBook[-2]), (self.priceBook[-1]-self.priceBook[0]), _scr, _scrP,  self.neutralized, self.bot, self.sold, self.neutral, self.ebft, self.orderBalance);
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
            return;
        if(currentAsk*1<self.motion):
            return;
        
        self.systemType=0;
        self.ATR_scR=0; self.mot_scR=0; self.xxl_scR=0; self.ATR_scRp=0; self.mot_scRp=0; self.xxl_scRp=0; self.ATR_scR=0; self.mot_scR=0;
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
        

        if(currentAsk-currentBid>self.motion):
            print('qCheck');
            return;


        self.priceBook.append((currentAsk+currentBid+self.mktTrades[-1])/3);

        if(len(self.ask)>2):
            self.crAskPts = self.ask[-1]-self.ask[-2]; 
            self.crAskDt = self.crAskPts/self.ask[-1];
            self.askRate.append(sum(self.ask)/len(self.ask));
            self.maxAskRTE=max(self.askRate);
            self.minAskRTE=min(self.askRate);
            askRTE = self.askRate[-1]; offsetAsk = askRTE/4; 
            aA = askRTE-offsetAsk-offsetAsk;
            aB = askRTE-offsetAsk;
            aC = askRTE+offsetAsk;
            aD = askRTE+offsetAsk+offsetAsk;
            
            offer=5;
            if(self.crAskDt==self.maxAskRTE): offer=10; pass;
            elif(self.crAskDt==self.minAskRTE): offer=4; pass;
            elif(askRTE>aD): offer=9; pass;
            elif(askRTE>aC): offer=8; pass;
            elif(askRTE<aA): offer=6; pass;
            elif(askRTE<aB): offer=7; pass;
            else: offer=5; pass;
            
            self.pxOFFER=self.ask[-1]+((self.chkATR+self.chkATR+self.chkATR+self.chkATR)*offer); 
            # print('ASK', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ, currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, offsetAsk, askRTE, self.crAskPts, self.minAskRTE,    self.maxAskRTE, offer, self.pxOFFER);
            pass;
        if(len(self.bid)>2):
            self.crBidPts=self.bid[-1]-self.bid[-2]; 
            self.crBidDt=self.crBidPts/self.bid[-1]; 
            self.bidRate.append(sum(self.bid)/len(self.bid)); self.maxBidRTE=max(self.bidRate); self.minBidRTE=min(self.bidRate);
            bidRTE = self.bidRate[-1]; offsetBid = bidRTE/4;
            bA = bidRTE-offsetBid-offsetBid;
            bB = bidRTE-offsetBid;
            bC = bidRTE+offsetBid;
            bD = bidRTE+offsetBid+offsetBid;

            purchase=5;
            if(self.crBidDt==self.maxBidRTE): purchase=10; pass;
            elif(self.crBidDt==self.minBidRTE): purchase=4; pass;
            elif(bidRTE>bD): purchase=9; pass;
            elif(bidRTE>bC): purchase=8; pass;
            elif(bidRTE<bA): purchase=6; pass;
            elif(bidRTE<bB): purchase=7; pass;
            else: purchase=5; pass;
            
            self.pxBID = self.bid[-1]+(self.chkATR*offer);
            #print('BID', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ, currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, offsetBid, bidRTE, self.crBidPts, self.minBidRTE,  self.maxBidRTE, purchase, self.pxBID);
            pass;

        self.ebft=0;
        # MOTION 1 + #
        if(currentLocation > self.motion):
            FT=0;
            FBT=0;
            self.ebft+=1;
            
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            #print(self.mktTrades[-1]);
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                # print(self.mktSpread);
                mxSpr=max(self.mktSpread); 
                mnSpr=min(self.mktSpread);
                pass;
            else:
                mxSpr=self.mktSpread[-1];mnSpr=self.mktSpread[-1];
                pass;
                
            self.ATR_TypeA=1;
            self.ATR_scRp+=1;
            printBars('ATR1', currentLocation, currentRate, mxSpr, mnSpr);
            # print('ATR1', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
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
                #print('ATR1B ', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
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
                # print(self.mktSpread);
                mxSpr=max(self.mktSpread); 
                mnSpr=min(self.mktSpread);
                pass;
            else:
                mxSpr=self.mktSpread[-1];mnSpr=self.mktSpread[-1];
                pass;

            self.ATR_TypeB=2;
            self.ATR_scRp+=1;
            printBars('ATR2', currentLocation, currentRate, mxSpr, mnSpr);
            # print('ATR2 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
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
                print('ATR2B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
            pass;

        if(currentLocation < -self.motion):
            FT=0;FBT=0; 
            self.ebft-=1;
            
            
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk); 
            
            # print(self.mktTrades[-1]);
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            
            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                # print(self.mktSpread);
                mxSpr=max(self.mktSpread); 
                mnSpr=min(self.mktSpread);
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;
                
            self.ATR_TypeB=3;
            self.ATR_scR-=1;
            printBars('ATR3', currentLocation, currentRate, mxSpr, mnSpr);
            #print('ATR3 ', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ, currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
            #pathC = '{}.{}'.format("ATRC", self.file_name);
            #service.write_file(pathC, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
                    
            if(currentAsk-self.p1 < md.L1.daily_low):
                
                self.ATR_TypeB=3.1;
                self.ATR_scR-=1;
                self.ebft+=1;
                self.neutral+=1;
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                printBars('ATR3-B', currentLocation, currentRate, mxSpr, mnSpr);
                # print('ATR3B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
            pass;
            
        if(currentLocation < -self.active):
            FT=0;FBT=0;
            self.ebft-=1;
            self.mktTrades.append(md.L1.last); 
            marketSpread(currentBid,currentAsk);
            
            #print(self.mktTrades[-1]);
            
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            
            if(len(self.mktSpread)>2):
                # print(self.mktSpread);
                mxSpr=max(self.mktSpread); 
                mnSpr=min(self.mktSpread);
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;
                
            self.ATR_TypeB=4;
            self.ATR_scR-=1;
            printBars('ATR4', currentLocation, currentRate, mxSpr, mnSpr);
            #print('ATR4 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
            
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
                #print('ATR4B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;
            pass;
            

        if(self.chk_SPY > 0.02):
            FT=0;
            FBT=0;
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk); 
            #print(self.mktTrades[-1]);
            
            chkPrints=0;
            if(len(self.mktTrades)>2):
                chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
                pass;
            
            mxSpr=mnSpr=0;
            if(len(self.mktSpread)>2):
                # print(self.mktSpread);
                mxSpr=max(self.mktSpread); 
                mnSpr=min(self.mktSpread);
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
                #print('motion5.1',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                pass;
                
            if(currentRate>self.__class__.spyCHG):
                self.ebft+=1;
                self.motionA=5.2;
                self.mot_scRp+=1;
                #    MOTION 5.2
                printBars('motion5.2', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion5.2',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                #lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('pMax5', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMax5',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('pMin5', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMin5',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('nMax5', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMax5',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('nMin5', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMin5',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
                
            if(FT==0):
                self.neutral+=1;
                printBars('m5_FT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                #print('m5_FT_neutral',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;

            if(self.chk_SPY > 0.04):
                mxSpr=mnSpr=0;
                if(len(self.mktSpread)>2):
                    # print(self.mktSpread);
                    mxSpr=max(self.mktSpread); 
                    mnSpr=min(self.mktSpread);
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
                #print('motion5-B', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('pMax5b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMax5b', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('pMin5b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMin5b', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('nMax5b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMax5b', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;
                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('nMax5b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMax5b', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                    pass;
                if(FBT==0):
                    self.neutral+=2;
                    printBars('m5_FBT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('m5_FBT_neutral', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
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
                mnSpr=min(self.mktSpread);
                pass;
            else:
                mxSpr=self.mktSpread[-1];
                mnSpr=self.mktSpread[-1];
                pass;

            if(currentRate<self.__class__.spyCHG):
                self.ebft-=1;
                self.motionA=6.1;
                self.mot_scR-=1;
                
                #offerInventory = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='increase', order_quantity=self.qty, price=self.pxOFFER, user_key=112, allow_multiple_pending=40)
                printBars('motion6.1', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion6.1', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
            if(currentRate>self.__class__.spyCHG):
                self.ebft+=1;
                self.motionA=6.2;
                self.mot_scRp+=1;
                #lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
                printBars('motion6.2', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion6.2',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('pMax6', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMax6', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('pMin6', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMin6', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('nMax6', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMax6', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('nMin6', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMin6', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
            if(FT==0):
                self.neutral+=1;
                printBars('m6_FT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                #print('m6_FT_neutral', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;

            if(self.chk_SPY < -0.04):
            
                mxSpr=mnSpr=0;
                if(len(self.mktSpread)>2):
                    mxSpr=max(self.mktSpread); 
                    mnSpr=min(self.mktSpread);
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
                #print('motion6-B', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    self.ebft-=1;
                    printBars('pMax6b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMax6b', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('pMin6b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('pMin6b',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;
                    printBars('nMax6b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMax6b',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;
                    printBars('nMax6b', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('nMax6b',     service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                    pass;

                if(FBT==0):
                    self.neutral+=2;
                    printBars('m6_FBT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('m6_FBT_neutral',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                    pass;
                pass;
            pass;
            
        if(self.chk_QQQ > 0.02):
            mxSpr=mnSpr=0;
            
            if(len(self.mktSpread)>2):
                # print(self.mktSpread);
                mxSpr=max(self.mktSpread); 
                mnSpr=min(self.mktSpread);
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
                #print('motion7.1',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
                
            if(currentRate>self.__class__.qqqCHG):
                self.ebft+=1;
                self.motionB=7.2;
                self.mot_scRp+=1;
                #lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.qty, price=self.pxBID, user_key=111, allow_multiple_pending=40);
                printBars('motion7.2', currentLocation, currentRate, mxSpr, mnSpr);
                #print('motion7.2',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
   
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('pMax7', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMax7',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('pMin7', currentLocation, currentRate, mxSpr, mnSpr);
                #print('pMin7',    service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,      self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;
                printBars('nMax7', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMax7',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;
                printBars('nMax7', currentLocation, currentRate, mxSpr, mnSpr);
                #print('nMax7',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                pass;
            if(FT==0):
                self.neutral+=1;
                printBars('m7_FT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                #print('m7_FT_neutral',    service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,    FBT, self.ebft, self.orderBalance);
                pass;
            
            if(self.chk_QQQ > 0.04):
            
                mxSpr=mnSpr=0;
                
                if(len(self.mktSpread)>2):
                    # print(self.mktSpread);
                    mxSpr=max(self.mktSpread); 
                    mnSpr=min(self.mktSpread);
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
                    self.neutral+=2;
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
                mnSpr=min(self.mktSpread);
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
                    self.neutral+=2;
                    printBars('m8_FBT_neutral', currentLocation, currentRate, mxSpr, mnSpr);
                    #print('m8_FBT_neutral',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,     FBT, self.ebft, self.orderBalance);
                    pass;
                pass;
            pass;
            
        if(self.motionA!=0 or self.motionB!=0):
        
            if(self.ATR_scR!=0 or self.mot_scR!=0 or self.xxl_scR!=0):
                #print('\n\nMINUS:\t', self.ATR_scR+self.mot_scR+self.xxl_scR);
                if(self.ATR_scR<=-1 and self.mot_scR<=-1 and self.xxl_scR<=-1):
                    #print('-1');
                    pass;
                if(self.ATR_scR<=-2 and self.mot_scR<=-2 and self.xxl_scR<=-2):
                    #print('-2');
                    pass;
                if(self.ATR_scR<=-3 and self.mot_scR<=-3 and self.xxl_scR<=-3):
                    #print('-3');
                    pass;
                if(self.ATR_scR<=-4 and self.mot_scR<-4 and self.xxl_scR<=-4):
                    #print('-4');
                    pass;
                pass;

            if(self.ATR_scRp!=0 or self.mot_scRp!=0 or self.xxl_scRp!=0):
                #print('\n\nPLUS:\t', self.ATR_scRp+self.mot_scRp+self.xxl_scRp);
                if(self.ATR_scRp>=4 and self.mot_scRp>=4 and self.xxl_scRp>=4):
                    #print('+4');
                    pass;
                if(self.ATR_scRp>=3 and self.mot_scRp>=3 and self.xxl_scRp>=3):
                    #print('+3');
                    pass;
                if(self.ATR_scRp>=2 and self.mot_scRp>=2 and self.xxl_scRp>=2):
                    #print('+2');
                    pass;
                if(self.ATR_scRp>=1 and self.mot_scRp>=1 and self.xxl_scRp>=1):
                    #print('+1');
                    pass;
                pass;
            pass;

        if(self.motionA!=0 or self.motionB!=0):
            #print('systemType=2');               
            self.systemType=2;
            self.systemRevolver.append(self.systemType);
            
            if(self.ATR_TypeB==3 and self.ATR_TypeB==4 and self.motionA==6.1 and self.motionX==6.3 and self.motionB==8.1 and self.motionY==8.3):
                self.systemType=7;
                self.systemRevolver.append(self.systemType);
                pass;
            elif(self.ATR_TypeB==3 and self.motionA==6.1 and self.motionX==6.3 and self.motionB==8.1 and self.motionY==8.3):
                self.systemType=6;
                self.systemRevolver.append(self.systemType);
                pass;
            elif(self.ATR_TypeB==4 and self.motionA==6.1 and self.motionX==6.3 and self.motionB==8.1 and self.motionY==8.3):
                self.systemType=5;
                self.systemRevolver.append(self.systemType);
                pass;
            elif(self.ATR_TypeB==4 and self.ATR_TypeB==3 and self.motionA==6.1 and self.motionB==8.1):
                self.systemType=4;
                self.systemRevolver.append(self.systemType);
            elif(self.ATR_TypeB==4 and self.ATR_TypeB==3 and self.motionA==6.1):
                self.systemType=3;
                self.systemRevolver.append(self.systemType);
            elif(self.ATR_TypeB==4 and self.ATR_TypeB==3 and self.motionA==8.1):
                self.systemType=3;
                self.systemRevolver.append(self.systemType);
            elif(self.ATR_TypeB==3 and self.motionA==6.1 and self.motionB==8.1):
                self.systemType=2;
                self.systemRevolver.append(self.systemType);
            elif(self.ATR_TypeB==4 and self.motionA==6.1 and self.motionB==8.1):
                # self.systemType=1;
                self.systemRevolver.append(self.systemType);
            elif(self.motionA==6.1 and self.motionB==8.1):
                self.systemType=1;
                self.systemRevolver.append(self.systemType);
            elif(self.motionA==6.1):
                self.systemType=0;
                self.systemRevolver.append(self.systemType);
            elif(self.motionB==8.1):
                self.systemType=0;
                self.systemRevolver.append(self.systemType);

            if(self.systemRevolver[-2]!=self.systemRevolver[-1]):
                #if(self.systemRevolver[-1]>self.systemRevolver[-2]): print('definitely moves lower if its quiet'); pass;
                #if(self.systemRevolver[-1]<self.systemRevolver[-2]): print('moves higher only if its quiet.'); pass;
                pass;
            pass;
        pass;
        
        if(self.key==1):
            self.neutralized+=self.neutral;
            s=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
            n=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
            
            
            #print('ebft',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, s, n,  self.neutralized,   self.neutral, self.ebft, self.orderBalance);
            printAction('key', currentLocation, currentRate, s, n, 'ACTION');
            
            if(self.ebft<0):
                self.ebft-=(s+n);
                
                #print('ebft',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, s, n,  self.neutralized,   self.neutral, self.ebft, self.orderBalance);
                printAction('ebft(-)', currentLocation, currentRate, s, n, 'DOWN');
                
                self.bot+=self.neutral;
                self.sold+=self.ebft;
                
                #self.neutral+=s;    
                self.orderSession+=1;
                self.orderBalance+=(self.ebft+self.neutral);
                self.allocationRate+=abs(self.ebft);
                self.orderSell.append([self.symbol, abs(self.ebft)]);
                self.orderBuy.append([self.symbol, self.neutral]);
                
                
                lvlDOWN=abs(self.ATR_scR+self.mot_scR+self.xxl_scR);
                if(lvlDOWN>=3):
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=lvlDOWN, user_key=lvlDOWN);
                    pass;

                printAction('ebft(-)EXCH', currentLocation, currentRate, s, n, 'DOWN');
                #print('ebft_exchg',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, self.ATR_scRp+self.mot_scRp+self.xxl_scRp, self.ATR_scR+self.mot_scR+self.xxl_scR,     'down', self.ebft, self.neutral, self.orderBalance);
                pass;
                
                if(abs(account[self.symbol].position.shares)!=0):
                    printAction('offer', currentLocation, currentRate, s, n, 'DOWN'); 
                    #print('offer',    service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,     self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate,  1, -1, self.neutral, self.ebft, self.ebft+self.neutral, self.orderBalance);
                    self.orderBalance;
                    #tcLong = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(self.ebft), user_key=113, allow_multiple_pending=40);
                    pass;
                    
            if(self.ebft>0):
                self.ebft+=(n+s);
                printAction('ebft(+)', currentLocation, currentRate, s, n, 'UP'); 
                self.bot+=self.ebft;
                self.sold-=self.neutral;
                #print('ebft',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, s, n,  self.neutralized,   self.neutral, self.ebft, self.orderBalance);
         
                #self.neutral+=s;
                self.orderSession+=1; self.orderBalance+=self.ebft-self.neutral; self.allocationRate+=abs(self.ebft); 
                self.orderBuy.append([self.symbol, self.ebft]); self.orderSell.append([self.symbol, self.neutral]);
                lvlUP=self.ATR_scRp+self.mot_scRp+self.xxl_scRp;
                if(lvlUP>=3):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=lvlUP, user_key=lvlUP);
                    pass;
                    
                printAction('ebft(+)EXCH', currentLocation, currentRate, s, n, 'UP');    
                #print('ebftexchg',     service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, self.ATR_scR+self.mot_scR+self.xxl_scR, self.ATR_scRp+self.mot_scRp+self.xxl_scRp,     'up', self.ebft, self.neutral, self.orderBalance);
            
                if(abs(account[self.symbol].position.shares)!=0):
                    printAction('bid', currentLocation, currentRate, s, n, 'UP'); 
                    #print('bid',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, 1, -1, self.ebft, self.neutral, self.ebft-self.neutral, self.orderBalance);
                    self.orderBalance;
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
                    printAction('SELL', currentLocation, currentRate, s, n, 'UP'); 
                    #print('sell',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,    self.chk_SPY, self.chk_QQQ,     currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, 1, -1,     self.orderSession, self.orderBalance, QTY, self.orderBalance);
                    # 1 HOP
                    #order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='exit', user_key=2);
                
                if(self.orderBalance<0):
                    #crsShort = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=abs(QTY), price=self.pxBID, user_key=111, allow_multiple_pending=40);
                    printAction('BUY', currentLocation, currentRate, s, n, 'UP'); 
                    #print('buy',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,    currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, 1, -1, self.orderSession, self.orderBalance, QTY, self.orderBalance);
                    # 1 HOP
                    #order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='exit', user_key=1);
                self.orderBalance=0;
                pass;
            pass;
        pass;
        
    def on_fill(self, event, md, order, service, account):
        self.neutralized-=1;
        pass;
