import os
import json
import uuid
from dotenv import load_dotenv
from mistralai import Mistral
from pathlib import Path

QUESTION_DIR="questions"

# load API key from .env file
load_dotenv()


def question_generation(post_text, client):
    run_id = str(uuid.uuid4().hex)
    prompt = f"Generate questions to verify whether the following post is NOT misleading: {post_text}. Return the questions in a short JSON object. Please include at least 5 questions."
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format = {
            "type": "json_object",
        }
    )

    try:
        questions = json.loads(chat_response.choices[0].message.content)
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        exit(1)

    if "questions" not in questions:
        print("Error: 'questions' not found in response.")

    return run_id, questions['questions'], {"prompt": prompt, "post_text": post_text}


def store_post_and_questions(run_id, post_text, questions, prompt_data):
    filename = Path(QUESTION_DIR) / f"{run_id}.json"
    with open(filename, "w") as f:
        json.dump({
            "run_id": run_id,
            "post": post_text,
            "questions": questions,
            "prompt_data": prompt_data
        }, f)

if __name__ == "__main__":
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "open-mistral-nemo"
    client = Mistral(api_key=api_key)

    post_text = "Our popular coffee shop, Brew Haven, is now offering free Wi-Fi and extended hours until 10 PM daily! :coffee::computer:"

    run_id, questions, prompt_data = question_generation(post_text, client)

    if len(questions) < 5:
        print("Error: Less than 5 questions generated.")
        exit(1)


    for question in questions:
        print(question)

    store_post_and_questions(run_id, post_text, questions, prompt_data)


