I made a copy of Fauconberg under the BDincer Kore so I can compare one versus the other. I added the variables and structures to Fauconberg as a precursor, I need to see how it performs in FWD testing before I add the Risk Mgmt Procedures onto Fauconberg.

I added a few elements to control the Max Cap and Unit Allocation Procedures in Fauconberg.

I ran the most recent backtest using 10/20/30K denoms and this was the result.


BDincer Kore


(-) TIMER.
(-) i must get this whole selling timer fixed this afternoon.


9:51:27	
F	B	20	MELI	1336.59	NSDQ

** continuously cancelled the sales 

  
C	SS	20	MELI	1338.24	ARCA	062E3138303E-402	9:53:20	BDincer Kore	User Canceled
C	SS	20	MELI	1338.24	ARCA	062E1-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.54	ARCA	062E1-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.54	ARCA	062E694C2221-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.54	ARCA	062E1-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.54	ARCA	062E1-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.07	ARCA	062E694C2221-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.07	ARCA	062E694C2221-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.07	ARCA	062E1303932-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1342.07	ARCA	062E694C2221-402	9:53:20	BDincer Kore	User Canceled
C	SS	120	MELI	1333.16	NSDQ	062E1-402	9:53:20	BDincer Kore	User Canceled
C	SS	10	MELI	1341.37	ARCA	062E694C2221-402	9:53:20	BDincer Kore	User Canceled

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/32aa56d9-aef2-417f-a2ce-17ca2c35013b)



* it is supposed to offload a small amount at a time when certain price conditions are met.
C	SS	20	MSTR	392.75	ARCA	062E1-402	9:53:20	BDincer Kore	User Canceled

R	 	 	MSTR	 	 	 	9:57:00	BDincer Kore	failed pending order check -- num_pending= 41	NO ORDER

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/24afd7e7-6cce-47ea-a46d-2cfee8a48b89)




HASH     6df1a0d2dc9b73bdcb6f16fd0d84c0bc

- No EOD positions.
- Fewer trades.
- More precision.
- 75 Trades

I don't think that volume is possible for this ticker.

I'll see what the FWD Test does today. 

Comparing AAPL to AAPL, for example - usin gthose two accounts.

[trades-table-data (3).csv](https://github.com/bdincerTrader/Fauconberg1/files/12303057/trades-table-data.3.csv)



F	B	20	
MELI	1326.94	NSDQ	062E4C22202D-402	10:03:29	BDincer Kore	Fill

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/149a7711-c6b0-4deb-b82d-c594b57cb2f9)



MELI	1	18	BuySide	8/9/2023 10:02	1,330.00	8/9/2023 10:02	1,332.79
MELI	1	18	BuySide	8/9/2023 10:03	1,326.79	8/9/2023 10:03	1,329.58
MELI	1	18	BuySide	8/9/2023 10:38	1,327.15	8/9/2023 10:38	1,329.94
MELI	1	1	BuySide	8/9/2023 10:46	1,328.63	8/9/2023 10:52	1,325.56
MELI	1	1	BuySide	8/9/2023 10:51	1,328.07	8/9/2023 10:52	1,325.56
MELI	1	18	BuySide	8/9/2023 10:52	1,323.30	8/9/2023 10:56	1,325.47

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/535e9efd-ce54-4cae-b79a-d2a4f5bb1c82)



USING A SYSTEM OF 10/ 20/ 30/ 40 SHARES 


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/e9706f68-2e67-46f6-b88f-3d3a80d2bea2)


10K/ 20K/ 30K Shares 

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/9d02f425-6a40-412c-af22-5db209fa0ffa)



LOB  10.85
ORIG. ON 10.75

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/2b54a0d5-40ad-4785-8475-7ed52016c0f0)



market data issues 8-9-2023

[market data issues 8-9-2023.pdf](https://github.com/bdincerTrader/Fauconberg1/files/12305458/market.data.issues.8-9-2023.pdf)
