@slyoung69


If the symbols in the scope are in "bear" territory, the program doesn't allocate.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/a5a77712-6ce8-4830-8923-c941de511672)



I thought there was a data issue yesterday.
- I dropped a line of Code in there to automatically buy 1 Share of every ticker in the universe of the System; turned it off after.
- If the symbols in the scope are in "bear" territory, the program doesn't allocate. ****

GTG. 100%

##### LINE 160
*** MAINTAINS A FRESH ORDER BOOK
cancels the pending book it it approaches 30 orders.


##### LINE 224
*** WILL  CLOSE THE POSITION AND DE-LIST THE SYMBOL IF IT TURNS INTO A ( - ) or [ - ]
IF self.safetySymbol=750.. There's no coming back (it is unsubscribed for the remainder of the session).


##### LINE 267

*** MAKES SURE self.limitBP>0 and len(account[self.symbol].pending.orders)<30

    self.limitBP =   self.order_quantity_max  -   account[self.symbol].position.capital_long  -  account[self.symbol].pending.capital_long;

    self.order_quantity_max = % of account BP (parameter accountBP/maxSymbolTrade);

*** I can adjust this later to dynamically adjust, in case the [ + ] grows at a certain rate.


##### LINE 290
*** Runs the same risk check as # LINE 267 before submitting any orders.

-------------

EXAMPLE, LIMIT BP.

HASH: 4424ad0c39f5fa5c0be97862df577cc1
    limitBP= $3,000,000
    accountBP=$15,000,000
    maxSymbolTrade=5

/s/ BD.



--

***** 

## LONG ONLY SYSTEM.


If the symbols in the scope are in "bear" territory, the program doesn't allocate.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/a5a77712-6ce8-4830-8923-c941de511672)



****** NO ORDERS 8/16 OR 8/17 (AS OF CURRENT)

I thought there was a data issue yesterday in FWD Testing.

... I dropped a line of Code in there to automatically buy 1 Share of any Symbol that entered the on_start() Fn.
... Turned the system off after and closed all positions manually.

   
### QQQ

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/f95f7686-877d-4395-8a1f-f3d6763f92bd)


### SPY
![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/6196a24c-c272-4d31-8ae5-bee5e804c06c)



*** No  further updates required at this time.
    
    0 Rejects/ Errors.
    0 EOD Positions.
    108 Symbols Evaluated.
    15 Symbols Traded.
    0 Human Intervention.

#### $27,456 MTM P/L
--

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/df262f57-ee8e-4113-91f4-b5c65346d3b6)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/04c39251-50c9-4500-8c79-2d839903393c)






### SETS
    
