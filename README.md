#**How to connect LLM to SQL database with LangChain SQLChain**

Introduction
In recent years, Large Language Models (LLMs) have become exponentially popular due to their remarkable capabilities in generating coherent and contextually relevant text across a wide range of domains. Although LLMs are used for answering questions, assisting in research, and helping engineers in software development, one of the major weaknesses LLMs have shown is their ability to generate incorrect or nonsensical text, also known as “hallucination.” For example, if you ask OpenAI’s ChatGPT: “When did France gift Lithuania Vilnius TV Tower?”, ChatGPT might respond: “France gifted Lithuania Vilnius TV Tower in 1980“, which is factually untrue since France had nothing to do with the construction of the Vilnius TV Tower.

One reason why LLMs can return such confident lies is that LLMs will attempt to conflate different sources of information on the internet to produce a response that is inaccurate or misleading. Another reason for LLMs’ hallucination is that the source of information isn’t accurate and that the LLM will use the information without validation. To help reduce LLM hallucination for a specific domain, we can attempt to connect a LLM to a SQL database which holds accurate structured information to be queried by the LLM. This will make the LLM focus on a single source for its information extraction, which allows the LLM to return the most accurate information possible provided by the database.

This article will demonstrate how to use a LLM with a SQL database by connecting OpenAI’s GPT-3.5 to a postgres database. We will be using LangChain for our framework and will be writing in Python.

**1. Getting started**
Let us install the required packages first, make sure you have already installed postgreSQL on your machine and have an OpenAI account as well. Create a new python virtual environment if needed:

pip install langchain 
pip install openai
pip install psycopg2
Create a file called main.py and import the following:

from langchain import OpenAI, SQLDatabase
from langchain.chat_models import ChatOpenAI
#from langchain import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain

**2. Connect the database**
Before we can connect the database to our LLM, let us first get a database to connect to. Since LangChain uses SQLAlchemy to connect to SQL databases, we can use any SQL dialect supported by SQLAlchemy, such as MS SQL, MySQL, MariaDB, PostgreSQL, Oracle SQL, Databricks, or SQLite. If you would like to know more about the requirements for connecting to databases, please refer to the SQLAlchemy documentation here. In my example I will be using Dataherald’s postgres real_estate database. This database contains 16 tables about rent, sales, inventory, and various other real estate information for locations across the United States in the last couple years. We will connect our LLM to this database in attempt to answer real estate questions in the United States.

The postgres database connection with psycopg2 looks like the following string:

username = "postgres"
password = '123456789'
host = "127.0.0.1"
port = "5432"
mydatabase = "llm-postgresql"

pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"


Now let us setup the connection for the database:

db = SQLDatabase.from_uri(pg_uri)



**3. Setup LLM**
Since we will be using GPT-3.5, we will use an OpenAI API key:

OPENAI_API_KEY = ""

llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

PROMPT = """ 
Given an input question, first create a syntactically correct postgresql query to run,  
then look at the results of the query and return the answer.  
The question: {question}
"""

#db_chain = SQLDatabaseSequentialChain(llm=llm, database=db, verbose=True, top_k=3)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, top_k=3)

question = "what is the average rent price in chicago from nov 2021 according to now?" 
# use db_chain.run(question) instead if you don't have a prompt
db_chain.run(PROMPT.format(question=question))

print(db_chain)

##Input and output

****Question : what is the average rent price in chicago from nov 2021 according to redfin?**
**

**Answer:The average rent price in Chicago from November 2021 until now is $1525.**

