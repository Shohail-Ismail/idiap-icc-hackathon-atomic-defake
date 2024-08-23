from atomic_defake.aggregation import verify_post
from atomic_defake.question_generation import question_generation
from atomic_defake.human_response_generation import manual_input_human_responses

class AtomicDeFake:
    def __init__(self, aggregation_method):
        self.aggregation_method = aggregation_method

    def generate_atomic_questions(self):
        pass

    def generate_LLM_responses(self, questions):
        pass

    def generate_human_responses(self, questions):
        pass

    def generate_responses(self, questions):
        self.generate_LLM_responses(questions)
        self.generate_human_responses(questions)

    def aggregate_responses(self, qa_pairs):
        return verify_post("test_run_id", qa_pairs, method=self.aggregation_method)

    def verify(self):
        questions = self.generate_atomic_questions()

        responses = self.generate_responses(questions)

        return self.aggregate_responses(responses)

