from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route('/')
def home():
    return "Hello World"

@app.route('/query', methods=['POST'])
def query():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        return jsonify({'error': 'OpenAI Key is not set'}), 500

    agent = create_csv_agent(OpenAI(temperature=0), "./AAPL.csv")
    user_question = request.form.get('query')

    if user_question is None or user_question == "":
        return jsonify({'error': 'No query provided'}), 400

    ans = agent.run(user_question)
    return jsonify({'answer': ans}), 200

if __name__ == '__main__':
    app.run()
