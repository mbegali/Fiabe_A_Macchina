import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Imposta la tua chiave API di OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def generate_prompt(story_so_far):
    """Genera il prompt per GPT basato sulla storia attuale."""
    return f"La storia finora:\n{story_so_far}\n\nContinua la storia:"

def generate_story(prompt, temperature):
    """Genera una continuazione della storia utilizzando l'API aggiornata di OpenAI."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un narratore creativo. Rispondi esclusivamente in italiano."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def interactive_story():
    """Esegui una sessione interattiva di narrazione con GPT."""
    print("Benvenuto nell'esperienza di narrazione interattiva!")
    story = input("Inizia la storia: ")

    # Chiedi la temperatura una sola volta all'inizio
    while True:
        temp_input = input("Imposta la temperatura (0.1 - 1.0, default 0.7): ")
        try:
            temperature = float(temp_input) if temp_input else 0.7
            break  # Esci dal ciclo una volta ottenuto un input valido
        except ValueError:
            print("Input della temperatura non valido. Per favore, inserisci un numero tra 0.1 e 1.0.")

    while True:
        prompt = generate_prompt(story)
        gpt_continuation = generate_story(prompt, temperature)
        print(f"\nContinuazione di GPT:\n{gpt_continuation}\n")

        # Aggiungi la continuazione di GPT alla storia
        story += f" {gpt_continuation}"

        # L'utente continua la storia
        user_addition = input("Tocca a te continuare la storia (o digita 'exit' per terminare): ")
        if user_addition.lower() == 'exit':
            print("\nStoria finale:\n", story)
            break

        story += f" {user_addition}"

if __name__ == "__main__":
    interactive_story()
