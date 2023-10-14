from cloudquant.interfaces import Strategy
import datetime, time, random


class locator(Strategy):
    __script_name__ = 'locate1'

    spyCHG =0.00;
    qqqCHG =0.00;
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return md.stat.prev_close>50.00 and md.stat.atr>5 or symbol=="SPY" or symbol=="QQQ"

    def on_start(self, md, order, service, account):
        if("+" in self.symbol):
            return;
        
        if(self.symbol=="MIMO+A"):
            return;
        
        self.key=0;
        self.mktSpread=[];
        self.mktTrades=[];
        self.orderBuy=[];
        self.orderSell=[];
        self.neutral=0;
        self.neutralized=0;
        self.releaseRate=0;
        self.orderSession=0;
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
        
        result = datetime.datetime.strptime(self.TradeDate,'%Y-%m-%d %H:%M:%S.%f')
        print(result)
        result.strftime("%b %d %Y %H:%M:%S")
        #print(result)
        print(result.strftime("%Y-%d %H:%M:%S"), self.symbol)
        self.file_name = '{}--{}.csv'.format(self.symbol, result.strftime("%Y-%m-%d"))
        self.axcelFileDate=result.strftime("%Y-%m-%d")+self.symbol;
        self.ebft=0;
        self.mktTrades.append(self.zero);
        
    def on_timer(self, event, md, order, service, account):
       
        
        def marketSpread(b, a):
            self.key=1;
            #print('mk spr: ', self.symbol, b, a);
            if(((a+b)/2)>b and ((a+b)/2)<a):
                self.mktSpread.append(a-b);
            return a-b;
        
        self.neutral=0;
        currentBid = md.L1.bid;
        currentAsk = md.L1.ask;

        currentLocation =  currentBid - self.zero;
        currentRate = currentLocation/self.zero;
        

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
        
        
        self.ebft=0;
        # MOTION 1 + #
        if(currentLocation > self.motion):
            FT=0;FBT=0;
            self.ebft+=1;
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            print('ATR1 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            #pathA = '{}.{}'.format("ATRA", self.file_name);
            #service.write_file(pathA, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentBid+self.p1 > md.L1.daily_high):
                # FIFTH UNIT OF INDICATION, MAXIMUM
                print('ATR1B ', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
  
        if(currentLocation > self.active):
            FT=0;FBT=0;
            self.ebft+=1;
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            print('ATR 2 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            #pathB = '{}.{}'.format("ATRB", self.file_name);
            #service.write_file(pathB, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentBid+self.p1 > md.L1.daily_high):
                # FIFTH UNIT OF INDICATION, MAXIMUM
                print('ATR2B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

        if(currentLocation < -self.motion):
            FT=0;FBT=0;
            self.ebft-=1;
            #print('GPS', currentLocation, -self.motion)
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);

            print('ATR3 ', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            #pathC = '{}.{}'.format("ATRC", self.file_name);
            #service.write_file(pathC, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));

            if(currentAsk-self.p1 < md.L1.daily_low):
                # FIFTH UNIT OF INDICATION, MINIMUM
                print('ATR3B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
        
        if(currentLocation < -self.active):
            FT=0;FBT=0;
            self.ebft-=1;
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);

            print('ATR4 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            #pathD = '{}.{}'.format("ATRD", self.file_name);
            #service.write_file(pathD, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentAsk-self.p1 < md.L1.daily_low):
                # FIFTH UNIT OF INDICATION, MINIMUM
                print('ATR4B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

        # MOTION 5 - #
        if(self.chk_SPY > 0.02):
            FT=0;FBT=0;
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
        
            print('motion5',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate<self.__class__.spyCHG):
                self.ebft-=2;
                print('motion5.1',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate>self.__class__.spyCHG):
                self.ebft+=2;
                print('motion5.2',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            

            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('pMax5',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('pMin5',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
                
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('nMax5',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('nMin5',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(FT==0):
                self.neutral+=1;
                print('m5_FT_neutral',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            

            if(self.chk_SPY > 0.04):
                
                print('motion5-B',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('pMax5b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('pMin5b',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('nMax5b',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('nMin5b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(FBT==0):
                    self.neutral+=2;
                    print('m5_FBT_neutral',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            

        # MOTION 6 - #
        if(self.chk_SPY < -0.02):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            FT=0;FBT=0;

            #print(self.mktSpread);
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            
            print('motion6',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate<self.__class__.spyCHG):
                self.ebft-=2;
                print('motion6.1',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate>self.__class__.spyCHG):
                self.ebft+=2;
                print('motion6.2',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('pMax6',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('pMin6',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
                
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('nMax6',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('nMin6',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

            if(FT==0):
                self.neutral+=1;
                print('m6_FT_neutral',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            

            if(self.chk_SPY < -0.04):
                print('motion6-B',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('pMax6b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('pMin6b',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('nMax6b',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('nMin6b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(FBT==0):
                    self.neutral+=2;
                    print('m6_FBT_neutral',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            
        if(self.chk_QQQ > 0.02):
            FT=0;FBT=0;
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            #print('8',currentBid,currentAsk);
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);

            
            print('motion7',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate<self.__class__.qqqCHG):
                self.ebft-=2;
                print('motion7.1',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate>self.__class__.qqqCHG):
                self.ebft+=2;
                print('motion7.2',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
                    
   
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('pMax7',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('pMin7',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('nMax7',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('nMin7',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

            if(FT==0):
                self.neutral+=1;
                print('m7_FT_neutral',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(self.chk_QQQ > 0.04):

                print('motion7-B',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('pMax7b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('pMin7b',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('nMax7b',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('nMin7b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
                
                if(FBT==0):
                    self.neutral+=2;
                    print('m7_FBT_neutral',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

        if(self.chk_QQQ < -0.02):
            FT=0;FBT=0;
            self.mktTrades.append(md.L1.last);
            #print('8',currentBid,currentAsk);
            chk1=marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            print('motion8',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate<self.__class__.qqqCHG):
                self.ebft-=2;
                print('motion8.1',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(currentRate>self.__class__.qqqCHG):
                self.ebft+=2;
                print('motion8.2',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);


            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('pMax8',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('pMin8',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
                
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                FT-=1;self.ebft-=1;
                print('nMax8',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                FT+=1;self.ebft+=1;
                print('nMin8',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

            if(FT==0):
                self.neutral+=1;
                print('m8_FT_neutral',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
            
            if(self.chk_QQQ < -0.04):
 
                print('motion8-B',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
        
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('pMax8b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('pMin8b',  service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    FBT-=1;self.ebft-=1;
                    print('nMax8b',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    FBT+=1;self.ebft+=1;
                    print('nMin8b',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);

                if(FBT==0):
                    #FTB multiplier.
                    self.neutral+=2;
                    print('m8_FBT_neutral',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr, FT,  FBT, self.ebft);
       
        if(self.key==1):
            
            self.neutralized+=self.neutral;
            
            print('ebft',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, max(self.mktSpread), min(self.mktSpread),  self.ebft,   self.ebft, self.ebft);

            if(self.ebft<0):
                self.orderSession+=1;
                self.releaseRate+=abs(self.ebft);
                self.orderSell.append([self.symbol, abs(self.ebft)])
                self.orderBuy.append([self.symbol, self.neutral])
                print('offer',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, max(self.mktSpread), min(self.mktSpread), self.neutral, self.ebft, self.ebft+self.neutral);
                pass;
            if(self.ebft>0):
                self.orderSession+=1;
                self.releaseRate+=abs(self.ebft);
                self.orderBuy.append([self.symbol, self.ebft])
                self.orderSell.append([self.symbol, self.neutral])
                print('bid',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, max(self.mktSpread), min(self.mktSpread), self.ebft, self.neutral, self.ebft-self.neutral);
                pass;

            if(self.orderSession>0):
                self.releaseRate/self.orderSession;
             
            if(self.orderSession>0 and):
                
    def on_fill(self, event, md, order, service, account):
        self.neutralized-=1;
        pass;
