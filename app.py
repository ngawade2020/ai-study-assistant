from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

chat_history = []

def generate_response(question):

    question = question.lower()

    responses = {

        "python":
        """
Python is a powerful programming language used in:
- AI
- Web Development
- Automation
- Data Science
        """,

        "ai":
        """
Artificial Intelligence allows machines to simulate human intelligence.

Major AI fields:
- Machine Learning
- NLP
- Robotics
- Computer Vision
        """,

        "flask":
        """
Flask is a lightweight Python web framework used for web applications.
        """
    }

    for key in responses:

        if key in question:
            return responses[key]

    return "Interesting question! I am still learning."

def summarize_text(text):

    words = text.split()

    summary = " ".join(words[:100])

    return summary + "..."

@app.route("/", methods=["GET", "POST"])
def home():

    global chat_history

    if request.method == "POST":

        # Text Question
        if "question" in request.form:

            question = request.form["question"]

            response = generate_response(question)

            chat_history.append({
                "question": question,
                "response": response
            })

        # PDF Upload
        if "pdf_file" in request.files:

            pdf_file = request.files["pdf_file"]

            if pdf_file.filename != "":

                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    pdf_file.filename
                )

                pdf_file.save(filepath)

                pdf_reader = PyPDF2.PdfReader(filepath)

                text = ""

                for page in pdf_reader.pages:
                    text += page.extract_text()

                summary = summarize_text(text)

                chat_history.append({
                    "question": f"Uploaded PDF: {pdf_file.filename}",
                    "response": f"Summary:\n\n{summary}"
                })

    return render_template(
        "index.html",
        chat_history=chat_history
    )

if __name__ == "__main__":
    app.run(debug=True)