tickerItrA=['FNGU','TMO','ELV','DDS','GS','TSLA','NFLX','INSP','PANW','PLPC','FIVE','FICO','ZBRA','ASML','SMCI','TMV','URI','FNGU','SPOT','MSCI','EQIX','MSTR','MELI','PH','ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','MPWR','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];
    
tickerItrB = ['GS','MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','URI','FSLR','SWAV','GUSH','REGN','PANW','FIVE','FICO','ZBRA','ASML','SMCI','TMV','LRCX','ACLS','FCNCA','CMG','GS','MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','URI','FSLR','SWAV','GUSH','REGN','PANW','FIVE','FICO','ZBRA','ASML','SMCI','TMV','LRCX','ACLS','FCNCA','CMG'];
    
tickerItrC = ['ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','BRK.A','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA','DDOG','DE','DECK','DHR','DPST','DPZ','ELF','ELV','ENPH','EPAM','EQIX','ESS','FCNCA','FDS','FICO','FNGU','FSLR','GNRC','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','ITW','KLAC','LII','LIN','LLY','LMT','LPLA','LRCX','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MLM','MOH','MPWR','MSCI','MSFT','MSI','MSTR','MTD','NFLX','NOC','NOW','NVDA','NVR','NXPI','ODFL','OIH','ORLY','PANW','PAYC','PEN','PH','PODD','POOL','PSA','PXD','REGN','RETA','RGEN','RH','RMD','ROK','ROKU','ROP','SAIA','SBAC','SEDG','SHW','SIMO','SMCI','SN','SNOW','SNPS','SOXX','SPGI','SPOT','STE','SYK','TDG','TDY','TEAM','TMO','TSCO','TSLA','ULTA','UNH','UPST','URI','VGT','VRTX','W','WAT','WCC','WDAY','WSO','WST','ZBRA','ZS'];

tickerItrD = ['SAM','VMI','TYL','MUSA','BLD','BIO','RS','COO','NICE','EG','HII','KRTX','LAD','TFX','WIRE','JLL','CYBR','MEDP','GLOB','FCN','UTHR','SWAV','MKTX','MSGS','CRL','PCTY','RNR','ARCB','DUOL'];

tickerItrE=['ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','BRK.A','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];

tickerItrF=['DDOG','DE','DECK','DHR','DPST','DPZ','ELF','ELV','ENPH','EPAM','EQIX','ESS','FCNCA','FDS','FICO','FNGU','FSLR','GNRC','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','ITW','KLAC','LII','LIN','LLY','LMT','LPLA','LRCX'];

tickerItrG=['MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','GS','MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','URI','FSLR','SWAV','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MLM','MOH','MPWR','MSCI','MSFT','MSI','MSTR','MTD','NFLX','NOC','NOW','NVDA','NVR','NXPI','ODFL','OIH','ORLY','PANW','PAYC','PEN','PH','PODD','POOL','PSA','PXD','REGN','RETA','RGEN','RH','RMD','ROK','ROKU'];
    
tickerItrH=['ROP','SAIA','SBAC','SEDG','SHW','SIMO','SMCI','SN','SNOW','SNPS','SOXX','SPGI','SPOT','STE','SYK','TDG','TDY','TEAM','TMO','TSCO','TSLA','ULTA','UNH','UPST','URI','VGT','VRTX','W','WAT','WCC','WDAY','WSO','WST','ZBRA','ZS'];
     
### BACKTEST SUMMARY

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/25b76d2a-e805-4c4f-af45-a39132ece9cf)





![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/23a35d4a-66b8-4427-a1aa-4468eb8b4082)



Order Status -- 	qabdincer


F	S	225	GS	332.71	NSDQ			106791QZON2	062E6D694C23-402	13:08:25	BD_Fauconberg	Fill
F	B	18	GS	332.51	NSDQ			106763QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106762QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106760QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106747QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106745QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106742QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106740QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106738QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106736QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106734QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106732QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106730QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106718QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106715QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106713QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106711QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106709QZON2	062E696D694D-402	13:06:41	BD_Fauconberg	Fill
F	B	17	GS	332.83	GSALGO			106764GZON2	062E64724F75-402	13:06:34	BD_Fauconberg	Fill
F	B	5	GS	332.84	GSALGO			106761GZON2	062E64724F75-402	13:06:20	BD_Fauconberg	Fill
F	B	5	GS	332.84	GSALGO			106759GZON2	062E64724F75-402	13:06:13	BD_Fauconberg	Fill
F	B	5	GS	332.84	GSALGO			106746GZON2	062E64724F75-402	13:06:06	BD_Fauconberg	Fill
F	B	5	GS	332.76	GSALGO			106744GZON2	062E64724F75-402	13:05:59	BD_Fauconberg	Fill
F	B	5	GS	332.76	GSALGO			106741GZON2	062E64724F75-402	13:05:52	BD_Fauconberg	Fill
F	B	5	GS	332.76	GSALGO			106739GZON2	062E64724F75-402	13:05:45	BD_Fauconberg	Fill
F	B	5	GS	332.76	GSALGO			106737GZON2	062E64724F75-402	13:05:38	BD_Fauconberg	Fill
F	B	5	GS	332.70	GSALGO			106735GZON2	062E64724F75-402	13:05:31	BD_Fauconberg	Fill
F	B	5	GS	332.63	GSALGO			106733GZON2	062E64724F75-402	13:05:24	BD_Fauconberg	Fill
F	B	5	GS	332.63	GSALGO			106731GZON2	062E64724F75-402	13:05:17	BD_Fauconberg	Fill
F	B	5	GS	332.66	GSALGO			106729GZON2	062E64724F75-402	13:05:10	BD_Fauconberg	Fill
F	B	5	GS	332.70	GSALGO			106717GZON2	062E64724F75-402	13:05:03	BD_Fauconberg	Fill
F	B	5	GS	332.66	GSALGO			106714GZON2	062E64724F75-402	13:04:56	BD_Fauconberg	Fill
F	B	5	GS	332.70	GSALGO			106712GZON2	062E64724F75-402	13:04:49	BD_Fauconberg	Fill
F	B	5	GS	332.64	GSALGO			106710GZON2	062E64724F75-402	13:04:42	BD_Fauconberg	Fill
F	B	5	GS	332.64	GSALGO			106708GZON2	062E64724F75-402	13:04:35	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106707QZON2	062E696D694D-402	13:04:29	BD_Fauconberg	Fill
F	B	5	GS	332.67	GSALGO			106706GZON2	062E64724F75-402	13:04:28	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106705QZON2	062E696D694D-402	13:04:25	BD_Fauconberg	Fill
F	B	5	GS	332.51	NSDQ			106703QZON2	062E31303D31-402	13:04:25	BD_Fauconberg	Fill
F	B	5	GS	332.67	GSALGO			106704GZON2	062E64724F75-402	13:04:21	BD_Fauconberg	Fill
F	B	5	GS	332.68	GSALGO			106702GZON2	062E6D694C23-402	13:04:14	BD_Fauconberg	Fill
