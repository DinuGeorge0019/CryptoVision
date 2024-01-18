from openai import OpenAI

def request_gpt_crypto_analysis(crypto_data, _SEED=42):
    context_promt = """You possess expertise in crypto market, and you are required to help with an advice."""

    request_prompt = f"""
    Analyze this crypto data and tell me when should I invest in crypto. 
    Crypto data: 
    when_to_buy_date:{crypto_data['when_to_buy_date']}, 
    minimum_price:{crypto_data['minimum_price']}, 
    when_to_sell:{crypto_data['when_to_sell']}, 
    maximum_price:{crypto_data['maximum_price']},
    possible_profit:{crypto_data['possible_profit']},
    possible_loss:{crypto_data['possible_loss']},. 
    Answer a sentence of maximum 200 characters.
    """

    client = OpenAI(
      api_key='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'
    )
    
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      messages=[
        {"role": "system", "content": context_promt},
        {"role": "user", "content": request_prompt}
      ],
      temperature=0.7,
      seed=_SEED,
      n=1,
      max_tokens=200
    )

    # Assuming `response` is your ChatCompletion object
    choice = response.choices[0]
    message_content = choice.message.content    

    return message_content