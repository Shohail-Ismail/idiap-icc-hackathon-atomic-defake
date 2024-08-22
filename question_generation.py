import os
import json
from dotenv import load_dotenv
from mistralai import Mistral

# load API key from .env file
load_dotenv()

def question_generation(post_text, client):
    pass

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": f"Generate questions to verify whether the following post is NOT misleading: {post_text}. Return the questions in a short JSON object. Please include at least 5 questions.",
            },
        ],
        response_format = {
            "type": "json_object",
        }
    )

    return chat_response

if __name__ == "__main__":
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "open-mistral-nemo"
    client = Mistral(api_key=api_key)

    post_text = "Our popular coffee shop, Brew Haven, is now offering free Wi-Fi and extended hours until 10 PM daily! :coffee::computer:"

    response = question_generation(post_text, client)

    try:
        question_obj = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        exit(1)

    if len(question_obj['questions']) < 5:
        print("Error: Less than 5 questions generated.")
        exit(1)


    print(question_obj)
    for question in question_obj['questions']:

        print(question)

