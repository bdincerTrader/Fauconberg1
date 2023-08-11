
  ### LOOKS GOOD.

  ![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/5caac297-6d3a-4b04-86c4-246ec4a4e0c6)

Both accounts running the same system -looks good in both.

[server Config Issue.pdf](https://github.com/bdincerTrader/Fauconberg1/files/12322654/server.Config.Issue.pdf)

* looks like they are syncronized now.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/e42641be-cc1f-4ecc-ba02-691c73118cad)


##  RUNNING BLOCK E: 2023-08-11

maxBP 5
Symbol Universe A.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/8110faf5-de2e-444a-ae34-bebe29fcb8f2)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/c4e40d74-f9e2-4868-a32a-50d7a2e80d95)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/d42d7d10-31d5-40c2-add7-7888843c1c9d)


MSTR IS IN THE SAME UNIVERSE AS what bdincer kore is running.

please explain

tickerItrA=['TMO','ELV','DDS','GS','TSLA','NFLX','INSP','PANW','PLPC','FIVE','FICO','ZBRA','ASML','SMCI','TMV','URI','FNGU','SPOT','MSCI','EQIX','MSTR','MELI','PH','ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','MPWR','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];

no orders placed in BD_Fauconberg. was running the same ALGO as BDincer Kore. 
![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/fc4be6e0-e471-4895-908c-a0b864ce2417)


    
![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/62096385-b810-4e43-b829-1cc1dd9db5c6)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/7dc6fdec-fd8b-4280-b897-6ce9be698f48)

[SystemA-SystemB.xlsx](https://github.com/bdincerTrader/Fauconberg1/files/12323446/SystemA-SystemB.xlsx)

----     ----     ----      ----     ----     ----     ----      ----     ----

I just restarted the model in both accounts and now I am seeing this the other way around, meaning the orders and being propagated from SystemA (opposite to the issue I had earlier this AM).

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/3572c14f-432a-400b-9f8c-697881305a8b)




This AM I launched fauconberg from two different FWD Testing Accounts.

SystemA: Faunconberg was running in FWD Account: BD_Fauconberg (10.10.10.75)
SystemB: FauconbergBandsLOB was running in FWD Account: BDincer Kore (10.10.10.77)

The two systems above are identical, with respect to their timers and the CODE.

FauconbergBandsLOB was operating on a much larger universe of symbols on server 10.10.10.77.

** Symbol Universe: Price>50.00 ATR>5 and VOLUME>555555

- I turned the two systems on maybe a minute apart.

SystemB allocated to symbols MSTR and AON which are both in the universe of symbols covered by SystemA.
***  Curious if the server (10.10.10.75) had an issue today, or does not cover the md in the tickers that are coded to spec in SustemA. Both SystemA and SystemB should have equally performed, allocated, etc..


** SystemB was operating on a fixed set of symbols on server 10.10.10.75.

** Symbol Universe: ['TMO','ELV','DDS','GS','TSLA','NFLX','INSP','PANW','PLPC','FIVE','FICO','ZBRA','ASML','SMCI','TMV','URI','FNGU','SPOT','MSCI','EQIX','MSTR','MELI','PH','ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','MPWR','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];
   

Thanks for looking into this!

/s/ BD.
  
