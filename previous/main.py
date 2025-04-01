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

def generate_story(prompt, temperature=0.7):
    """Generate a story continuation from GPT using the updated OpenAI API."""
    client = openai.OpenAI()  # Create a new client instance
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
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

    while True:
        prompt = generate_prompt(story)

        # Get user input for temperature setting
        try:
            temp_input = input("Set the temperature (0.1 - 1.0, default 0.7): ")
            temp = float(temp_input) if temp_input else 0.7
            gpt_continuation = generate_story(prompt, temperature=temp)
            print(f"\nGPT's continuation:\n{gpt_continuation}\n")
        except ValueError:
            print("Invalid temperature input. Using default (0.7).")
            gpt_continuation = generate_story(prompt, temperature=0.7)

        # Append GPT's addition
        story += f" {gpt_continuation}"

        # User continues the story
        user_addition = input("Your turn to continue the story (or type 'exit' to stop): ")
        if user_addition.lower() == 'exit':
            print("\nFinal Story:\n", story)
            break

        story += f" {user_addition}"

if __name__ == "__main__":
    interactive_story()
