import openai
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key (you can also set it as an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(story_so_far):
    """Generate the prompt for GPT based on the current story."""
    return f"The story so far:\n{story_so_far}\n\nContinue the story:"

def generate_story(prompt, temperature):
    """Generate a story continuation from GPT using the updated OpenAI API."""
    client = openai.OpenAI()  # Create a new client instance
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un grande scrittore di fiabe. Scrivi sempre in Italiano"},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def interactive_story():
    """Run an interactive storytelling session with GPT."""
    print("Welcome to the Interactive Storytelling Experience!")
    story = input("Start the story: ")

    # Ask for the temperature once at the beginning
    while True:
        temp_input = input("Set the temperature (0.1 - 1.0, default 0.7): ")
        try:
            temperature = float(temp_input) if temp_input else 0.7
            break  # Exit loop once valid input is given
        except ValueError:
            print("Invalid temperature input. Please enter a number between 0.1 and 1.0.")

    while True:
        prompt = generate_prompt(story)
        gpt_continuation = generate_story(prompt, temperature)
        print(f"\nGPT's continuation:\n{gpt_continuation}\n")

        # Append GPT's addition
        story += f" {gpt_continuation}"

        # User continues the story
        user_addition = input("Ora tocca a te continuare la storia: ")
        if user_addition.lower() == 'exit':
            print("\nFinal Story:\n", story)
            break

        story += f" {user_addition}"

if __name__ == "__main__":
    interactive_story()
