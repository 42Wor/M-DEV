from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session, make_response, flash
import json
import markdown
import os
from functools import wraps
import secrets
from datetime import timedelta
from werkzeug.utils import secure_filename
import google.generativeai as genai
import datetime
''' =================================
   1. Initialization and Configurations
   ================================= '''
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Using secrets for the secret key.
app.permanent_session_lifetime = timedelta(minutes=30)

''' =================================
   2. Project Settings and Constants
   ================================= '''
README_FOLDER = "templates/Project/projectmd"
README_FOLDER_ASSETS = os.path.join(README_FOLDER, "Assets")
ADMIN_PASSWORD = "'"  #  REPLACE WITH A STRONG PASSWORD!

# Ensure the base README_FOLDER and Assets folder exists
os.makedirs(README_FOLDER, exist_ok=True)
os.makedirs(README_FOLDER_ASSETS, exist_ok=True)

# Gemini API configuration
genai.configure(api_key='AIzaSyACCG5jwizEchxEb3fnJlchzHY7HLp7QSw') #REPLACE WITH YOUR API KEY

generation_config = genai.types.GenerationConfig(
    candidate_count=1,
    max_output_tokens=1500,
)
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

''' =================================
   3. Authentication Decorator
   ================================= '''

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

''' =================================
   4. Gemini API Functions
   ================================= '''

def generate_name_from_gemini(prompt_suffix="for a markdown file"):
    """Generates a name using Gemini API."""
    prompt = f"Generate a creative and concise name {prompt_suffix}. Just return the name in lowercase, no extra text."
    try:
        response = model.generate_content(prompt)
        # Convert to lowercase and replace spaces with hyphens
        return response.text.strip().lower().replace(" ", "-")
    except Exception as e:
        print(f"Gemini API error during name generation: {e}")
        return None

def generate_markdown_from_gemini(prompt_prefix, user_markdown_content=""):
    """Generates markdown content using Gemini API based on a prompt and optionally user content."""
    prompt = f"{prompt_prefix}\n\n---\n\nCurrent Markdown Content (optional context):\n{user_markdown_content}\n\n---\n\nGenerate Markdown content based on the above."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error during markdown generation: {e}")
        return None

''' =================================
   5. Markdown Editor Routes
   ================================= '''

@app.route('/editor/<category>/<filename>', methods=['GET', 'POST'])
@login_required
def editor(category, filename):
    file_path = os.path.join(README_FOLDER, category, filename)
    is_new_file = (filename == 'new_file.md')

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'generate_name':
            generated_name = generate_name_from_gemini()
            if generated_name:
                return jsonify({'generated_name': generated_name})
            else:
                return jsonify({'error': 'Failed to generate name.'}), 500

        elif action == 'generate_markdown':
            user_prompt_prefix = request.form.get('prompt_prefix', "Expand on this markdown content")
            markdown_content = request.form.get('markdown_content', "")
            generated_markdown = generate_markdown_from_gemini(user_prompt_prefix, markdown_content)
            if generated_markdown:
                return jsonify({'generated_markdown': generated_markdown})
            else:
                return jsonify({'error': 'Failed to generate markdown.'}), 500

        elif action == 'save_as':
            markdown_content = request.form['markdown_content']
            new_filename_input = request.form.get('new_filename')
            if not new_filename_input:
                flash("Filename for 'Save As' is missing.", 'error')
                return redirect(url_for('editor', category=category, filename=filename))  # Keep category
            new_filename = secure_filename(new_filename_input)
            if not new_filename.endswith(".md"):
                new_filename += ".md"

            # Get category for new file, default to current if not provided
            new_category = request.form.get('new_category', category)
            new_file_path = os.path.join(README_FOLDER, new_category, new_filename)

            # Ensure the new category directory exists
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            if os.path.exists(new_file_path) and not is_new_file:
                flash(f"File '{new_filename}' already exists.  Choose a different name for 'Save As'.", 'error')
                return redirect(url_for('editor', category=category, filename=filename))

            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            flash(f"File saved as '{new_filename}' successfully!", 'success')
            return redirect(url_for('editor', category=new_category, filename=new_filename))

        elif action == 'save':
            markdown_content = request.form['markdown_content']
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            flash('File saved successfully!', 'success')
            return redirect(url_for('editor', category=category, filename=filename))
        else:
            return "Invalid action", 400

    # --- GET request (loading editor) ---
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        return "File not found.", 404

    return render_template('Project/editor.html', category=category, filename=filename, markdown_content=markdown_content)

