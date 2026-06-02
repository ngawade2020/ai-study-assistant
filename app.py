from flask import Flask, render_template, request

app = Flask(__name__)

chat_history = []

def generate_response(question):

    question = question.lower()

    responses = {

        "python":
        """
Python is a powerful and beginner-friendly programming language.

It is widely used in:
- AI/ML
- Web Development
- Automation
- Data Science
        """,

        "ai":
        """
Artificial Intelligence enables machines to simulate human intelligence.

Major AI fields:
- Machine Learning
- NLP
- Computer Vision
- Robotics
        """,

        "flask":
        """
Flask is a lightweight Python web framework.

It is commonly used for:
- APIs
- AI apps
- Dashboards
- Web applications
        """
    }

    for key in responses:

        if key in question:
            return responses[key]

    return """
I am still learning.

Try asking about:
- Python
- AI
- Flask
"""

@app.route("/", methods=["GET", "POST"])
def home():

    global chat_history

    if request.method == "POST":

        question = request.form["question"]

        response = generate_response(question)

        chat_history.append({
            "question": question,
            "response": response
        })

    return render_template(
        "index.html",
        chat_history=chat_history
    )

if __name__ == "__main__":
    app.run(debug=True)