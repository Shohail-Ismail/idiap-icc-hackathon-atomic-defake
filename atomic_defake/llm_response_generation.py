import json
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
RESPONSE_DIR = Path("responses")
MODEL_NAME = "open-mistral-nemo"
TEMPERATURE = 0.0


def read_question_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    post = data["prompt_data"]["post_text"]
    questions = data["questions"]
    run_id = data["run_id"]
    return run_id, post, questions, data


def ask_certainty():
    certainty = input("How certain are you about it? [h/m/l]: ")
    while certainty not in ["h", "m", "l"]:
        print("Invalid response. Please enter 'h', 'm', or 'l'")
        certainty = input("How certain are you about it? [h/m/l]: ")
    return certainty


def generate_answer(question, post, client):
    response_answer = client.chat.complete(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "user",
                "content": f"Given the following post and question, please provide a detailed answer to the question: \n Post: {post} \n Question: {question}",
            },
        ],
    )
    return response_answer.choices[0].message.content


def evaluate_for_misinformation(post, question, client):
    evaluation_response = client.chat.complete(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "user",
                "content": f"Given the following post and a critical question about it, evaluate the post for any misinformation. Be critical of user-generated sources like Twitter. Also give a misinformation certainty, and give the reason for that misinformation certaintly level. Use only fields of 'misinformation' (with possible labels of 'No misinformation', 'Some misinformation', 'Mostly misinformation'), 'certainty, 'reason' for all the answers, using no other fields or headings. Post: {post}\n Question: {question}\n Return the evaluation in a JSON format.",
            },
        ],
        response_format={
            "type": "json_object",
        },
    )

    try:
        evaluation = json.loads(evaluation_response.choices[0].message.content)
    except json.JSONDecodeError:
        print(f"Error decoding JSON response for evaluation of answer: {answer}")

    return evaluation


def generate_llm_responses(post, questions, client):
    qa_pairs = []
    for q in questions:
        # answer_response = generate_answer(q, post, client)
        # time.sleep(2)
        evaluation_response = evaluate_for_misinformation(post, q, client)
        qa_pairs.append(
            {
                "question": q,
                # "answer": answer_response,
                "response_llm": {
                    "response": evaluation_response["misinformation"],
                    "certainty": evaluation_response["certainty"],
                    "reason": evaluation_response["reason"],
                },
            }
        )
        time.sleep(2)
    return qa_pairs
