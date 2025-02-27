import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from tqdm import tqdm
import time

# Load the environment variables from the .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 800,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-01-21",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Cargar el dataset
dataset2025 = pd.read_excel('data/MIR25_answered_20250128.xlsx', sheet_name='Sheet1')
print(dataset2025.columns)

PROMPT_TEMPLATE = """Behave like a hypotethical doctor who has to answer the following question. You have to indicate only a number 1-4 with the correct answer. Don't output anything different than 1-4 please. The question is:
{description}"""

# Iterate sobre las filas con respuestas vacías o ERROR
for index, row in tqdm(dataset2025.iterrows(), total=dataset2025.shape[0]):
    if pd.isna(dataset2025.iloc[index, 6]) or dataset2025.iloc[index, 6] == "ERROR":
        description = row["Description"]
        prompt = PROMPT_TEMPLATE.format(description=description)
        print(f"Description: {description}")
        
        attempts = 0
        while attempts < 2:
            try:
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                result = response.text.strip()
                print(f"Respuesta: {result}")
                print(f"indice de resultado: {index}")
                dataset2025.iloc[index, 6] = result
                break
            except Exception as e:
                attempts += 1
                print(f"Error: {e}")
                if attempts == 2:
                    dataset2025.iloc[index, 6] = "ERROR"
                    print(f"indice de resultado: {index}")
                    print("Máximo número de intentos alcanzado")
        
        time.sleep(2)  # espera 2 segundos entre peticiones

# Save the diagnoses to a new XLSX file
dataset2025.to_excel('data/MIR25_answered_20250128.xlsx', index=False)

