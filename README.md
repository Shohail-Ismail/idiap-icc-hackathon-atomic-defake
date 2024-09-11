# Atomic DeFake

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
