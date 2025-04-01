import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Keep 'story' as an empty string if you plan to use it globally.
# Or define it inside 'interaction()'—but let's keep it here for now:
story = ""

def generate_prompt(story, user_input):
    return f"La storia finora:\n{story}\n\nL'utente ha scritto:\n{user_input}\n\nContinua la storia in italiano con un tono fiabesco:"

def generate_story(prompt, temperature):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un narratore esperto di fiabe. Rispondi esclusivamente in italiano. "},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def user_starts():
    return input("Inizia la storia: ")

def ask_temperature():
    while True:
        print("Che temperatura vuoi? Usa un numero tra 0.1 e 1.0:")
        try:
            temperature = float(input())
            if 0.1 <= temperature <= 1.0:
                return temperature
            else:
                print("Errore: Il numero deve essere tra 0.1 e 1.0.")
        except ValueError:
            print("Errore: Inserisci un numero valido tra 0.1 e 1.0.")

def interaction():
    global story  # If you want to modify the global 'story', or just define story locally.

    print("Incomincia la tua storia:")
    user_input = input()            # 1) First user input
    temperature = ask_temperature() # 2) Ask temperature

    while True:
        # Append the user's input to story
        story += " " + user_input

        # Create the prompt from the updated story
        prompt = generate_prompt(story, user_input)

        # Check if the user typed 'exit'
        if user_input.lower() == "exit":
            print("Fine della storia.")
            return  # or break, depending on how you want to exit

        # Generate the AI response
        AI_response = generate_story(prompt, temperature)

        # Append AI response to story
        story += " " + AI_response

        # Print or do something with the updated story
        print("\n--- Storia finora ---")
        print(AI_response)

        # Ask the user for more input
        user_input = input("\nContinua la storia (o 'exit' per terminare): ")

# Notice: We removed the lines that tried to call generate_prompt and generate_story
# at the top level, because they referred to user_input and temperature which don't
# exist until we get them from within interaction().

interaction()