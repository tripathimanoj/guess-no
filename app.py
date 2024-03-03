from flask import Flask, render_template, request
import random

app = Flask(__name__)

max_tries = 5
tries_left = max_tries
secret_number = None  # Initialize secret_number as None initially

def generate_secret_number():
    global secret_number
    secret_number = random.randint(1, 100)

# Generate secret number when the program starts and when the page is reloaded
generate_secret_number()

@app.route('/guptchar')  # guptchar ko sub pata hai
def get_secret():
    global secret_number
    if secret_number is None:
        return "The secret number has not been generated yet. Play the game first."
    sc = secret_number
    return f"The secret number is: {sc}"  # guptchar ne kaan mai bta diya ==> call guptchar in this endpoiint /guptchar

@app.route('/')
def homepage():
    global tries_left
    global max_tries
    global secret_number

    # Generate a new secret number when the homepage is accessed
    generate_secret_number()

    tries_left = max_tries
    return render_template('index.html', max_tries=max_tries)

@app.route('/guess', methods=['POST'])
def result():
    global tries_left
    global max_tries
    global secret_number
    
    guess = int(request.form['guess'])

    tries_left -= 1

    if tries_left == 0 or guess == secret_number:
        if guess == secret_number:
            message = "Congratulations! You guessed the correct number."
        else:
            message = f"Sorry, you ran out of tries. The secret number was {secret_number}."
        tries_left = max_tries
        return render_template('result.html', message=message)
    else:
        if guess < secret_number:
            message = "Your guess is too low. Try again."
        else:
            message = "Your guess is too high. Try again."
        return render_template('index.html', message=message, tries_left=tries_left, max_tries=max_tries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
