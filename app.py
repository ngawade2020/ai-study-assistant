from flask import Flask, render_template, request
import os
import PyPDF2
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

chat_history = []


def generate_response(question):

    question = question.lower()

    if "python" in question:

        return """
Python is a powerful programming language.

Popular uses:
• AI & Machine Learning
• Web Development
• Automation
• Data Science
"""

    elif "ai" in question:

        return """
Artificial Intelligence enables machines to simulate human intelligence.

Main AI fields:
• Machine Learning
• NLP
• Robotics
• Computer Vision
"""

    elif "flask" in question:

        return """
Flask is a lightweight Python web framework.

Common uses:
• AI Apps
• APIs
• Dashboards
• Full-stack Web Apps
"""

    return f"""
You asked:

"{question}"

This is a simulated AI response.
"""


def summarize_text(text):

    words = text.split()

    summary = " ".join(words[:150])

    return summary + "..."


@app.route("/", methods=["GET", "POST"])
def home():

    global chat_history

    if request.method == "POST":

        # Chat Message

        question = request.form.get("question")

        if question and question.strip() != "":

            response = generate_response(question)

            current_time = datetime.now().strftime("%H:%M")

            chat_history.append({

                "question": question,

                "response": response,

                "time": current_time
            })

        # PDF Upload

        pdf_file = request.files.get("pdf_file")

        if pdf_file and pdf_file.filename != "":

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                pdf_file.filename
            )

            pdf_file.save(filepath)

            pdf_reader = PyPDF2.PdfReader(filepath)

            text = ""

            for page in pdf_reader.pages:

                extracted = page.extract_text()

                if extracted:

                    text += extracted

            summary = summarize_text(text)

            current_time = datetime.now().strftime("%H:%M")

            chat_history.append({

                "question":
                f"Uploaded PDF: {pdf_file.filename}",

                "response":
                f"AI Summary:\n\n{summary}",

                "time": current_time
            })

    return render_template(
        "index.html",
        chat_history=chat_history
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)