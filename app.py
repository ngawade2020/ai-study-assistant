from flask import Flask, render_template, request

app = Flask(__name__)

def generate_response(question):

    question = question.lower()

    if "python" in question:
        return "Python is a powerful programming language."

    elif "ai" in question:
        return "Artificial Intelligence allows machines to learn and make decisions."

    elif "flask" in question:
        return "Flask is a lightweight Python web framework."

    else:
        return "Interesting question! I am still learning."

@app.route("/", methods=["GET", "POST"])
def home():

    response = ""

    if request.method == "POST":

        question = request.form["question"]

        response = generate_response(question)

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)