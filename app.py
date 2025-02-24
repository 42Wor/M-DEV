from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session, make_response
import json
import markdown
import os
from functools import wraps
import secrets
import datetime  # Import the datetime module
from datetime import timedelta  # Import timedelta from datetime module
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(minutes=30)

README_FOLDER = "templates/Project/projectmd"
ADMIN_PASSWORD = "'"

# --- Authentication Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
# --- End Authentication Decorator ---


# ... (rest of your existing routes: home, project, readme_page, static, com, Privacy, FAQs, Chat, submit_form, faq) ...



# --- Markdown Editor Routes ---
@app.route('/editor/<filename>', methods=['GET', 'POST'])
@login_required  # Protect the editor
def editor(filename):
    file_path = os.path.join(README_FOLDER, filename)
    print(f"Debug: Attempting to open file at path: {file_path}") # Debug 1: Check file path

    if request.method == 'POST':
        # ... (POST request handling - save logic - no need to change for now) ...
        pass # Keep your existing POST handling logic

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            print(f"Debug: Successfully read content from file.") # Debug 2: File read success
            print(f"Debug: First 50 chars of markdown_content: {markdown_content[:50]}") # Debug 3: Sample of content
    except FileNotFoundError:
        print(f"Debug: File not found at path: {file_path}") # Debug 4: File not found error
        return "File not found.", 404
    except Exception as e:
        print(f"Debug: Error reading file: {e}") # Debug 5: Other file reading errors
        return f"Error reading file: {e}", 500

    print(f"Debug: Rendering editor.html with filename: {filename}") # Debug 6: Before render template
    return render_template('Project/editor.html', filename=filename, markdown_content=markdown_content)
@app.route('/editor/new', methods=['GET', 'POST'])
@login_required # Protect new file creation too
def new_editor():
    if request.method == 'POST':
        filename = request.form['new_filename']
        if not filename.endswith(".md"):
            filename += ".md" # Ensure .md extension
        file_path = os.path.join(README_FOLDER, filename)

        if os.path.exists(file_path):
            return "File already exists.", 400 # Or handle differently

        markdown_content = request.form['markdown_content'] # Content for new file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            return redirect(url_for('readme_page', filename=os.path.splitext(filename)[0])) # Redirect to the new page
        except Exception as e:
            return f"Error creating file: {e}", 500

    return render_template('Project/editor.html', filename='new_file.md', markdown_content='') # Empty editor for new file


# --- Admin and Login ---
@app.route('/admin/')
@login_required
def admin():
    readme_files_base_names = []
    try:
        for filename in os.listdir(README_FOLDER):
            if filename.endswith(".md") or filename.endswith(".markdown"):
                base_name = os.path.splitext(filename)[0]
                readme_files_base_names.append(base_name)
    except FileNotFoundError:
        return f"Error: Folder '{README_FOLDER}' not found.", 404

    return render_template('admin/admin_panel.html', readme_files=readme_files_base_names)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('home')) # Or admin login page


# ---  File Deletion (Admin Feature) ---
@app.route('/admin/delete/<filename>')
@login_required
def admin_delete_file(filename):
    file_path = os.path.join(README_FOLDER, filename + ".md") # Ensure .md extension for deletion
    try:
        os.remove(file_path)
        return redirect(url_for('admin')) # Redirect back to admin panel
    except FileNotFoundError:
        return "File not found.", 404
    except Exception as e:
        return f"Error deleting file: {e}", 500

@app.route('/preview', methods=['POST'])
def preview_markdown():
    data = request.get_json()
    markdown_text = data.get('markdown', '')
    html_content = markdown.markdown(markdown_text)
    return jsonify({'html_content': html_content})

# Home Page
@app.route("/")
def home():
    resp = make_response(render_template("index.html")) # Create a response object
    now = datetime.datetime.now()
    resp.set_cookie('last_visit', now.strftime("%Y-%m-%d %H:%M:%S")) # Set the cookie
    return resp



@app.route("/project/")  # Main page route
def project():
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

# --- 404 Error Handler ---
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development
