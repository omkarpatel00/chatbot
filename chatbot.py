from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Load data from file
def load_data(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

def parse_data(data):
    entries = re.split(r'\n\n', data)
    members = []
    for entry in entries:
        member = {}
        lines = entry.split('\n')
        for line in lines:
            key, value = line.split(': ')
            member[key.strip()] = value.strip()
        members.append(member)
    return members

data_file = 'mydata.txt'
data = load_data(data_file)
members = parse_data(data)

# Basic greeting responses
greeting_responses = ["Hello! How can I help you today?", "Hi there! What can I assist you with?", "Hey! How can I assist you today?"]

# Function to get response from the bot
def get_bot_response(user_text):
    user_text = user_text.lower()
    if user_text in ['hi', 'hello', 'hey']:
        return greeting_responses[0]  # Return a random greeting response
    elif 'who is' in user_text:
        person = user_text.split('who is ')[-1].strip()
        for member in members:
            if person.lower() == member.get('name', '').lower():
                return f"{member['name']}, {member['position']}"
        return f"I am sorry! I don't have information on that person."
    else:
        return "I am sorry! I don't understand you."

# Route to render index.html template
@app.route('/')
def home():
    return render_template("index.html")

# Route to handle chatbot interaction
@app.route('/get')
def get_bot_response_route():
    user_text = request.args.get('msg')
    bot_response = get_bot_response(user_text)
    return str(bot_response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

