import argparse
import json
from pathlib import Path

RESPONSE_DIR = Path("responses")

def read_question_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    post = data['prompt_data']['post_text']
    questions = data['questions']
    run_id = data['run_id']
    return run_id, post, questions, data


def manual_input_human_responses(post, questions):
    qa_pairs = []
    for q in questions:
        print(f"Post: {post}")
        print(f"Question: {q}")
        response = input("Response [y/n/?]: ")
        while response not in ['y', 'n', '?']:
            print("Invalid response. Please enter 'y', 'n', or '?'")
            response = input("Response [y/n/?]: ")
        qa_pairs.append({"question": q, "response": response})
        print()
    return qa_pairs

def store_qa_pairs(run_id, qa_pairs, data):
    filename = Path(RESPONSE_DIR) / f"{run_id}.json"
    data['qa_pairs'] = qa_pairs
    with open(filename, "w") as f:
        json.dump(data, f)


def main():
    parser = argparse.ArgumentParser(description="A basic argparse example.")
    parser.add_argument('file', type=str, help='The path to a file containing the atomic questions', default=None)
    args = parser.parse_args()

    run_id, post, questions, data = read_question_file(Path(args.file))
    qa_pairs = manual_input_human_responses(post, questions)
    store_qa_pairs(run_id, qa_pairs, data)






if __name__ == "__main__":
    main()
