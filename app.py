from flask import Flask, render_template, request, jsonify, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI
from sqlalchemy import text
import secrets
from db import EmotionAnalysis, MoodTracker, ThoughtDiary, ChatSummary, Users, Chat, Messages
from Emotion import analyze_and_insert_emotions
from Sentiment import get_sentiments
from Summary import summarize_and_insert_summary
#from chatgpt import start_chatbot
#from blenderbot import generate_response
#from dialoGPT import chat_with_dialogpt
import json
#from chat import NLP_response
from datetime import datetime,date

app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

# Initialize SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask application
app.secret_key = secret_key




@app.route('/')
def index():
    return render_template('model.html')


def create_user(username, email, password):
    try:
        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return True  # User created successfully
    except Exception as error:
        print(f"Error creating user: {error}")
        return False  # Error creating user


# Function to check if a user exists and validate the password
def check_user(username, password):
    try:
        user = Users.query.filter_by(username=username).first()

        if user is None:
            return False  # User does not exist

        # Validate the password using bcrypt or another secure method
        # For example, using bcrypt:
        # if bcrypt.check_password_hash(user.password, password):
        if user.password == password:
            return True  # Login successful
        else:
            return False  # Incorrect password

    except Exception as error:
        print(f"Error checking user: {error}")
        return False  # Error checking user


@app.route("/create_user", methods=["GET", "POST"])
def create_user_route():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Call the function to create the user in the database (using database.py)
        if create_user(username, email, password):
            # If user creation is successful, redirect to the dashboard
            session['username'] = username
            return redirect('/dashboard')
        else:
            # If user creation fails, show an error message
            flash("Error creating user.", "error")

    return render_template("contact.html")



@app.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard.html", username=username)
    else:
        return redirect("/")

@app.route("/model.html", methods=["GET", "POST"])
def model():
    # Handle the GET request
    return render_template("model.html")


@app.route("/select", methods=["POST"])
def model_select():
    username = session["username"]
    chat_model = request.form.get("model")
    date = datetime.now()

    # Store the chat_model in the session
    session["chat_model"] = chat_model
    print(chat_model)

    # Insert the chat data into the database
    try:
        new_message = Chat(username=username, chat_model=chat_model, date=date)
        db.session.add(new_message)
        db.session.commit()
    except Exception as error:
        print(f"Error inserting chat data: {error}")

    return redirect("/chat")

@app.route("/chat")
def chat_ui():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run(port=5001)
