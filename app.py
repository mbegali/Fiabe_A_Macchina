from flask import Flask, render_template, request, session, redirect, url_for
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret")  # Set a secure key in your .env!

def generate_prompt(story, user_input):
    return f"La storia finora:\n{story}\n\nL'utente ha scritto:\n{user_input}\n\nContinua la storia in italiano con un tono fiabesco. Devi continuare dalla sua ultima parola."

def generate_story(prompt, temperature):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un narratore esperto di fiabe. Rispondi esclusivamente in italiano."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if "story" not in session:
        session["story"] = ""
    if "temperature" not in session:
        session["temperature"] = 0.7

    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        if user_input.lower() == "exit":
            final_story = session["story"]
            session.clear()
            return render_template("end.html", story=final_story)

        temperature = float(request.form.get("temperature", 0.7))
        session["temperature"] = temperature
        session["story"] += " " + user_input

        prompt = generate_prompt(session["story"], user_input)
        ai_response = generate_story(prompt, temperature)
        session["story"] += " " + ai_response

        return render_template("index.html", story=session["story"], ai_response=ai_response, temperature=temperature)

    return render_template("index.html", story=session["story"], ai_response=None, temperature=session["temperature"])

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
