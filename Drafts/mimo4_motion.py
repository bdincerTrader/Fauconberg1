from cloudquant.interfaces import Strategy
import datetime, time, random


class locator(Strategy):
    __script_name__ = 'locate1'
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return md.stat.prev_close>5.00 and md.stat.atr>5;
     
    def on_start(self, md, order, service, account):
        self.motion = md.stat.atr;
        self.active = self.motion*1.5;
        self.zero = md.stat.prev_close;
        self.triggerHigh = self.motion-self.zero;
        self.triggerLow = self.zero-self.motion;
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=1), repeat_interval=service.time_interval(minutes=1), timer_id="motionDetected");
        
        
        self.TradeDate=service.time_to_string(service.system_time)
        print(self.TradeDate)
        
        result = datetime.datetime.strptime(self.TradeDate,'%Y-%m-%d %H:%M:%S.%f')
        print(result)
        result.strftime("%b %d %Y %H:%M:%S")
        print(result)
        print(result.strftime("%Y-%d %H:%M:%S"))
        self.file_name = '{}--{}.csv'.format(self.symbol, result.strftime("%Y-%m-%d"))
        self.axcelFileDate=result.strftime("%Y-%m-%d")+self.symbol;
        
    def on_timer(self, event, md, order, service, account):
        currentBid = md.L1.bid;
        currentLocation =  currentBid - self.zero;
        
        # MOTION 1 + #
        if(currentLocation > self.motion):
            print('ATR 1: ', self.symbol, md.L1.bid, md.L1.last, md.L1.ask);
            pathA = '{}.{}'.format("ATRA", self.file_name)
            print(pathA)
            service.write_file(pathA, '{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, md.L1.bid, md.L1.last, md.L1.ask, currentLocation));
        
        # MOTION 2 + #
        if(currentLocation > self.active):
            print('ATR 2: ', self.symbol, md.L1.bid, md.L1.last, md.L1.ask);
            pathB = '{}.{}'.format("ATRB", self.file_name)
            print(pathB)
            service.write_file(pathB, '{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, md.L1.bid, md.L1.last, md.L1.ask, currentLocation));
            
        # MOTION 3 - #
        if(currentLocation < -self.motion):
            print('ATR 3: ', self.symbol, md.L1.bid, md.L1.last, md.L1.ask);
            pathC = '{}.{}'.format("ATRC", self.file_name)
            print(pathC)
            service.write_file(pathC, '{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, md.L1.bid, md.L1.last, md.L1.ask, currentLocation));
            
        # MOTION 4 - #
        if(currentLocation < -self.active):
            print('ATR 4: ', self.symbol, md.L1.bid, md.L1.last, md.L1.ask);
            pathD = '{}.{}'.format("ATRD", self.file_name)
            print(pathD)
            service.write_file(pathD, '{},{},{},{},{},{}'.format(self.axcelFileDate, self.symbol, md.L1.bid, md.L1.last, md.L1.ask, currentLocation));
            
        return;    
        
