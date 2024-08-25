import json
import os
import uuid
import time
import random
from pathlib import Path

from dotenv import load_dotenv
from mistralai import Mistral

from atomic_defake.aggregation import verify_post, VERTIFICATION_STRATEGIES
from atomic_defake.human_response_generation import manual_input_human_responses
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
        # api_key = os.environ["MISTRAL_API_KEY"]
        
        # self.model = "open-mistral-nemo"
        # self.client = Mistral(api_key=api_key)
        self.reset()

    def reset(self):
        """
        """
        self.status = "start"
        self.verified = False
        self.post_text = None

        self.qa_pairs_h = {}

    def get_status(self):
        return self.status

    def get_output(self):
        """
        """
        print(self.post_text)

        if self.post_text is None:
            ret=-1
            user_response = "No post to verify" 
        else:
            if self.verified:
                ret=1
                user_response = self.post_text + " (Verified by ADF)"
            else:
                ret=0
                user_response=self.qa_pairs_h
        
        return self.verified, user_response

    def set_status(self, status):
        """ """
        assert status in STATUSES
        self.status = status

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
        self.set_status("wait")
        
        self.post_text = post_text
        print(self.post_text)

        run_id = self.generate_run_id()

        questions = self.generate_atomic_questions(post_text)
        time.sleep(3)

        responses = self.generate_responses(post_text, questions)

        final_label = self.aggregate_responses(run_id, responses)

        self.store_run(run_id, post_text, responses, final_label)

        self.set_status("completed")
        self.verified = final_label

    #########################################################################
    # Fake part for development. This should be replicated with the real version    
    # def verify_fake(self, post_text, threshold=0.5):
    #     self.set_status("wait")
    #     self.post_text = post_text



    #     likelihood = random.random()
    #     if likelihood > threshold:
    #         self.verified = True
    #     else:
    #         self.verified = False
    #     time.sleep(2)

    #     self.set_status("completed")

    def get_ai_questions_fake(self):
        """
        """
        adf_questions = {
            "qa_pair" : [
            {
                "question": "Is this OK? 1",
            },
            {
                "question": "Is this OK? 2",
            },
            {
                "question": "Is this OK? 3",
            },
            {
                "question": "Is this OK? 4",
            },
            {
                "question": "Is this OK? 5",
            },
            ]
        }

        return adf_questions

    def verify_ai_fake(self, post_text, threshold=0.5):
        self.set_status("wait")
        self.post_text = post_text

        print("AI Fake")
        print(self.post_text)

        time.sleep(2)

        self.set_status("human_responses")

    def set_human_responses(self, uuid, user_qas):
        """
        """
        if uuid not in self.qa_pairs_h:
            self.qa_pairs_h[uuid] = user_qas


    def detect_mislead_info_fake(self):
        """
        """
        # final_label = self.aggregate_responses(run_id, responses)

        ### Aggregate results from the human and the AI
        self.set_status("aggregation")
        
        threshold=0.5

        likelihood = random.random()
        
        print(threshold)
        print(likelihood)
        
        if likelihood > threshold:
            self.verified = True
        else:
            self.verified = False

        time.sleep(3)

        self.set_status("completed")
