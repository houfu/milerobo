# Milerobo

A project to explore whether data augmented LLM can "beat" ChatGPT, and 
how far it can go to satisfy a human expert.

* ChatGPT is a chatbot developed by OpenAI built on top of OpenAi's GPT3 family of large language models.
It's finetuned and trained, and is known to give articulate answers.
* The [Milelion](https://milelion.com/about-us) is a "Singapore-based miles and points resource that teaches 
you how to travel better for less".
A very niche website catering to a very niche "hobby".
* On 11 February 2023, a [post on the Milelion](https://milelion.com/2023/02/11/can-chatgpt-handle-miles-and-points-questions/)
tested ChatGPT on several miles related question. The writer posted the response from ChatGPT as well as his evaluation of the answer.
The conclusion in short: "Perhaps, but not today."
* I was curious to see whether a "data augmented" approach can improve ChatGPT's results and this repository 
posts the results.

In short, the code in this repo does the following:
1. Scrape several blog articles from the Milelion site and store in a vector store.
2. When a question is asked, the LLM chain retrieves the 4 most similar articles from the scraped blog articles
and uses them as context to assist a GPT3 LLM to generate an answer.
3. Compare the answer from my LLM with ChatGPT and the evaluation of a human expert, and reflect.

**TODO: Blog post in more detail**

## How to run the code in this repository

**Pre-requisites**
* An OpenAI Api Key. You can obtain one by signing up for an account with OpenAI 
(Embeddings and completions are NOT FREE)
* A vectorstore from Weaviate. A sandbox account should be sufficient for toying with this code.

In order to run the notebook, you need a vectorstore that is filled with chunks of Milelion articles.
Running the scraper in this repository with the pre-requisites to get this vectorstore.


1. Clone the repo
2. Run `poetry install`. The dependencies are grouped into two: `poetry install -G scraper` 
installs the dependencies which are used for the scraper. `poerty install` is sufficient to install
the dependencies that are needed to run the notebook.
3. Create a `.env` file with the necessary variables. The example shows you the values you need to
input.
4. In the first milelion directory, run the shell command `scrapy crawl articles` (This will scrape 
the website, separate the articles into chunks, upload it to weaviate and vectorise them)
5. Once the process is finished, you can run the notebook and get some results.

## Disclaimer

This project is for my education and research purpose only. I never promised a chatbot that
will answer all your miles related question. I am not responsible for any losses 
if you relied on the advice given by this model.

## Contact
You can reach me via [email](mailto:houfu@lovelawrobots.com)