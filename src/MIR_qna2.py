import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import anthropic
from openai import AzureOpenAI

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

# Configuración de variables
endpoint = os.getenv("ENDPOINT_URL", "https://dxgptbot.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME2", "o1")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY2")

# Inicialización del cliente de Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-12-01-preview"
)

# Para debuggear
print(f"Endpoint: {endpoint}")
print(f"Deployment: {deployment}")
print(f"API Key: {subscription_key[:5]}...")

# Importing the dataset from MIR md
# dataset = pd.read_excel('data/24/MIR24GPT.xlsx')

dataset2025 = pd.read_excel('data/25/MIR25_answered_20250128.xlsx', sheet_name='Sheet1')
print(dataset2025.columns)
# In col, GPT-4, save the answers from GPT-4
PROMPT_TEMPLATE = "Behave like a hypotethical doctor who has to answer the following question. You have to indicate only a number 1-4 with the correct answer. Don't output anything different than 1-4 please. The question is \n:{description}"

PROMPT_2025 = "Behave like a hypotethical doctor who has to answer the following question. I am taking the Spanish MIR exam. Answer only the correct answer, there is no need to explain the answer (there can only be one correct): \n {description}"

# Modificar el bucle para empezar desde la fila 26
for index, row in tqdm(dataset2025.iterrows(), total=dataset2025.shape[0]):
    if pd.isna(dataset2025.iloc[index, 5]) or dataset2025.iloc[index, 5] == "ERROR":
        description = row["Description"]
        print(f"Row {index}: Description: {description}")
        
        attempts = 0
        while attempts < 2:
            try:
                completion = client.chat.completions.create(
                    model=deployment,
                    messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(description=description)}],
                    max_completion_tokens=800
                )
                diagnosis = completion.choices[0].message.content
                print(f"Row {index}: Answer: {diagnosis}")
                break
            except Exception as e:
                attempts += 1
                print(e)
                if attempts == 2:
                    diagnosis = "ERROR"

        dataset2025.iloc[index, 5] = diagnosis

# Save the diagnoses to a new XLSX file
dataset2025.to_excel('data/25/MIR25_answered_20250128.xlsx', index=False)

