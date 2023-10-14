from cloudquant.interfaces import Strategy, Event
import ktgfunc, datetime

class imbalanceTrade(Strategy):
    #tickerItr = ['AA','AAL','AAP','BEAM','BG','BAM','AXP']
    tickerItr = ['AXP']
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in imbalanceTrade.tickerItr

    def on_start(self, md, order, service, account):
        self.TradeDate=service.time_to_string(service.system_time)
        #time2=service.system_time.strftime("%b %d %Y")
        #print(time2)
        print(self.TradeDate)
        #format: str='%Y-%m-%d %H:%M:%S.%f
         
        result = datetime.datetime.strptime(self.TradeDate,'%Y-%m-%d %H:%M:%S.%f')
        print(result)
        result.strftime("%b %d %Y %H:%M:%S")
        print(result)
        print(result.strftime("%Y-%d %H:%M:%S"))
        
        self.file_name = '_{}--{}-balanceImbalance.csv'.format(self.symbol, result.strftime("%Y-%m-%d"))
        
        self.axcelFileDate=result.strftime("%Y-%m-%d")
        
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(minutes=1), timer_id="Allocate")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=1), timer_id = "checkPositions")
        service.add_time_trigger(md.market_close_time - service.time_interval(seconds=30), timer_id = "checkAgain")
        service.write_file(self.file_name,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('date','_time', '_symbol','_atr', '_avol' , '_beta', '_prev_close',' _open',' _chg_from_open',' _pct_chg_open',' _rvol',' _bid',' _ask',' _last',' _last_size',' _core_acc_vol',' _agr_ask_sz',' _agr_bid_sz',' _d_spread',' _d_vwap',' _d_high',' _d_low',' _m_vwap',' _acc_volume',' _d_bidvol',' _d_askvol',' _d_count','bvwap[-1]',' askvol[-1]',' bidvol[-1]',' close[-1]',' count[-1]',' high[-1]',' low[-1]',' open[-1]',' spread[-1]',' volume[-1]'))      
        
        # over 10 days based on an underlying 250 days of TR (True Range). You can use TA Lib to create alternative timeframes.
        self._atr=md.stat.atr
        # 21 day avg vol.
        self._avol=md.stat.avol
        self._beta=md.stat.beta
        self._prev_close=md.stat.prev_close
    
    def on_timer(self, event, md, order, service, account):
        
        timerID = datetime.datetime.strptime(service.time_to_string(service.system_time),'%Y-%m-%d %H:%M:%S.%f')
        idxBar=md.bar.minute_by_index(-9)
        print(timerID.strftime("%H.%M"))
        
        
        #for _dat in range(0, 9, 1):
        #    print(timerID.strftime("%H.%M"), _dat, md.L1.minute_vwap, idxBar.bvwap[_dat], idxBar.askvol[_dat], idxBar.bidvol[_dat], idxBar.close[_dat], idxBar.count[_dat], idxBar.high[_dat], idxBar.low[_dat], idxBar.open[_dat], idxBar.spread[_dat], idxBar.volume[_dat])
        
        
        
        
        
        service.write_file(self.file_name,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.axcelFileDate, timerID.strftime("%H.%M"), self.symbol, self._atr, self._avol , self._beta, self._prev_close, md.L1.open,md.L1.change_from_open, md.L1.percent_change_from_open, md.L1.rvol, md.L1.bid, md.L1.ask, md.L1.last, md.L1.last_size, md.L1.core_acc_volume, md.L1.agr_bid_size, md.L1.agr_ask_size, md.L1.daily_spread, md.L1.daily_vwap, md.L1.daily_high, md.L1.daily_low, md.L1.minute_vwap, md.L1.core_acc_volume, md.L1.daily_bidvol, md.L1.daily_askvol, md.L1.daily_count,idxBar.bvwap[-1], idxBar.askvol[-1], idxBar.bidvol[-1], idxBar.close[-1], idxBar.count[-1], idxBar.high[-1], idxBar.low[-1], idxBar.open[-1], idxBar.spread[-1], idxBar.volume[-1]))      
        pass
