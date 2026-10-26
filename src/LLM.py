from openai import OpenAI
import os

def assistant(prompt):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
    )
    print(response.output_text)
    return response.output_text