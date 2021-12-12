import math

import requests
import json
from datetime import datetime

# TODO: move to a config file
url = 'https://api.thegraph.com/subgraphs/name/aave/protocol-multy-raw'


# json parsing
class Tx:
    def __init__(self, tx_json):
        self.tx_type = tx_json['__typename'].lower()
        self.amount = float(tx_json['amount']) / math.pow(10, int(tx_json['reserve']['decimals']))
        self.symbol = tx_json['reserve']['symbol']
        self.tx_hash = tx_json['id']
        unixtime = int(tx_json['timestamp'])
        self.time = datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
        # TODO: Ideally, we should query liquidation threshold at the time for which we want to calc Health Factor
        self.liquidation_threshold = int(tx_json['reserve']['reserveLiquidationThreshold'])


def get_user_transactions(user):
    # docs:
    query = """query txHistory {
      userTransactions(where: {user: "%s"}, orderBy: timestamp ) {
        id
        timestamp
        __typename
        ... on Borrow {
          amount
          reserve {symbol, , decimals, reserveLiquidationThreshold}
        }
          ... on  Repay {
          amount: amountAfterFee // this has been changed in the new V2 API to be consistent
          reserve {symbol, , decimals, reserveLiquidationThreshold}
        }
        ... on Deposit {
          amount
          reserve {symbol, decimals, reserveLiquidationThreshold}
        }
        ... on  RedeemUnderlying{
          amount
          reserve {symbol, decimals, reserveLiquidationThreshold}
        }
      }
    }""" % user

    # Execute the query on the transport
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)
    return json_data['data']['userTransactions']


def query_address(address):
    txs = get_user_transactions(address)
    for tx in [Tx(x) for x in txs if (x['__typename']).lower() in ('borrow', 'deposit', 'repay', 'redeemunderlying')]:
        # TODO: get price from e.g. Coinmarketcap https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesHistorical
        # then calculate sum(price * deposited * liquidation_threshold per borrowed token) / total_borrowed_value at each step
        # as explained in https://docs.aave.com/risk/asset-risk/risk-parameters#health-factor
        # we can use price in USD instead of in ETH. It makes no difference as long as we price all assets in the same quote currency
        # TODO: Query for the current balance because it might have changed due to interest
        # TODO: Query for current liquidation threshold for all other assets
        print(", ".join([tx.time, tx.tx_hash, tx.tx_type, tx.symbol, str(tx.amount), str(tx.liquidation_threshold)]))


if __name__ == '__main__':
    query_address("0x1b7835d2074914161dd6a2d48e393be1dbf296d1")
