# Atomic DeFake
   * [Description](#description)
   * [Running the app](#running-the-app)
   * [Guide](#guide)
   * [Things to note](#things-to-note)


## Description
Prototype made by [Shohail Ismail](https://github.com/Shohail-Ismail), [Michiel van der Meer](https://m0re4u.github.io/projects.html), and [Alessio Xompero](https://github.com/kerolex) for the 'Idiap Research Institute - Create Challenge 2024' hackathon to detect misinformation in text posts. Uses Streamlit UI and Mistral API pipeline to generate atomic assessment questions for fact-checking, combining AI and human answers to aggregate final trustworthiness verdicts. Also provides feedback for iterative content improvement, configurable as an automatable corrective feedback loop for pre-post content verification. Next steps involve training on [AVeriTeC](https://arxiv.org/abs/2305.13117) for enhanced accuracy and explainability.

---

## Running the app
### Requirements
* Anaconda
* Python 3.11

### Installation
```
conda create -n atomic-defake python=3.11

conda activate atomic-defake

pip install -r requirements.txt
```

### Setup
Create `.env` file in the project root and put in your Mistral API key as follows:
```
MISTRAL_API_KEY=<YOUR_KEY>
```

### Run
```
streamlit run ui.py
```
---

## Guide 

1) After running the app, a Streamlit interface will open in your browser. After logging in (credentials aren't needed), click 'User post' from the sidebar and input text to verify for misinformation, then click the 'AtomicDeFake' button.
2) You will then be taken to the 'Contributor' screen where you can answer AI-generated questions about the post and give a final confidence score in your answers.
    - The reason for this is that AtomicDeFake works on a reciprocal crowdsourcing system, so to get your post verified, you must answer 5 questions on 2 different users' posts. Though, for the sake of this demo, you will be answering the same questions on your own post twice.
3) After doing this, the page will run the aggregator, which combines AI analysis with what other people have said about your post, thus exhibiting an AI + Human-In-The-Loop (HITL) system.
4) If the post is deemed to contain misinformation, the human + AI responses are given, with a prompt to rewrite and resubmit your post, else the post is verified and deemed to be factual.


---


## Things to note

- The aggregator is precision-oriented and risk-averse, favouring false negatives over false positives (except certain edge cases detailed below). This means that two abstentions by contributors vetoes the verification regardless of AI responses. It also means that absolute quantifiers (always/never/zero) will often nudge the evaluation AI towards declaring the post false, which encourages nuance in language.
    - **TEST**: consistent "I don't know" answers
    - **FUTURE**: fine-tuning the model to better distinguish and setting up AI-overrule thresholds/consensus-forcing question loops for abstention
- The question-generation AI operates at clause-level granularity so that false subclaims are not ignored in favour of more/larger true (sub)claims; in other words, it splits post text into **atomic** claims. This characteristic is also embodied by the truthfulness evaluation AI, owing to its risk-averse nature, meaning that one erroneous sub-claim voids the whole post.
    - **TEST**: multi-claim text, i.e., "The sky is blue and clouds are green", “mRNA COVID-19 vaccines contain microchips and reduce severe disease risk”, etc.
    - **FUTURE**: the current mechanism is fine, though feedback could be made more granular (per sub-claim).
- The aggregator is currently primed to trust human responses implicitly over AI, which decreases distrust from public and risk of hallucinations swaying consensus. However, this also means that, if a clearly factual statement ("The sky is blue") is deemed by at least one of the human contributors to be false, it is voided as such - even if the AI and other human recognise the text as factual.
    - **TEST**: treating factual questions as false, and answering the HITL questions as such.
    - **FUTURE**: implement aform of reputation and disagreement audits to gain more information on reasons - if given reasons are weak, decrease reputation.


<!-- yo README, I'm extremely tired and I'm gonna go climb now, later bro -->