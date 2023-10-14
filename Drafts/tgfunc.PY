from cloudquant.interfaces import Strategy, Event
import ktgfunc

class Gr8Script73dd21b7bdd74364a663afa51a5e4392(Strategy):
    __script_name__ = 'CARLYLE'
    CASH_PER_SYMBOL=500000
    ACCOUNT_LOSS_LIMIT=500000
    SYMBOL_LOSS_LIMIT=100000

    # tickerItrB = ['ADBE','ASML','AVGO','AZO','BIO','BKNG','BLK','GS','MS','COST','CMG','DDS','DECK','ELV','EQIX','FCNCA','FDS','FICO','FNGU','GWW','HUBS','HUM','IDXX','IIVI','INTU','KLAC','LRCX','MDB','MDGL','MELI','MPWR','MSCI','MSTR','MTD','NFLX','NOW','NVDA','ORLY','REGN','SAIA','SEDG','SMCI','SNPS','SOXX','SWAV','TDG','TMO','TSLA','ULTA','UNH','URI','SPY','QQQ'];
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        #return symbol == 'AAL'
        return md.stat.prev_close>50.00 and md.stat.atr>5 and md.stat.avol>175000;
        
    def on_start(self, md, order, service, account):
        self.cash_allocation = self.__class__.CASH_PER_SYMBOL;
        self.tracking_ON = md.market_open_time + service.time_interval(minutes=20)
        self.tracking_OFF = md.market_close_time - service.time_interval(hours=2)
        self.regITR=0;
        self.obs_VWAP=[];
        self.vwap_TRACKER=[];
        self.vwap_TTL_CTR=0.00;
        self.vwap_PCT_CTR=0.00;
        pass;
        
    def on_minute_bar(self, event, md, order, service, account, bar):
        # [1]   The system only allocates during a specified time interval of the day (9:50AM - 2:00PM).
        if(event.timestamp<self.tracking_ON or event.timestamp>self.tracking_OFF):
            return;
        
        bar_2m = bar.minute_by_index(-1)
        if(len(bar_2m.bvwap)<1):
            return;
            
        self.obs_VWAP.append(bar_2m.bvwap[-1])
        
        self.regITR+=1;
        if(len(self.obs_VWAP)>1):
            vwap_PX1_CHG = self.obs_VWAP[-1]-self.obs_VWAP[-2]
            vwap_PCT_CHG = vwap_PX1_CHG / (self.obs_VWAP[-2]+0.000001)
            self.vwap_TTL_CTR += vwap_PX1_CHG;
            self.vwap_PCT_CTR += vwap_PCT_CHG;
            vwap_AVG_PTS = self.vwap_TTL_CTR/self.regITR;
            vwap_AVG_RTE = self.vwap_PCT_CTR/self.regITR;
            vwap_WGT_CHG = vwap_PX1_CHG/(vwap_AVG_PTS+0.000001)
            vwap_WGT_RTE = vwap_PCT_CHG/(vwap_AVG_RTE+0.000001)
            self.vwap_TRACKER.append(vwap_AVG_RTE)
        
        #if(account[self.symbol].unrealized_pl.entry_pl>0):
        #    if(account[self.symbol].position.shares<0):
        #        short_spr = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='exit', user_key=666.999, allow_multiple_pending=40);  
        #        pass;
        #    else:
        #        long_spr = order.algo_sell(self.symbol, algorithm='398a38ee-b614-4678-90a6-dbf40d2a54b9', intent='exit', user_key=999.666, allow_multiple_pending=40);
        #        pass;
                
        # [2]   The system extrapolates the anticipated price direction forward 30 minutes using a 15-minute regression of fwd rate trajectory guidance.
        if(self.regITR%10 == 0 and len(self.vwap_TRACKER)>15):
            rng15 = sum(self.vwap_TRACKER[-15:]) /15;
            fwd30 = 1+(rng15*30)
            px2 = self.obs_VWAP[-1]*fwd30;
            print("TICKER: {}\t rng15: {:.8f}\t fwd30: {:.8f}\t\t VWAP: {:.5f} \t PX1: {:.5f}\t\t{}".format(self.symbol, rng15, fwd30, self.obs_VWAP[-1], px2, service.time_to_string(service.system_time)))
            
            if(px2>self.obs_VWAP[-1]):
                SHARES_PER_SYMBOL=int(self.cash_allocation/md.L1.bid)
                init = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='none', order_quantity=SHARES_PER_SYMBOL, user_key=999, allow_multiple_pending=40);  
                service.write_file("01_carlyle"+self.symbol+".txt",'{},{},{},{},{},{}'.format(self.regITR, service.time_to_string(service.system_time), self.symbol, self.obs_VWAP[-1], px2, 1), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                pass;
            elif(px2<self.obs_VWAP[-1]):
                SHARES_PER_SYMBOL=int(self.cash_allocation/md.L1.bid)
                init = order.algo_sell(self.symbol, algorithm='398a38ee-b614-4678-90a6-dbf40d2a54b9', intent='none', order_quantity=SHARES_PER_SYMBOL, user_key=666.999, allow_multiple_pending=40);
                service.write_file("01_carlyle"+self.symbol+".txt",'{},{},{},{},{},{}'.format(self.regITR, service.time_to_string(service.system_time), self.symbol, self.obs_VWAP[-1], px2, -1), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                pass;
            pass;
        pass;
        
    def on_timer(self, event, md, order, service, account):
        pass;
        
    def on_fill(self, event, md, order, service, account):
        pass;

        # print(service.time_to_string(service.system_time))
        # print(event.timestamp, event.symbol, event.length, event.open, event.high, event.low, event.close, event.volume, event.vwap, event.spread, event.bidvol, event.askvol, event.count)
        # self.dataBookMS[self.itr][RATE_CHK+4]=sum(self.dataBookMS[self.itr][17:26])/9;
        # one_minute = bar.minute(include_extended = True)
        
        
