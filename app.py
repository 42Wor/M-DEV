from flask import Flask, render_template, request

app = Flask(__name__)


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Project Page
@app.route("/Project/")
def project():
    return render_template("Project/index.html")


# Python Project Page
@app.route("/Project/python/")
def python_project():
    return render_template("Project/python/index.html")


# Neural Networks Project Page
@app.route("/Project/Neural_Networks/")
def neural_project():
    return render_template("Project/Neural_Networks(MNIST)/index.html")


# 3D Scatter Plot Generator Page
@app.route("/Project/3D_Scatter_Plot/")
def scatter_plot():
    return render_template("Project/3D Scatter Plot Generator/index.html")


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
@app.route("/submit_form", methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print("Form Data:")
        print("Name:", name)
        print("Email:", email)
        print("Message:", message)
        # Here you can add code to save the data to a database,
        # send an email, or perform other actions with the form data.
        return render_template("com/index.html") # Or redirect to a thank you page

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development