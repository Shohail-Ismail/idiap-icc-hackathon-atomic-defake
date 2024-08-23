import json
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from mistralai import Mistral

from atomic_defake.aggregation import verify_post, VERTIFICATION_STRATEGIES
from atomic_defake.human_response_generation import manual_input_human_responses
from atomic_defake.llm_response_generation import generate_llm_responses
from atomic_defake.question_generation import question_generation

load_dotenv()


class AtomicDeFake:
    def __init__(self, aggregation_method):
        self.aggregation_method = aggregation_method
        if self.aggregation_method not in VERTIFICATION_STRATEGIES:
            raise ValueError(
                f"Invalid verification method: '{self.aggregation_method}', must be one of {VERTIFICATION_STRATEGIES}."
            )
        api_key = os.environ["MISTRAL_API_KEY"]
        self.model = "open-mistral-nemo"
        self.client = Mistral(api_key=api_key)

    def generate_run_id(self):
        return str(uuid.uuid4().hex)

    def generate_atomic_questions(self, post_text):
        questions, prompt_data = question_generation(post_text, self.client)
        return questions

    def generate_LLM_responses(self, post_text, questions):
        qa_pairs = generate_llm_responses(post_text, questions, self.client)
        return qa_pairs

    def generate_human_responses(self, post_text, questions):
        qa_pairs = manual_input_human_responses(post_text, questions)
        return qa_pairs

    def generate_responses(self, post_text, questions):
        """
        Generate answers to the atomic questions.
        """
        qa_pairs = self.generate_LLM_responses(post_text, questions)
        qa_pairs_human = self.generate_human_responses(post_text, questions)

        for qa_pair, qa_pair_h in zip(qa_pairs, qa_pairs_human):
            qa_pair["response_human"] = qa_pair_h["response_human"]

        return qa_pairs

    def store_run(self, run_id, post_text, qa_pairs, final_label):
        filename = Path(f"responses/{run_id}.json")
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        with open(filename, "w") as f:
            data = {
                "run_id": run_id,
                "prompt_data": {"post_text": post_text},
                "qa_pairs": qa_pairs,
                "final_label": final_label,
            }
            json.dump(data, f)

    def aggregate_responses(self, run_id, qa_pairs):
        return verify_post(run_id, qa_pairs, method=self.aggregation_method)

    def verify(self, post_text):
        run_id = self.generate_run_id()

        questions = self.generate_atomic_questions(post_text)

        responses = self.generate_responses(post_text, questions)

        final_label = self.aggregate_responses(run_id, responses)

        self.store_run(run_id, post_text, responses, final_label)
        return final_label
