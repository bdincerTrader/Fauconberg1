# https://youtu.be/g8p22U-5yVA?t=42
from cloudquant.interfaces import Strategy, Event
import ktgfunc

class Gr8Script4bb0b98126b74dc69548d1a3825b6b23(Strategy):
    __script_name__ = 'gaspard'

    bpRisk=50000; cycl=5; askRTE=1.0026; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; plUpperBand=bpRisk*.01; plLowerBand=-bpRisk*.01; plBandMult=bpRisk*.01; 

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'MSFT'

    def on_start(self, md, order, service, account):
        self.itr=0
        self.dataPt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMS =[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMSB =[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMSC =[[],[],[],[],[],[],[],[],[],[],[],[],[]]
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=45), repeat_interval=service.time_interval(seconds=3), timer_id="Allocate")
        # ATR over 10 days based on an underlying 250 days of TR (True Range). USE TA Lib# 21 day avg vol.
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;

        
        
    def on_timer(self, event, md, order, service, account):
        
        #print(self.symbol, self.itr, self._prev_close, self._atr, md.L1.bid_exchange, md.L1.bid, md.L1.last, md.L1.ask_exchange, md.L1.ask, md.L1.exchange, md.L1.daily_high, md.L1.daily_low, md.L1.gap)
        self.dataPt.append([self.symbol, 0, self.itr, md.L1.exchange, md.L1.ask_exchange, md.L1.bid_exchange, md.L1.last,  md.L1.bid, md.L1.ask, md.L1.daily_high, md.L1.daily_low,  self._prev_close, md.L1.closing_trade, self._atr])

        barA=md.bar.minute(start=-32, end=None, include_empty=False, include_extended=True, bar_size=1, today_only=True)
        rangeMS = min(len(barA.timestamp), len(barA.askvol), len(barA.bidvol), len(barA.bvwap), len(barA.close), len(barA.count), len(barA.high), len(barA.low), len(barA.open), len(barA.spread), len(barA.volume))
        for idx in range(0, rangeMS, 1):
            self.dataBookMS.append([self.symbol, 32,  self.itr, barA.timestamp[idx], barA.askvol[idx], barA.bidvol[idx], barA.bvwap[idx], barA.close[idx], barA.open[idx], barA.high[idx], barA.low[idx], barA.count[idx], barA.spread[idx], barA.volume[idx]])
        
        barB=md.bar.minute(start=-20, end=None, include_empty=False, include_extended=True, bar_size=2, today_only=True)        
        rangeMSB = min(len(barB.timestamp), len(barB.askvol), len(barB.bidvol), len(barB.bvwap), len(barB.close), len(barB.count), len(barB.high), len(barB.low), len(barB.open), len(barB.spread), len(barB.volume))
        for idxB in range(0, rangeMSB, 1):
            self.dataBookMSB.append([self.symbol, 20,  self.itr, barB.timestamp[idxB], barB.askvol[idxB], barB.bidvol[idxB], barB.bvwap[idxB], barB.close[idxB], barB.open[idxB], barB.high[idxB], barB.low[idxB], barB.count[idxB], barB.spread[idxB], barB.volume[idxB]])

        self.itr+=1;

    def on_finish(self, md, order, service, account):
        filenameDT=self.symbol+"-DT.txt"
        for aLoop in self.dataPt:
            for diLoop in aLoop:
                service.write_file(filenameDT, '{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(diLoop[0],diLoop[1],diLoop[2],diLoop[3],diLoop[4],diLoop[5],diLoop[6],diLoop[7],diLoop[8],diLoop[9],diLoop[10],diLoop[11],diLoop[12],diLoop[13]))

        filenameMS=self.symbol+"-A1.txt"
        for hLoop in self.dataBookMS:
            for diLoop in hLoop:
                service.write_file(filenameMS, '{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(diLoop[0],diLoop[1],diLoop[2],diLoop[3],diLoop[4],diLoop[5],diLoop[6],diLoop[7],diLoop[8],diLoop[9],diLoop[10],diLoop[11],diLoop[12],diLoop[13]))

        filenameMSC=self.symbol+"-A2.txt"
        for loopLoop in self.dataBookMSB:
            for diLoop in loopLoop:
                service.write_file(filenameMSC, '{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(diLoop[0],diLoop[1],diLoop[2],diLoop[3],diLoop[4],diLoop[5],diLoop[6],diLoop[7],diLoop[8],diLoop[9],diLoop[10],diLoop[11],diLoop[12],diLoop[13]))
