import os
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from tqdm import tqdm
import anthropic
from langchain_google_genai import ChatGoogleGenerativeAI
import time

# Load the environment variables from the .env file
load_dotenv()

def initialize_anthropic_c35(prompt, temperature=0, max_tokens=2000):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    # print(message.content)
    return message


model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    project="nav29-21389",
    location="europe-southwest1",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    max_output_tokens=800,
)
# Importing the dataset from MIR md
# dataset = pd.read_excel('data/MIR24GPT.xlsx')

dataset2025 = pd.read_excel('data/MIR25_answered_20250128.xlsx', sheet_name='Sheet1')
print(dataset2025.columns)
# In col, GPT-4, save the answers from GPT-4
PROMPT_TEMPLATE = "Behave like a hypotethical doctor who has to answer the following question. You have to indicate only a number 1-4 with the correct answer. Don't output anything different than 1-4 please. The question is \n:{description}"

PROMPT_2025 = "Behave like a hypotethical doctor who has to answer the following question. I am taking the Spanish MIR exam. Answer only the correct answer, there is no need to explain the answer (there can only be one correct): \n {description}"

# Define the chat prompt templates
human_message_prompt = HumanMessagePromptTemplate.from_template(PROMPT_TEMPLATE)
chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])

# Iterate over the rows with indices 0-10 in the data
for index, row in tqdm(dataset2025.iterrows(), total=dataset2025.shape[0]):
    # Get the ground truth (GT) and the description
    description = row["Description"]
    print(f"Description: {description}")
    # Generate the answer using the GPT-4 model
    formatted_prompt = chat_prompt.format_messages(description=description)
    attempts = 0
    while attempts < 2:
        try:
            diagnosis = model.invoke(formatted_prompt)
            if hasattr(diagnosis, 'content'):
                result = diagnosis.content
            else:
                result = str(diagnosis)
            print(f"Respuesta: {result}")
            dataset2025.iloc[index, 6] = result
            break
        except Exception as e:
            attempts += 1
            print(f"Error: {e}")
            if attempts == 2:
                dataset2025.iloc[index, 6] = "ERROR"
                print("Máximo número de intentos alcanzado")

    # Añadir un tiempo de espera entre peticiones
    time.sleep(2)  # espera 2 segundos entre peticiones

    # Add the diagnoses to column number 6 (GPT-4)
    # dataset2025.iloc[index, 6] = diagnosis.content
    # dataset2025.iloc[index, 5] = diagnosis.content
    # dataset2025.iloc[index, 4] = diagnosis_c35

# Save the diagnoses to a new XLSX file
dataset2025.to_excel('data/MIR25_answered_20250128.xlsx', index=False)

