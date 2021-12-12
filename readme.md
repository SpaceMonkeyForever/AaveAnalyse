### Goal

Estimate Aave Health Factor for the given address at different points in time.

### Contents
- Script to query the list of interactions the given address had with Aave v1.
  - This was done using Aave GraphQL API but could have been done by querying Ethereum blockchain directly using e.g. Etherscan
- Result Excel sheet: Contains the output of script plus price data and the calculated Health Factor at each point the address interacted with Aave. This can be automated (read TODO below)

### Notes:
- The Health Factor formula in the docs is based on prices in ETH but we use prices in USD because it's simpler and the
calculation doesn't change as long as the quote currency is consistent.
- In the sheet, the balance at the end is non-zero because of earned/owed interest. This also means that the Health Factor calculation
at each time given is not 100% accurate because the amount borrowed/deposited changed since the time of the precious transaction. This can be fixed by querying for all of the address's balances at each timestamp we're interested in.

### TODO:
Avoid using Excel by automating these steps:
- Query block number based on transaction hash using Etherscan API
- Query prices at certain times using e.g. CoinmarketCap API (paid subscription)
- Query Liquidation Threshold, which is used in calculating Health Factor, at the time for which we are calculating the health factor using Aave API.
- With that data, build address balance at any given point in time and calculate the Health Factor.
- Make the calculation more accurate by updating our knowledge of the address's balances at each timestamp because the amount deposited/borrowed changes based on the interest earned/owed.

### Resources used:

- Check given [account](https://etherscan.io/address/0x1b7835d2074914161dd6a2d48e393be1dbf296d1) on Etherscan:
  - Notice it is using **v1 of Aave** 
- Aave documentation on [Health Factor](https://docs.aave.com/risk/asset-risk/risk-parameters#health-factor)
- Create a [test account](https://kovan.etherscan.io/address/0x1eba8679615c7326767e41aea9d6c45aec030e92) on Kovan testnet and use it in [Aave staging](https://staging.aave.com/)
  - [0x1eba8679615c7326767e41aea9d6c45aec030e92](https://kovan.etherscan.io/address/0x1eba8679615c7326767e41aea9d6c45aec030e92) 
- Inspect different operations on Etherscan to understand how to identify them on the blockchain
- Read Aave API documentation and use the playground ([v1 prod](https://thegraph.com/hosted-service/subgraph/aave/protocol-multy-raw) and [kovan](https://thegraph.com/hosted-service/subgraph/aave/protocol-v2-kovan?selected=playground)) to construct the right query.


### Final output (taken from Excel sheet)

| Health Factor |	Block Num |
| ----------- | ----------- |
| Inf	| 10394277 |
| 1.48	| 10394295 |
| 2.38	| 10470088 |
| 1.62	| 10470095 |
| 2.10	| 10599809 |
| 7.41	| 10867350 |
| Inf	| 10868596 |
| Inf	| 10872624 |
| Inf	| 10872633 |
