from flask.__init__ import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
import os
from datetime import timedelta

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=30)


@app.route("/")
def home():
    return render_template(
        "index.html",
    )


if __name__ == "__main__":
    app.run(debug=True)
