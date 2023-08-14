
2023-08-14

#### MAX CAPITAL SET TO 5% ACCOUNT CAPITAL FOR EACH SYMBOL.



![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/347de91c-fb86-4242-81b7-8ddb17f0ce99)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/e918d9ce-69e6-498c-958d-1f7a97a7e5cc)


** PENDING ORDER MAX ERROR ADJUSTED.


#### RESTART SYSTEM.

#### I PUT THESE GATES UP TO AVOID THE FAILED PENDING ORDER CHECK ERROR

account[self.symbol].pending.count_long<37

LINE 275:  IF	account[self.symbol].pending.count_long<38
	     RETURN
		CANCEL BIDS/ REDUCE RISK

LINE 326:  IF    account[self.symbol].pending.count_long>38 
	     RETURN
		CANCEL BIDS/ REDUCE RISK







The only errors/rejects I saw in BD_Fauconberg were the Max Capital errors 
    
- Max cap for an order in QA account is 100K. 
- I am running the algo on 252 symbols simultaneously in FWD testing.

** I use the Unit Allocation parameter/ single symbols (limits ttl exposure).

** If it's ok with you, I want to double check on something tonight/ Tomorrow in back/FWD testing.
** Maybe blacklist a few additional symbols.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/620a3d72-7d3e-4fce-b021-e830cfdaac84)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/32a3038d-6f9b-4808-b6f5-f5b5678de32e)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/246cf8c1-00cc-4d36-aea2-66b9d65faa2a)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/b4526fb4-12bf-4322-8f42-70323863c030)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/b5fe5629-7998-49de-b3eb-c9d252519a75)





