from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from ice_breaker import ice_break_with


app = Flask(__name__)


@app.route("/")
def index():
    """Render the main index page.

    Returns:
        str: Rendered HTML template for the index page.
    """
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    """Process a person's name and generate ice breaker information.

    Accepts a POST request with a 'name' form parameter, then generates
    a summary, interests, ice breakers, and profile picture URL.

    Returns:
        dict: JSON response containing summary_and_facts, interests,
              ice_breakers, and picture_url.
    """
    name = request.form["name"]
    summary_and_facts, interests, ice_breakers, profile_pic_url = ice_break_with(
        name=name
    )
    return jsonify(
        {
            "summary_and_facts": summary_and_facts.to_dict(),
            "interests": interests.to_dict(),
            "ice_breakers": ice_breakers.to_dict(),
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)
