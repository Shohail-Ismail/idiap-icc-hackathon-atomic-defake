import json

VERTIFICATION_STRATEGIES = ["single_false_or_unsure"]


def read_qa_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    run_id = data["run_id"]
    qa_pairs = data["qa_pairs"]
    return run_id, qa_pairs


def verify_single_false_or_unsure(qa_pairs_human, qa_pairs_llm):
    verified_by_adf = True
    llm_false = 0
    for qa_pair in qa_pairs_llm:
        response = qa_pair["response_llm"]["response"]
        if response == "Some misinformation" or response == "Mostly misinformation":
            llm_false += 1

    if llm_false > 2:
        verified_by_adf = False

    for _, user_qa_pairs in qa_pairs_human.items():
        if (
            user_qa_pairs["overall_label"] == "I don't know"
            or user_qa_pairs["overall_label"] == "Not trustworthy"
            or user_qa_pairs["overall_certainty"] == "uncertain"
            or user_qa_pairs["overall_certainty"] == "very uncertain"
        ):
            verified_by_adf = False
            break
    return verified_by_adf


def verify_post(qa_pairs_human, qa_pairs_llm, method="single_false_or_unsure"):
    if method == "single_false_or_unsure":
        return verify_single_false_or_unsure(qa_pairs_human, qa_pairs_llm)
    else:
        raise ValueError(
            f"Invalid verification method: '{method}', must be one of {VERTIFICATION_STRATEGIES}."
        )
