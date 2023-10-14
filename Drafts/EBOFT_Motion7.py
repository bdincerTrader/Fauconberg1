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

        self.mktSpread=[];
        self.mktTrades=[];
        self.motion = md.stat.atr;
        self.p1 = self.motion*0.01;
        self.active = self.motion*1.5;
        self.zero = md.stat.prev_close;
        self.triggerHigh = self.motion-self.zero;
        self.triggerLow = self.zero-self.motion;
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(minutes=2), timer_id="motionDetected");
        self.chk_SPY=self.chk_QQQ = 0;
        self.chkATR=self.motion*.015;
        self.TradeDate=service.time_to_string(service.system_time)
        print(self.TradeDate)
        
        result = datetime.datetime.strptime(self.TradeDate,'%Y-%m-%d %H:%M:%S.%f')
        print(result)
        result.strftime("%b %d %Y %H:%M:%S")
        #print(result)
        print(result.strftime("%Y-%d %H:%M:%S"), self.symbol)
        self.file_name = '{}--{}.csv'.format(self.symbol, result.strftime("%Y-%m-%d"))
        self.axcelFileDate=result.strftime("%Y-%m-%d")+self.symbol;
        
        self.mktTrades.append(self.zero);
        
    def on_timer(self, event, md, order, service, account):
       
    
        def marketSpread(b, a):
            #print('mk spr: ', self.symbol, b, a);
            if(((a+b)/2)>b and ((a+b)/2)<a):
                self.mktSpread.append(a-b);
            return a-b;
        
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
        
        
        
        # MOTION 1 + #
        if(currentLocation > self.motion):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            print('ATR1 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            pathA = '{}.{}'.format("ATRA", self.file_name);
            service.write_file(pathA, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentBid+self.p1 > md.L1.daily_high):
                print('ATR1B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
  
        if(currentLocation > self.active):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            print('ATR 2 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            pathB = '{}.{}'.format("ATRB", self.file_name);
            service.write_file(pathB, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentBid+self.p1 > md.L1.daily_high):
                print('ATR2B ', service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

        if(currentLocation < -self.motion):
            print('GPS', currentLocation, -self.motion)
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);

            print('ATR3 ', service.time_to_string(service.system_time),  self.symbol, self.zero,md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            #pathC = '{}.{}'.format("ATRC", self.file_name);
            #service.write_file(pathC, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));

            if(currentAsk-self.p1 < md.L1.daily_low):
                print('ATR3B ', service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
        
        if(currentLocation < -self.active):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);

            print('ATR4 ', service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            #pathD = '{}.{}'.format("ATRD", self.file_name);
            #service.write_file(pathD, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentAsk-self.p1 < md.L1.daily_low):
                print('ATR4B ', service.time_to_string(service.system_time),  self.symbol, self.zero,md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

        # MOTION 5 - #
        if(self.chk_SPY > 0.02):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
        
            print('motion5',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            
            if(currentRate<self.__class__.spyCHG):
                print('motion5.1',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);
            
            if(currentRate>self.__class__.spyCHG):
                print('motion5.2',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);
            

            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                print('pMax5',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                print('pMin5',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
                
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                print('nMax5',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                print('nMin5',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

            if(self.chk_SPY > 0.04):
                print('motion5-B',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('pMax5b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('pMin5b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('nMax5b',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('nMin5b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );



        # MOTION 6 - #
        if(self.chk_SPY < -0.02):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);

            #print(self.mktSpread);
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            
            print('motion6',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            
            if(currentRate<self.__class__.spyCHG):
                print('motion6.1',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);
            
            if(currentRate>self.__class__.spyCHG):
                print('motion6.2',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);
            
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                print('pMax6',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                print('pMin6',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
                
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                print('nMax6',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                print('nMin6',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

            if(self.chk_SPY < -0.04):
                print('motion6-B',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
                
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('pMax6b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('pMin6b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('nMax6b',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('nMin6b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );


        if(self.chk_QQQ > 0.02):
            self.mktTrades.append(md.L1.last);
            marketSpread(currentBid,currentAsk);
            #print('8',currentBid,currentAsk);
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);

            
            print('motion7',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            
            if(currentRate<self.__class__.qqqCHG):
                print('motion7.1',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);
            
            if(currentRate>self.__class__.qqqCHG):
                print('motion7.2',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);
                    
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                print('pMax7',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                print('pMin7',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                print('nMax7',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                print('nMin7',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

            if(self.chk_QQQ > 0.04):
                print('motion7-B',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('pMax7b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('pMin7b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('nMax7b',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('nMin7b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
                
                
        if(self.chk_QQQ < -0.02):
            self.mktTrades.append(md.L1.last);
            #print('8',currentBid,currentAsk);
            chk1=marketSpread(currentBid,currentAsk);
            
            chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
            mxSpr=max(self.mktSpread);
            mnSpr=min(self.mktSpread);
            print('motion8',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
            
            if(currentRate<self.__class__.qqqCHG):
                print('motion8.1',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);
            
            if(currentRate>self.__class__.qqqCHG):
                print('motion8.2',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr);

            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                print('pMax8',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                print('pMin8',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
                
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                print('nMax8',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );
           
            if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                print('nMin8',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

            
            if(self.chk_QQQ < -0.04):
                print('motion8-B',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr); 
        
                if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('pMax8b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('pMin8b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mxSpr):
                    print('nMax8b',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,   self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );

                if(chkPrints<self.chkATR and self.mktSpread[-1]==mnSpr):
                    print('nMin8b',  service.time_to_string(service.system_time),   self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask, self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate, mxSpr, mnSpr );


            
