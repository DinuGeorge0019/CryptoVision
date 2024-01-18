
from bitquery import bitquery
from datetime import datetime, timedelta

_API_KEY = "BQYg5FZJ1koaDcTRKtYpmoh3gNfnQZ2z"


def get_bitcoin_transaction_count_from_this_week():
    # Calculate the dates
    now = datetime.now()
    one_week_ago = now - timedelta(weeks=1)

    # Format the dates
    now_str = now.isoformat()
    one_week_ago_str = one_week_ago.isoformat()
    
    query = f"""
    query{{
      bitcoin(network: bitcoin) {{
        transactions(
          options: {{asc: "date.date"}}
          date: {{till: "{now_str}", since: "{one_week_ago_str}"}}
        ) {{
          date {{
            date(format: "%Y-%m-%d %H:%M:%S")
          }}
          countBigInt
        }}
      }}
    }}
    """
    
    transactions = bitquery.run_query(_API_KEY, query)

    return transactions
  
  
def get_bitcoin_latest_transactions():
    # Get the current time
    now = datetime.now()

    # Subtract one hour
    one_hour_ago = now - timedelta(hours=4)

    # Convert to ISO 8601 format
    one_hour_ago_iso = one_hour_ago.isoformat()
    
    query = f"""
    query {{
        bitcoin(network: bitcoin) {{
          transactions(
            options: {{desc: ["inputValue"], limit: 10, offset: 0}}
            time: {{after: "{one_hour_ago_iso}"}}
          ) {{
            block {{
              timestamp {{
                time(format: "%Y-%m-%d %H:%M:%S")
              }}
            }}
            feeValue(in: USD)
            inputValue(in: USD)
            inputValueInBTC: inputValue(in: BTC)
            inputCount
            outputCount
            hash
          }}
        }}
    }}
    """
    
    transactions = bitquery.run_query(_API_KEY, query)

    return transactions

def get_bitcoin_active_miners_and_value_from_this_week():
    # Calculate the dates
    now = datetime.now()
    one_week_ago = now - timedelta(weeks=1)

    # Format the dates
    now_str = now.isoformat()
    one_week_ago_str = one_week_ago.isoformat()
    
    query = f"""
    query{{
      bitcoin(network: bitcoin) {{
        outputs(
          options: {{asc: "date.date"}}
          date: {{since: "{one_week_ago_str}", till: "{now_str}"}}
          txIndex: {{is: 0}}
          outputDirection: {{is: mining}}
          outputScriptType: {{notIn: ["nulldata", "nonstandard"]}}
        ) {{
          date: date {{
            date(format: "%Y-%m-%d %H:%M:%S")
          }}
          count: countBigInt(uniq: addresses)
          value
        }}
      }}
    }}
    """
    
    result = bitquery.run_query(_API_KEY, query)

    return result

def get_bitcoin_mined_blocks_and_value_this_week():
    # Calculate the dates
    now = datetime.now()
    one_week_ago = now - timedelta(weeks=1)

    # Format the dates
    now_str = now.isoformat()
    one_week_ago_str = one_week_ago.isoformat()
    
    query = f"""
    query{{
      bitcoin(network: bitcoin) {{
        transactions(options: {{asc: "date.date"}}, date: {{since: "{one_week_ago_str}", till: "{now_str}"}}) {{
          date: date {{
            date(format: "%Y-%m-%d %H:%M:%S")
          }}
          count: countBigInt(uniq: blocks)
          minedValue
        }}
      }}
    }}
    """
    
    result = bitquery.run_query(_API_KEY, query)

    return result
