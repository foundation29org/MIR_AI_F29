import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Importing the dataset from MIR md
dataset = pd.read_excel('data/24/MIR24GPT_final.xlsx')

# head
print(dataset.head())

"""
  Numero                                           Pregunta    Especialidad  Respuesta correcta  Respuesta correcta Ministerio V0.   GPT-4  Claude  Bard  Medisearch  Copilot 
0      1  Pregunta asociada a la imagen 1.\nHombre de 56...  Endocrinología                 NaN                                 2.0      2     NaN   NaN         NaN       NaN
1      2  Pregunta asociada a la imagen 2.\nPaciente que...   Traumatología                 NaN                                 4.0      3     NaN   NaN         NaN       NaN
2      3  Pregunta asociada a la imagen 3.\nHombre de 75...    Dermatología                 NaN                                 2.0      2     NaN   NaN         NaN       NaN
3      4  Pregunta asociada a la imagen 4.\nHombre de 25...    Dermatología                 NaN                                 3.0      3     NaN   NaN         NaN       NaN
4      5  Pregunta asociada a la imagen 5.\n\nMujer de 3...     Ginecología                 NaN                                 3.0      3     NaN   NaN         NaN       NaN
"""

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Exploratory Data Analysis (EDA)

# Summary statistics for numerical columns
print("Summary Statistics:\n", dataset.describe())

# Check for missing values
print("\nMissing Values:\n", dataset.isnull().sum())

# Distribution of 'Especialidad' for rows 25 and onwards (No miramos las preguntas con Imágenes de momento)
dataset_from_25 = dataset.iloc[25:]
fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
sns.countplot(y='Especialidad', data=dataset_from_25, order = dataset_from_25['Especialidad'].value_counts().index, ax=ax)
ax.set_title('Distribución de Especialidades (Sin Preguntas de Imágenes)')
ax.set_xlabel('Count')
ax.set_ylabel('Specialty')
fig.savefig('data/24/specialties_distribution_no_images.png', dpi=300)

# Now for this same distribution take the columns 5 and 6 (Correcta Ministerio y GPT-4) and calculate the accuracy of GPT-4
correct_answers = dataset_from_25.iloc[:, 4].values.astype(int)
gpt_answers = dataset_from_25.iloc[:, 5].values.astype(int)
accuracy = sum(correct_answers == gpt_answers) / len(correct_answers)
error = 1 - accuracy
print(f"\nAccuracy of GPT-4: {accuracy}")
print(f"Error of GPT-4: {error}")

# # Print me the ones that are wrong
# print("\nWrong Answers:")
# for i in range(len(correct_answers)):
#     if correct_answers[i] != gpt_answers[i]:
#         print(f"Correct: {correct_answers[i]}, GPT-4: {gpt_answers[i]}")

# Now we will do a distribution of categories and each accuracy for each category. We will do this for the rows 25 and onwards.
# You already have the categories in the column 2 (Especialidad)
# Calculate the accuracy of GPT-4 for each category in 'Especialidad'
category_accuracy = dataset_from_25.groupby('Especialidad').apply(
    lambda x: sum(x.iloc[:, 4].values.astype(int) == x.iloc[:, 5].values.astype(int)) / len(x)
)

# Create a bar plot for the accuracy of GPT-4 for each category
# Convert accuracy to percentage
category_accuracy_percentage = category_accuracy * 100

# Create a reversed color palette suitable for a research paper
colors = sns.color_palette('rocket_r', len(category_accuracy))[::-1]

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
category_accuracy_percentage.sort_values(ascending=False).plot(kind='bar', ax=ax, color=colors)
ax.set_title('Precisión de GPT-4 por Especialidad')
ax.set_xlabel('Especialidad')
ax.set_ylabel('Precisión (%)')
plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig('data/24/gpt4_accuracy_by_specialty.png', dpi=300)

# Print the accuracy for each category in percentage
print("\nAccuracy of GPT-4 by Specialty (%):")
print(category_accuracy_percentage)

# Now we will do a analysis of the answers of GPT-4 Vision for the rows 0-25.
# We will do a distribution of categories and each accuracy for each category. We will do this for the rows 0-25.

dataset_img = pd.read_excel('data/24/MIR24GPT_vision_answered_v2.xlsx')
dataset_img = dataset_img.iloc[:25]

# Calculate the accuracy of GPT-4 Vision vs GPT-4 vs Correcta Ministerio.
correct_answers = dataset_img.iloc[:, 4].values.astype(int)
gpt_answers = dataset_img.iloc[:, 6].values.astype(int)
gpt_vision_answers = dataset_img.iloc[:, 5].values.astype(int)

gpt_accuracy = sum(correct_answers == gpt_answers) / len(correct_answers)
gpt_error = 1 - gpt_accuracy
print(f"\nAccuracy of GPT-4: {gpt_accuracy} for images")
print(f"Error of GPT-4: {gpt_error} for images")

gpt_vision_accuracy = sum(correct_answers == gpt_vision_answers) / len(correct_answers)
gpt_vision_error = 1 - gpt_vision_accuracy
print(f"\nAccuracy of GPT-4 Vision: {gpt_vision_accuracy}")
print(f"Error of GPT-4 Vision: {gpt_vision_error}")

# Now combine the two accuracies in a bar plot
# Create a color palette
colors = sns.color_palette('hsv', 2)

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.bar(x=['GPT-4', 'GPT-4 Vision'], height=[gpt_accuracy, gpt_vision_accuracy], color=colors)
ax.set_title('Precisión de GPT-4 vs GPT-4 Vision')
ax.set_xlabel('Modelo')
ax.set_ylabel('Precisión (%)')
fig.tight_layout()
fig.savefig('data/24/gpt4_vs_gpt4_vision.png', dpi=300)

# Now we will do a distribution of categories and each accuracy for each category. Combining GPT-4 and GPT-4 Vision.
# Merge general dataset from 25 onwards with the dataset with images from 0-25
dataset_from_25 = dataset_from_25.reset_index(drop=True)
dataset_img = dataset_img.reset_index(drop=True)
dataset_merged = pd.concat([dataset_from_25, dataset_img], axis=0)

# Calculate the accuracy of GPT-4 vs Correcta Ministerio.
correct_answers = dataset_merged.iloc[:, 4].values.astype(int)
gpt_answers = dataset_merged.iloc[:, 5].values.astype(int)
gpt_accuracy = sum(correct_answers == gpt_answers) / len(correct_answers)
gpt_error = 1 - gpt_accuracy
print(f"\nTotal Accuracy of GPT-4: {gpt_accuracy}")
print(f"Total Error of GPT-4: {gpt_error}")

# Now calculate the accuracy again but for each category in 'Especialidad'
category_accuracy = dataset_merged.groupby('Especialidad').apply(
    lambda x: sum(x.iloc[:, 4].values.astype(int) == x.iloc[:, 5].values.astype(int)) / len(x)
)

# Create a bar plot for the accuracy of GPT-4 for each category
# Convert accuracy to percentage
category_accuracy_percentage = category_accuracy * 100

# Create a color palette
colors = sns.color_palette('rocket_r', len(category_accuracy_percentage))[::-1]

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
category_accuracy_percentage.sort_values(ascending=False).plot(kind='bar', ax=ax, color=colors)
ax.set_title('Precisión de GPT-4 por Especialidad')
ax.set_xlabel('Especialidad')
ax.set_ylabel('Precisión (%)')
plt.xticks(rotation=45)
fig.tight_layout()
fig.savefig('data/24/complete_gpt4_accuracy_by_specialty.png', dpi=300)
