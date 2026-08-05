from flask import Flask, render_template
from crud import get_all_tickets

app = Flask(__name__)


@app.route("/")
def index():
    """
    Display all support tickets.
    """

    tickets = get_all_tickets()

    return render_template(
        "index.html",
        tickets=tickets
    )


if __name__ == "__main__":
    app.run(debug=True)
