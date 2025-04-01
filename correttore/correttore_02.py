import openai
import os
from docx import Document
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to get feedback from GPT (updated for OpenAI v1.0+)
def get_gpt_feedback(sentence):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ Initialize the client
    response = client.chat.completions.create(  # ✅ Use new API format
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert Italian language teacher. Analyze the sentence for grammar mistakes and provide a correction with a short explanation in English."},
            {"role": "user", "content": f"Sentence: '{sentence}'"}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content  # ✅ New way to access response

# Load the student's Word document
doc = Document("student_essay.docx")

# Process each paragraph
for para in doc.paragraphs:
    if para.text.strip():  # Ignore empty lines
        gpt_feedback = get_gpt_feedback(para.text)
        para.text += f" [Attento qui: {gpt_feedback}]"  # Add GPT comment

# Save the document
doc.save("student_essay.docx")
print("Grammar feedback added using GPT!")
