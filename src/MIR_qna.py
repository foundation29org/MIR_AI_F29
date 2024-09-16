import os
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from tqdm import tqdm
import anthropic


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

# Initialize the AzureChatOpenAI model
model = AzureChatOpenAI(
    openai_api_version="2023-06-01-preview",
    azure_deployment="nav29",
    temperature=0,
    max_tokens=800,
    model_kwargs={"top_p": 1, "frequency_penalty": 0, "presence_penalty": 0}
)

model_name = "gpt-4o"
openai_api_key=os.getenv("OPENAI_API_KEY")
gpt4o = ChatOpenAI(
        openai_api_key = openai_api_key,
        model_name = model_name,
        temperature = 0,
        max_tokens = 800,
    )


# Importing the dataset from MIR md
dataset = pd.read_excel('data/MIR24GPT.xlsx')

# In col, GPT-4, save the answers from GPT-4
PROMPT_TEMPLATE = "Behave like a hypotethical doctor who has to answer the following question. You have to indicate only a number 1-4 with the correct answer. Don't output anything different than 1-4 please. The question is \n:{description}"

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
            diagnosis = gpt4o(formatted_prompt).content  # Call the model instance directly
            print(diagnosis)
            diagnosis_c35 = initialize_anthropic_c35(formatted_prompt[0].content).content[0].text
            print(diagnosis_c35)
            break
        except Exception as e:
            attempts += 1
            print(e)
            if attempts == 2:
                diagnosis = "ERROR"
                diagnosis_c35 = "ERROR"

    # Add the diagnoses to column number 6 (GPT-4)
    dataset.iloc[index, 5] = diagnosis
    dataset.iloc[index, 6] = diagnosis_c35

# Save the diagnoses to a new XLSX file
dataset.to_excel('data/MIR24GPT_answered_20240916.xlsx', index=False)

