## About The Project
Data visualization of data from transaction history and an NLP chat bot. The code for visualization was forked from the publication below. I added the chatbot feature and modified their code to make it work. 

## How to run

First, create and activate your virtual environment

Second, install the dependencies from requirements.txt
```
pip install -r requirements.txt
```

Third, fill in the .env file with your OPEN AI API key

Fourth, you want to put in whatever source documents you have within the sourceDocuments folder and run vector_gen.py
```
python3 vector_gen.py
```
This will convert the documents into vector embeddings to be stored within the vector Store

Lastly, run the code
```
streamlit run Chat2VIS.py
```

Code for visualization forked from the publication https://doi.org/10.1109/ACCESS.2023.3274199:

P. Maddigan and T. Susnjak, "Chat2VIS: Generating Data Visualizations via Natural Language Using ChatGPT, Codex and GPT-3 Large Language Models," in IEEE Access, vol. 11, pp. 45181-45193, 2023, doi: 10.1109/ACCESS.2023.3274199.
