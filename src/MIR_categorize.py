import os
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from tqdm import tqdm


# Load the environment variables from the .env file
load_dotenv()

# Initialize the AzureChatOpenAI model
model = AzureChatOpenAI(
    openai_api_version="2023-06-01-preview",
    azure_deployment="nav29",
    temperature=0,
    max_tokens=800,
    model_kwargs={"top_p": 1, "frequency_penalty": 0, "presence_penalty": 0}
)

# Importing the dataset from MIR md
dataset = pd.read_excel('data/MIR24GPT.xlsx')

# In col, GPT-4, save the answers from GPT-4
PROMPT_TEMPLATE = """Behave like a hypotethical doctor who has to categorize the following question. You have to indicate only a the Category from the list I give you that is most appropriate. 

Categorys:

--------------------
Digestivo
Cardiología
Estadística
Infecciosas
Miscelánea
Neumología
Neurología
Ginecología
Endocrinología
Hematología
Reumatología
Nefrología
Pediatría
Psiquiatría
Traumatología
Dermatología
Urología
ORL (Otorrinolaringología)
Oftalmología
Inmunología
--------------------

Don't output anything different than one and only category please, and in Spanish. The question is \n:{description}"""

# Define the chat prompt templates
human_message_prompt = HumanMessagePromptTemplate.from_template(PROMPT_TEMPLATE)
chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])

# Iterate over the rows with indices 0-10 in the data
for index, row in tqdm(dataset.iterrows(), total=dataset.shape[0]):
    # Get the ground truth (GT) and the description
    description = row[1]
    # Generate the answer using the GPT-4 model
    formatted_prompt = chat_prompt.format_messages(description=description)
    attempts = 0
    while attempts < 2:
        try:
            diagnosis = model(formatted_prompt).content  # Call the model instance directly
            break
        except Exception as e:
            attempts += 1
            print(e)
            if attempts == 2:
                diagnosis = "ERROR"

    # Add the diagnoses to column number 6 (GPT-4)
    dataset.iloc[index, 2] = diagnosis

# Save the diagnoses to a new XLSX file
dataset.to_excel('data/MIR24GPT_categorized.xlsx', index=False)