### RE: Error 2023-08-01 23:29

* LINE 324:  checks quantity
* LINE 333:  checks maxQty (using the BP in self.order_quantity_max) prior to entering conditional order statement.


### RE: Error 2023-08-02 11:23

* ERROR: FF Max Capital 114*1959.99 > 100000
#### TKR: CMG	 	 	 		      NO ORDER	10:36:25	
* LINE 333 will block the Reject.

### RE: Error 2023-08-02 18:15
* I cleared that up.
* Most errors I saw were from maxcap Reject (ref.: 2023-08-02 11:23)
* ref. LINE 333, LINE 324.

# ADDED
* I updated the timer to reduce the number of cancel/reject orders.
LINE 246 - Orderbook Timer to aggregate oddlots into one pending order.
* Did not see any errors from self.procPL21==3 or self.procPL2==4 after the change.

* I'll run it again tomorrow and see how it goes.

## FORWARD TESTING:  8/3/2023

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/2ea97605-111e-4a83-81a6-c4235fa410d3)


## BACKTEST: June, 2023


JUNE BACKTEST RESULTS: 251 SYMBOL UNIVERSE NO REJECTS.

[Trades - Fauconberg TRADE FILE](https://github.com/bdincerTrader/Fauconberg1/files/12253887/Trades.-.Fauconberg.08-03.13_26_44.csv)



[Sumary Table Data](https://github.com/bdincerTrader/Fauconberg1/files/12253886/submission-table-data.15.csv)

/s/ BD.
