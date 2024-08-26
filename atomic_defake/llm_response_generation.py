import argparse
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()
RESPONSE_DIR = Path("responses")


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


def generate_answer(question, client):
    response_answer = client.chat.complete(
        model="open-mistral-nemo",
        messages=[
            {
                "role": "user",
                "content": f"Please provide a detailed answer to the following question: {question}.",
            },
        ],
    )
    return response_answer.choices[0].message.content


def evaluate_for_misinformation(answer, client):
    evaluation_response = client.chat.complete(
        model="open-mistral-nemo",
        messages=[
            {
                "role": "user",
                "content": f"Given the following answer, evaluate it for misinformation. Specifically, assess the answer itself for sanity and consistency, give a misinformation certainty, and give the reason for that misinformation certaintly level, and use only heading of 'misinformation' (with possible labels of 'None', 'Little', 'Some', 'Most' and 'All'), 'certainty, 'reason' for all the answers, using no other headings pr subheadings: {answer}. Return the evaluation in a JSON format.",
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
        print(f"Post: {post}")
        print(f"Question: {q}")
        answer_response = generate_answer(q, client)
        evaluation_response = evaluate_for_misinformation(answer_response, client)
        qa_pairs.append(
            {
                "question": q,
                "response_llm": {
                    "response": evaluation_response["misinformation"],
                    "certainty": evaluation_response["certainty"],
                    "reason": evaluation_response["reason"],
                },
            }
        )
        print()
        time.sleep(2)
    return qa_pairs


def store_qa_pairs(run_id, qa_pairs, data):
    filename = Path(RESPONSE_DIR) / f"{run_id}.json"
    data["qa_pairs"] = qa_pairs
    with open(filename, "w") as f:
        json.dump(data, f)


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    parser = argparse.ArgumentParser(description="A basic argparse example.")
    parser.add_argument(
        "file",
        type=str,
        help="The path to a file containing the atomic questions",
        default=None,
    )
    args = parser.parse_args()

    run_id, post, questions, data = read_question_file(Path(args.file))
    qa_pairs = generate_llm_responses(post, questions, client)
    store_qa_pairs(run_id, qa_pairs, data)


if __name__ == "__main__":
    main()
