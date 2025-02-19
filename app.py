from flask import Flask, render_template, request, jsonify
import json
import markdown
import os
app = Flask(__name__)

README_FOLDER = "templates/Project/projectmd"


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Project/")  # Main page route
def Project():
    readme_files_base_names = []  # Store base filenames (without .md)
    try:
        for filename in os.listdir(README_FOLDER):
            if filename.endswith(".md") or filename.endswith(".markdown"):
                base_name = os.path.splitext(filename)[0]  # Remove extension
                readme_files_base_names.append(base_name)
    except FileNotFoundError:
        return f"Error: Folder '{README_FOLDER}' not found.", 404

    print("Debug: readme_files_base_names =", readme_files_base_names)  # ADD THIS LINE
    return render_template("Project/index.html", readme_files=readme_files_base_names)



@app.route('/readme/<filename>')  # Route expects filename without .md extension
def readme_page(filename):
    readme_path = os.path.join(README_FOLDER, filename + ".md") # Add .md extension here
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            html_content = markdown.markdown(readme_content)
            return render_template("Project/readme_page.html", readme_html=html_content, readme_filename=filename + ".md") # Keep .md in title for clarity if you want
    except FileNotFoundError:
        return "README file not found.", 404


# Optional: Serve static files (like CSS) if you use style.css
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


# Portfolio Page
@app.route("/com/")
def portfolio():
    return render_template("com/index.html")


# Privacy Page
@app.route("/Privacy/")
def privacy():
    return render_template("Privacy/index.html")


# FAQs Page
@app.route("/FAQs/")
def faqs():
    return render_template("FAQs/index.html")


# Chat Page - using com/index.html as template
@app.route("/Chat/")
def Chat():
    return render_template("com/index.html")


# Form Submission Route
@app.route("/submit_form", methods=["POST"])
def submit_form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        print("Form Data:")
        print("Name:", name)
        print("Email:", email)
        print("Message:", message)
        # Here you can add code to save the data to a database,
        # send an email, or perform other actions with the form data.
        return render_template("com/index.html")  # Or redirect to a thank you page


@app.route("/faq")
def faq():
    with open("static/FAQs/faq.json") as f:
        faq_data = json.load(f)
    return jsonify(faq_data)


if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development
