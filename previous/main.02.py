import os
import openai
from dotenv import load_dotenv

def generate_prompt(story_so_far: str) -> str:
    """Genera il prompt per GPT basato sulla storia attuale."""
    return f"La storia finora:\n{story_so_far}\n\nContinua la storia:"

def generate_story(prompt: str, temperature: float) -> str:
    """Genera una continuazione della storia utilizzando l'API aggiornata di OpenAI."""
    # Assicurati di avere la tua chiave API caricata
    response = openai.ChatCompletion.create(
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

    # Chiedi la temperatura una sola volta
    while True:
        temp_input = input("Imposta la temperatura (0.1 - 1.0, default 0.7): ")
        try:
            temperature = float(temp_input) if temp_input else 0.7
            break
        except ValueError:
            print("Input non valido. Riprova con un numero tra 0.1 e 1.0.")

    while True:
        # Prima di generare il prompt, l’utente scrive il suo pezzo
        user_addition = input(
            "\nTocca a te continuare la storia (o digita 'exit' per terminare): "
        )
        if user_addition.lower() == "exit":
            print("\nStoria finale:\n", story)
            break

        # Appendi PRIMA il testo dell’utente
        story += f" {user_addition}"

        # Ora costruiamo il prompt con tutto lo story
        prompt = generate_prompt(story)

        # Chiediamo a GPT di continuare la storia
        gpt_continuation = generate_story(prompt, temperature)
        print(f"\nContinuazione di GPT:\n{gpt_continuation}\n")

        # Aggiungiamo la risposta di GPT
        story += f" {gpt_continuation}"

if __name__ == "__main__":
    # Carica la chiave API da .env oppure da variabile d'ambiente
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Avvia l'interazione
    interactive_story()
