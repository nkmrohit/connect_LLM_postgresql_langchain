from langchain import OpenAI, SQLDatabase
from langchain.chat_models import ChatOpenAI
#from langchain import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain

username = "postgres"
password = '123456789'
host = "127.0.0.1"
port = "5432"
mydatabase = "llm-postgresql"

pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"

db = SQLDatabase.from_uri(pg_uri)
print(db)

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







