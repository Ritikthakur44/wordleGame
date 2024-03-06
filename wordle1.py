from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session  # new import
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # new line
app.config['SESSION_TYPE'] = 'filesystem'  # new line
Session(app)  # new line

# The secret words and their hints
words = {
    "apple": [
        "I'm a type of fruit that can be used to make a popular beverage.",
        "I'm a symbol of knowledge in a famous story about gravity.",
        "I'm a common ingredient in a traditional autumn dessert."
    ],
    "banana": [
        "I'm a fruit that's often eaten raw and is rich in potassium.",
        "I'm a key ingredient in a popular split dessert.",
        "I'm a fruit that monkeys are famously fond of."
    ],
    "cat": [
        "I'm a popular pet known for my independence.",
        "I'm an animal that's often associated with having nine lives.",
        "I'm a small carnivorous mammal that's often kept as a pet."
    ],
    "dog": [
        "I'm a domesticated carnivorous mammal that's often called man's best friend.",
        "I'm a popular pet known for my loyalty and playfulness.",
        "I'm an animal that comes in breeds like Labrador, Poodle, and Bulldog."
    ],
    "elephant": [
        "I'm the largest land animal.",
        "I'm known for my long trunk and large ears.",
        "I'm an animal that's often associated with memory."
    ],
    "flamingo": [
        "I'm a bird known for my pink feathers and long, thin legs.",
        "I'm a bird that's often seen standing on one leg.",
        "I'm a bird that's native to parts of Africa, the Americas, and Asia."
    ],
    "giraffe": [
        "I'm the tallest living terrestrial animal.",
        "I'm known for my long neck and legs.",
        "I'm an animal that's native to Africa."
    ],
    "hippopotamus": [
        "I'm a large, mostly herbivorous mammal that's native to sub-Saharan Africa.",
        "I'm known for my large size and spend most of my time in water.",
        "I'm an animal that's often just called a 'hippo'."
    ],
    "iguana": [
        "I'm a lizard that's native to tropical areas of Central and South America.",
        "I'm known for my dewlap and spines running down my back.",
        "I'm a reptile that's often kept as a pet."
    ],
    "jaguar": [
        "I'm a large cat species native to the Americas.",
        "I'm known for my powerful build and beautiful rosette-covered coat.",
        "I'm an animal that's the third-largest big cat species after the tiger and lion."
    ]
}

@app.route("/", methods=["GET", "POST"])
def play_wordle():
    if 'attempts' not in session:
        session['attempts'] = 5
        session['word'], hints = random.choice(list(words.items()))
        session['hint'] = random.choice(hints)

    message = ""
    result = ""

    if request.method == "POST":
        guess = request.form["guess"]

        if len(guess) != len(session['word']):
            message = f"Guess should be {len(session['word'])} letters long!"
        else:
            for g, w in zip(guess, session['word']):
                if g == w:
                    result += '<span style="color: green;">🟩</span>'
                elif g in session['word']:
                    result += '<span style="color: yellow;">🟨</span>'
                else:
                    result += '<span style="color: red;">🟥</span>'

            if guess == session['word']:
                return redirect(url_for('win'))

            session['attempts'] -= 1
            if session['attempts'] == 0:
                return redirect(url_for('lose'))

            # Change the hint when the user guesses the word wrong
            session['hint'] = random.choice(words[session['word']])

    return render_template("index.html", attempts=session['attempts'], message=message, result=result, hint=session['hint'])

@app.route("/win", methods=["GET"])
def win():
    session.clear()
    return render_template("win.html")

@app.route("/lose", methods=["GET"])
def lose():
    correct_word = session['word']
    session.clear()
    return render_template("lose.html", correct_word=correct_word)

if __name__ == "__main__":
    app.run(debug=True)
