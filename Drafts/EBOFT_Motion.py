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
        
        self.mktSpread=self.mktTrades=[];
        self.motion = md.stat.atr;
        self.p1 = self.motion*0.01;
        self.active = self.motion*1.5;
        self.zero = md.stat.prev_close;
        self.triggerHigh = self.motion-self.zero;
        self.triggerLow = self.zero-self.motion;
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=1), repeat_interval=service.time_interval(minutes=1), timer_id="motionDetected");
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
        
        self.mktTrades.append(self.zero);
        
    def on_timer(self, event, md, order, service, account):
       
        currentBid = md.L1.bid;
        currentAsk = md.L1.ask;
        currentLocation =  currentBid - self.zero;
        currentRate = currentLocation/self.zero;
        
        self.mktSpread.append(md.L1.ask - md.L1.bid);
        self.mktTrades.append(md.L1.last);
        
        chkPrints=self.mktTrades[-1]-self.mktTrades[-2];
        mxSpr=max(self.mktSpread);
        mnSpr=min(self.mktSpread);
        
        
        if(self.symbol=='SPY'):
            self.__class__.spyCHG=currentLocation/self.zero;
            #print(self.__class__.spyCHG)
            pass;
        elif(self.symbol=='QQQ'):
            self.__class__.qqqCHG=currentLocation/self.zero;
            #print(self.__class__.qqqCHG)
            
            pass;
        else:
            self.chk_SPY = currentRate - self.__class__.spyCHG;
            self.chk_QQQ = currentRate - self.__class__.qqqCHG;
            
        
        # MOTION 1 + #
        if(currentLocation > self.motion):
            print('ATR 1 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            pathA = '{}.{}'.format("ATRA", self.file_name);
            service.write_file(pathA, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentBid+self.p1 > md.L1.daily_high):
                print('ATR 1B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
        
        # MOTION 2 + #
        if(currentLocation > self.active):
            print('ATR 2 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            pathB = '{}.{}'.format("ATRB", self.file_name);
            service.write_file(pathB, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentBid+self.p1 > md.L1.daily_high):
                print('ATR 2B ', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
                
            
        # MOTION 3 - #
        if(currentLocation < -self.motion):
            print('ATR 3 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            pathC = '{}.{}'.format("ATRC", self.file_name);
            service.write_file(pathC, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentAsk-self.p1 < md.L1.daily_low):
                print('ATR 3B ', service.time_to_string(service.system_time),self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);

        # MOTION 4 - #
        if(currentLocation < -self.active):
            print('ATR 4 ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            pathD = '{}.{}'.format("ATRD", self.file_name);
            service.write_file(pathD, '{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, service.time_to_string(service.system_time), md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate));
            
            if(currentAsk-self.p1 < md.L1.daily_low):
                print('ATR 4B ', service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);

        # MOTION 5 - #
        if(self.chk_SPY > 0.02):
            print('motion 5',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                print('motion 5-MX1',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                print('motion 5-MN1',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
                
            if(chkPrints<-self.chkATR and self.mktSpread[-1]==mxSpr):
                print('motion 5-MX3',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
           
            if(chkPrints<-self.chkATR and self.mktSpread[-1]==mnSpr):
                print('motion 5-MX4',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);


            if(self.chk_SPY > 0.04):
                print('motion 5-B',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
                

        # MOTION 6 - #    
        if(self.chk_SPY < -0.02):
            print('motion 6',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                print('motion 6-MX1',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                print('motion 6-MN1',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
                
            if(chkPrints<-self.chkATR and self.mktSpread[-1]==mxSpr):
                print('motion 6-MX3',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
           
            if(chkPrints<-self.chkATR and self.mktSpread[-1]==mnSpr):
                print('motion 6-MX4',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            


            
            
            if(self.chk_SPY < -0.04):
                print('motion 6-B',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
                
        if(self.chk_QQQ > 0.02):
           
            print('motion 7',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
                       
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mxSpr):
                print('motion 7-MX1',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
           
            if(chkPrints>self.chkATR and self.mktSpread[-1]==mnSpr):
                print('motion 7-MN1',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
                
            if(chkPrints<-self.chkATR and self.mktSpread[-1]==mxSpr):
                print('motion 7-MX3',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
           
            if(chkPrints<-self.chkATR and self.mktSpread[-1]==mnSpr):
                print('motion 7-MX4',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            

            if(self.chk_QQQ > 0.04):
                print('motion 7-B',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);

        if(self.chk_QQQ < -0.02):
            print('motion 8',  service.time_to_string(service.system_time), self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
            
            if(self.chk_QQQ < -0.04):
                print('motion 8-B',  service.time_to_string(service.system_time),  self.symbol, self.zero, md.L1.bid, md.L1.last, md.L1.ask,  self.chk_SPY, self.chk_QQQ,  currentLocation, self.__class__.spyCHG, self.__class__.qqqCHG, currentRate);
        return;    