@app.route('/editor/new', methods=['GET', 'POST'])
@login_required
def new_editor():
    if request.method == 'POST':
        filename = request.form['new_filename']
        category = request.form.get('new_category', 'default')  # Get category, default to 'default'

        if not filename.endswith(".md"):
            filename += ".md"

        file_path = os.path.join(README_FOLDER, category, filename)

        # Ensure the category directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if os.path.exists(file_path):
            return "File already exists.", 400

        markdown_content = request.form['markdown_content']
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        return redirect(url_for('readme_page', category=category, filename=os.path.splitext(filename)[0]))

    return render_template('Project/editor.html', filename='new_file.md', category='default', markdown_content='')  # Pass default category

@app.route('/preview', methods=['POST'])
def preview_markdown():
    data = request.get_json()
    markdown_text = data.get('markdown', '')
    html_content = markdown.markdown(markdown_text)
    return jsonify({'html_content': html_content})

''' =================================
   6. Admin Panel and Login Routes
   ================================= '''

@app.route('/admin/')
@login_required
def admin():
    readme_files_by_category = {}  # Dictionary to store files by category
    try:
        for category in os.listdir(README_FOLDER):
            category_path = os.path.join(README_FOLDER, category)
            if os.path.isdir(category_path) and category != "Assets":
                readme_files_by_category[category] = []  # Initialize list for the category
                for filename in os.listdir(category_path):
                    if filename.endswith((".md", ".markdown")):
                        base_name = os.path.splitext(filename)[0]
                        readme_files_by_category[category].append(base_name)
    except FileNotFoundError:
        return f"Error: Folder '{README_FOLDER}' not found.", 404

    return render_template('admin/admin_panel.html', readme_files_by_category=readme_files_by_category)

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
    return redirect(url_for('home'))

''' =================================
   7. File Deletion Route
   ================================= '''

@app.route('/admin/delete/<category>/<filename>')
@login_required
def admin_delete_file(category, filename):
    file_path = os.path.join(README_FOLDER, category, filename + ".md")
    try:
        os.remove(file_path)
        return redirect(url_for('admin'))
    except FileNotFoundError:
        return "File not found.", 404
    except Exception as e:
        return f"Error deleting file: {e}", 500

''' =================================
   8. Asset Management Routes
   ================================= '''

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(README_FOLDER_ASSETS, filename)
        file.save(file_path)
        return jsonify({'success': 'Image uploaded successfully', 'filename': filename})
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/list_assets')
@login_required
def list_assets():
    assets = []
    for filename in os.listdir(README_FOLDER_ASSETS):
        if allowed_file(filename):
            assets.append(filename)
    return jsonify({'assets': assets})

@app.route('/templates_assets/<path:filename>')
def serve_templates_assets(filename):
    return send_from_directory(os.path.join('templates', 'Project', 'projectmd', 'Assets'), filename)

''' =================================
   9. Main Application Routes
   ================================= '''

@app.route("/")
def home():
    resp = make_response(render_template("index.html"))
    now = datetime.datetime.now()
    resp.set_cookie('last_visit', now.strftime("%Y-%m-%d %H:%M:%S"))
    return resp

@app.route("/project/")
def project():
    readme_files_by_category = {} # Dictionary to store files by category
    try:
        for category in os.listdir(README_FOLDER):
            category_path = os.path.join(README_FOLDER, category)
            if os.path.isdir(category_path) and category != "Assets":
                readme_files_by_category[category] = [] # Initialize list for the category
                for filename in os.listdir(category_path):
                    if filename.endswith((".md",".markdown")):
                        base_name = os.path.splitext(filename)[0]
                        readme_files_by_category[category].append(base_name)

    except FileNotFoundError:
        return f"Error: Folder '{README_FOLDER}' not found.", 404

    return render_template("Project/index.html", readme_files_by_category=readme_files_by_category)

@app.route('/readme/<category>/<filename>')
def readme_page(category, filename):
    readme_path = os.path.join(README_FOLDER, category, filename + ".md")
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            html_content = markdown.markdown(readme_content, extensions=['toc'])
            return render_template("Project/readme_page.html", readme_html=html_content, readme_filename=f"{category}/{filename}.md")
    except FileNotFoundError:
        return "README file not found.", 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

''' =================================
   10. Additional Pages
   ================================= '''

@app.route("/com/")
def portfolio():
    return render_template("com/index.html")

@app.route("/Privacy/")
def privacy():
    return render_template("Privacy/index.html")

@app.route("/FAQs/")
def faqs():
    return render_template("FAQs/index.html")

@app.route("/Chat/")
def Chat():
    return render_template("com/index.html")

@app.route("/syntax/")
def Syntax():
    return render_template("Project/Syntax-md.html")

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
        return render_template("com/index.html")

@app.route("/faq")
def faq():
    with open("static/FAQs/faq.json") as f:
        faq_data = json.load(f)
    return jsonify(faq_data)

''' =================================
   11. Error Handling
   ================================= '''

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

''' =================================
   12. Main Execution Block
   ================================= '''

if __name__ == "__main__":
    app.run(debug=True)