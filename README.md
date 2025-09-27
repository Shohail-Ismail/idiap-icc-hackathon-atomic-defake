# Atomic DeFake

# Description
Prototype made by [Shohail Ismail](https://github.com/Shohail-Ismail), [Michiel van der Meer](https://m0re4u.github.io/projects.html), and [Alessio Xompero](https://github.com/kerolex) for the 'Idiap Research Institute - Create Challenge 2024' hackathon to detect misinformation in text posts. Uses Streamlit UI and Mistral API pipeline to generate atomic assessment questions for fact-checking, combining AI and human answers to aggregate final trustworthiness verdicts. Also provides feedback for iterative content improvement, configurable as an automatable corrective feedback loop for pre-post content verification. Next steps involve training on [AVeriTeC](https://arxiv.org/abs/2305.13117) for enhanced accuracy and explainability.

## Requirements
* Anaconda
* Python 3.11

## Installation
```
conda create -n atomic-defake python=3.11

conda activate atomic-defake

pip install -r requirements.txt
```

## Setup
Create a `.env` file in the project root and put in your Mistral API key as follows:
```
MISTRAL_API_KEY=<YOUR_KEY>
```

## Running the application
```
streamlit run ui.py
```
After running the app, a Streamlit interface will open in your browser. After logging in (credentials aren't needed), click 'User post' from the sidebar and input text to verify for misinformation. After clicking the 'AtomicDeFake' button, you will be taken to the 'Contributor' screen where you can answer questions about the post, along with a final confidence score (you will need to do this twice so as to simulate more than one fact-checker). After doing this, the page will run the aggregator, then output the result (with feedback if the post is deemed to contain misinformation).
