import json
import os
import uuid
import time
import random
from pathlib import Path

from dotenv import load_dotenv
from mistralai import Mistral

from atomic_defake.aggregation import verify_post, VERTIFICATION_STRATEGIES
from atomic_defake.llm_response_generation import generate_llm_responses
from atomic_defake.question_generation import question_generation

load_dotenv()


STATUSES = ["wait", "human_responses", "completed", "start", "aggregation"]


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
        self.reset()
        self.llm_responses = None
        self.generated_questions = None

    def reset(self):
        self.status = "start"
        self.verified = False
        self.post_text = None

        # LLM generated questions
        self.generated_questions = None

        # LLM responses
        self.llm_responses = None

        # Human responses
        self.qa_pairs_h = {}

    def get_status(self):
        return self.status

    def format_feedback(self):
        feedback_report = ""
        for _, user in self.qa_pairs_h.items():
            for idx in range(0, len(user["qa_pair"])):
                feedback_report += "Question {:d}: ".format(idx + 1)
                feedback_report += user["qa_pair"][idx]["question"]
                feedback_report += "\nResponse: "
                feedback_report += user["qa_pair"][idx]["response_human"]
                feedback_report += "\n"

            feedback_report += "Overal assessment: "
            feedback_report += user["overall_label"]
            feedback_report += "\nConfidence: "
            feedback_report += user["overall_certainty"]
            feedback_report += "\n"

        if self.llm_responses is not None:
            feedback_report += "=== LLM Responses ===\n"
            for qa_pair in self.llm_responses:
                feedback_report += "Question: "
                feedback_report += qa_pair["question"]
                feedback_report += "\nSupport amount: "
                feedback_report += qa_pair["response_llm"]["response"]
                feedback_report += "\n"

        return feedback_report

    def get_output(self):
        post_text_verified = None

        if self.post_text is None:
            post_text_verified = -1
            user_response = "No post to verify"
        else:
            if self.verified:
                post_text_verified = 1
                user_response = self.post_text + " (✅ Verified by ADF)"
            else:
                post_text_verified = 0
                user_response = self.format_feedback()

        return post_text_verified, user_response

    def set_status(self, status):
        """ """
        assert status in STATUSES
        self.status = status

    def generate_run_id(self):
        return str(uuid.uuid4().hex)

    def generate_atomic_questions(self, post_text):
        questions = question_generation(post_text, self.client)
        return questions

    def generate_LLM_responses(self, post_text, questions):
        qa_pairs = generate_llm_responses(post_text, questions, self.client)
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

    def aggregate_responses(self, qa_pairs_human, qa_pairs_llm):
        return verify_post(qa_pairs_human, qa_pairs_llm, method=self.aggregation_method)

    def verify_fake(self, post_text, threshold=0.5):
        self.set_status("wait")
        self.post_text = post_text

        likelihood = random.random()
        if likelihood > threshold:
            self.verified = True
        else:
            self.verified = False
        time.sleep(2)

        self.set_status("completed")

    def verify_ai(self, post_text):
        self.set_status("wait")
        self.post_text = post_text
        self.set_status("human_responses")

    def set_human_responses(self, uuid, user_qas):
        if uuid not in self.qa_pairs_h:
            self.qa_pairs_h[uuid] = user_qas

    def detect_mislead_info(self):
        self.set_status("aggregation")
        self.llm_responses = self.generate_LLM_responses(
            self.post_text, self.generated_questions
        )
        final_label = self.aggregate_responses(self.qa_pairs_h, self.llm_responses)
        print(self.qa_pairs_h)
        print(self.llm_responses)
        self.verified = final_label
        time.sleep(3)
        self.set_status("completed")
