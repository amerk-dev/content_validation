from openai import OpenAI
from config import api_key
client = OpenAI(api_key=api_key)

async def validate_text(text_to_validate: str) -> bool:
    response = client.moderations.create(input=text_to_validate)
    results = response.results
    print(results)
    flagged = results[0].get('flagged', False)
    return not flagged