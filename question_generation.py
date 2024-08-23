import os
import json
from pathlib import Path
import time
from dotenv import load_dotenv
from mistralai import Mistral

# Load API key
load_dotenv()

def question_generation(post_text, client):
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

def generate_answer(question, client):
    response_answer = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": f"Please provide a detailed answer to the following question: {question}.",
            },
        ],
    )
    return response_answer

def evaluate_for_misinformation(answer, client):
    evaluation_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": f"Given the following answer, evaluate it for misinformation. Specifically, assess the answer itself for sanity and consistency, give a misinformation certainty, and give the reason for that misinformation certaintly level, and use only heading of 'misinformation' (with possible labels of 'None', 'Little', 'Some', 'Most' and 'All'), 'certainty, 'reason' for all the answers, using no other headings pr subheadings: {answer}. Return the evaluation in a JSON format.",
            },
        ],
        response_format = {
            "type": "json_object",
        }
    )
    return evaluation_response

def process_questions(question_obj, client):
    evaluations = [] 
    for question in question_obj['questions']:
        ##print(f"\nProcessing question: {question}")

        # Generate answer for quetion
        answer_response = generate_answer(question, client)
        answer = answer_response.choices[0].message.content
        ##print(f"Answer: {answer}")

        # Evaluate answer for misinformation
        evaluation_response = evaluate_for_misinformation(answer, client)
        try:
            evaluation = json.loads(evaluation_response.choices[0].message.content)
            evaluations.append(evaluation)
            ##print(f"\nEvaluation: {evaluation}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON response for evaluation of answer: {answer}")
        
        time.sleep(1)

    return evaluations  

# Not necessary for func.
def pretty_print(question_obj, evaluations):
    print(json.dumps({"questions": question_obj['questions']}, indent=4))
    for evaluation in evaluations:
        print(json.dumps(evaluation, indent=4))


def save_questions_to_file(question_obj, post_text, run_id="default_run_id"):
    responses_dir = Path("responses")
    responses_dir.mkdir(exist_ok=True)
    
    data = {
        "run_id": run_id,
        "prompt_data": {"post_text": post_text},
        "questions": question_obj['questions']
    }
    with open(f"responses/{run_id}.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "open-mistral-nemo"
    client = Mistral(api_key=api_key)

    post_text = "Our popular coffee shop, Brew Haven, is now offering free Wi-Fi and extended hours until 10 PM daily! :coffee::computer:"
    run_id = "run_1"  # example id

    response = question_generation(post_text, client)

    try:
        question_obj = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        exit(1)

    if len(question_obj['questions']) < 5:
        print("Error: Less than 5 questions generated.")
        exit(1)

    save_questions_to_file(question_obj, post_text, run_id)
    evaluations = process_questions(question_obj, client)
    pretty_print(question_obj, evaluations)
