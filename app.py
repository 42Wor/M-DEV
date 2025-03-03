''' =================================
   1. Imports and Configurations
   ================================= '''
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session, make_response, flash
import json
import markdown
import os
from functools import wraps
import secrets
import datetime  # Import the datetime module
from datetime import timedelta  # Import timedelta from datetime module
from werkzeug.utils import secure_filename # Import secure_filename
import google.generativeai as genai  # Import the Gemini API library

''' =================================
   2. Flask App Initialization and Secret Key
   ================================= '''
app = Flask(__name__)
app.secret_key = "secrets.token_hex(16)"
app.permanent_session_lifetime = timedelta(minutes=30)

''' =================================
   3. Project Settings and Constants
   ================================= '''
README_FOLDER = "templates/Project/projectmd"
README_FOLDER_ASSETS = os.path.join(README_FOLDER, "Assets") # Define Assets folder path
ADMIN_PASSWORD = "'"

# Ensure Assets folder exists
os.makedirs(README_FOLDER_ASSETS, exist_ok=True)

# Configure Gemini API (replace with your actual API key or environment variable)
# Option 1: Set API key directly (less secure - for testing only)
# genai.configure(api_key="YOUR_API_KEY")
genai.configure(api_key='AIzaSyACCG5jwizEchxEb3fnJlchzHY7HLp7QSw')

generation_config = genai.types.GenerationConfig(
    candidate_count=1,
    max_output_tokens=200, # Adjust as needed
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
   4. Authentication Decorator
   ================================= '''
# --- Authentication Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
# --- End Authentication Decorator ---


''' =================================
   5. Gemini API Functions
   ================================= '''

def generate_name_from_gemini(prompt_suffix="for a markdown file"):
    """Generates a name using Gemini API."""
    prompt = f"Generate a creative and concise name {prompt_suffix}.  Just return the name, no extra text."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error during name generation: {e}")
        return None

def generate_markdown_from_gemini(prompt_prefix, user_markdown_content=""):
    """Generates markdown content using Gemini API based on a prompt and optionally user content."""
    prompt = f"{prompt_prefix}\n\n---\n\nCurrent Markdown Content (optional context):\n{user_markdown_content}\n\n---\n\nGenerate Markdown content based on the above. 700 line first draft.  No extra text."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error during markdown generation: {e}")
        return None

''' =================================
   6. Markdown Editor Routes
   ================================= '''
@app.route('/editor/<filename>', methods=['GET', 'POST'])
@login_required  # Protect the editor (optional for scratch, add back later)
def editor(filename):
    file_path = os.path.join(README_FOLDER, filename)
    is_new_file = (filename == 'new_file.md') # Check if it's a new file

    if request.method == 'POST':
        action = request.form.get('action') # Get the action (save, save_as, generate_name, etc.)

        if action == 'generate_name': # --- Generate Name Request ---
            generated_name = generate_name_from_gemini()
            if generated_name:
                return jsonify({'generated_name': generated_name})
            else:
                return jsonify({'error': 'Failed to generate name.'}), 500

        elif action == 'generate_markdown': # --- Generate Markdown Request ---
            user_prompt_prefix = request.form.get('prompt_prefix', "Expand on this markdown content") # Get prompt prefix from form, default if missing
            # Get markdown_content only when needed for generate_markdown as context
            markdown_content = request.form.get('markdown_content', "") # Get it safely, default to empty string
            generated_markdown = generate_markdown_from_gemini(user_prompt_prefix, markdown_content)
            if generated_markdown:
                return jsonify({'generated_markdown': generated_markdown})
            else:
                return jsonify({'error': 'Failed to generate markdown.'}), 500


        elif action == 'save_as': # --- Save As Logic ---
            markdown_content = request.form['markdown_content'] # Get markdown_content for save actions
            new_filename_input = request.form.get('new_filename') # Get new filename from form
            if not new_filename_input:
                flash("Filename for 'Save As' is missing.", 'error')
                return redirect(url_for('editor', filename=filename)) # Stay on same editor page
            new_filename = secure_filename(new_filename_input) # Sanitize filename
            if not new_filename.endswith(".md"):
                new_filename += ".md"
            new_file_path = os.path.join(README_FOLDER, new_filename)

            if os.path.exists(new_file_path) and not is_new_file: # Prevent overwriting existing file (unless original was new_file.md)
                flash(f"File '{new_filename}' already exists. Choose a different name for 'Save As'.", 'error')
                return redirect(url_for('editor', filename=filename)) # Stay on same editor page


            try:
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                flash(f"File saved as '{new_filename}' successfully!", 'success')
                return redirect(url_for('editor', filename=new_filename)) # Redirect to editor for new file
            except Exception as e:
                flash(f"Error saving file: {e}", 'error')
                return f"Error saving file: {e}", 500

        elif action == 'save': # --- Regular Save Logic (action == 'save') ---
            markdown_content = request.form['markdown_content'] # Get markdown_content for save actions
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                flash('File saved successfully!', 'success')
                return redirect(url_for('editor', filename=filename)) # Redirect to reload editor
            except Exception as e:
                flash(f"Error saving file: {e}", 'error')
                return f"Error saving file: {e}", 500
        else:
            return "Invalid action", 400 # Handle unexpected actions


    # --- GET request (loading editor) remains the same ---
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        return "File not found.", 404
    except Exception as e:
        return f"Error reading file: {e}", 500

    return render_template('Project/editor.html', filename=filename, markdown_content=markdown_content)

@app.route('/editor/new', methods=['GET', 'POST'])
@login_required # Protect new file creation (optional for scratch, add back later)
def new_editor():
    if request.method == 'POST':
        filename = request.form['new_filename']
        if not filename.endswith(".md"):
            filename += ".md"
        file_path = os.path.join(README_FOLDER, filename)

        if os.path.exists(file_path):
            return "File already exists.", 400

        markdown_content = request.form['markdown_content']
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            return redirect(url_for('readme_page', filename=os.path.splitext(filename)[0])) # Redirect to new page
        except Exception as e:
            return f"Error creating file: {e}", 500

    return render_template('Project/editor.html', filename='new_file.md', markdown_content='')


@app.route('/preview', methods=['POST'])
def preview_markdown():
    data = request.get_json()
    markdown_text = data.get('markdown', '')
    html_content = markdown.markdown(markdown_text)
    return jsonify({'html_content': html_content})
# --- End Markdown Editor Routes ---

''' =================================
   7. Admin Panel and Login Routes
   ================================= '''
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
# --- End Admin and Login ---


''' =================================
   8. File Deletion Route (Admin Feature)
   ================================= '''
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
# --- End File Deletion Route ---

''' =================================
   9. Asset Management Routes (NEW)
   ================================= '''
# --- Asset Management ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'} # Allowed image extensions

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
        filename = secure_filename(file.filename) # Use secure_filename
        file_path = os.path.join(README_FOLDER_ASSETS, filename)
        try:
            file.save(file_path)
            return jsonify({'success': 'Image uploaded successfully', 'filename': filename})
        except Exception as e:
            return jsonify({'error': f'Error saving file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/list_assets')
@login_required
def list_assets():
    assets = []
    try:
        for filename in os.listdir(README_FOLDER_ASSETS):
            if allowed_file(filename): # Only list allowed image types
                assets.append(filename)
    except FileNotFoundError:
        return jsonify({'error': f'Assets folder not found: {README_FOLDER_ASSETS}'}), 404
    return jsonify({'assets': assets})
# --- End Asset Management ---
# In your app.py, after your existing static route (@app.route('/static/<path:filename>'))

@app.route('/templates_assets/<path:filename>')  # New route prefix - choose something distinct
def serve_templates_assets(filename):
    return send_from_directory(os.path.join('templates', 'Project', 'projectmd', 'Assets'), filename)


''' =================================
   10. Main Application Routes (Home, Project, Readme, Static)
   ================================= '''
# --- Main Application Routes ---
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
            # Enable the 'toc' extension to generate header IDs
            html_content = markdown.markdown(readme_content, extensions=['toc'])
            return render_template("Project/readme_page.html", readme_html=html_content, readme_filename=filename + ".md") # Keep .md in title for clarity if you want
    except FileNotFoundError:
        return "README file not found.", 404


# Optional: Serve static files (like CSS) if you use style.css
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
# --- End Main Application Routes ---


''' =================================
   11. Additional Pages (Portfolio, Privacy, FAQs, Chat, Form Submission)
   ================================= '''
# --- Additional Pages ---
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

@app.route("/syntax/")
def Syntax():
    return render_template("Project/Syntax-md.html")

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
# --- End Additional Pages ---


''' =================================
   12. Error Handling (404)
   ================================= '''
# --- 404 Error Handler ---
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
# --- End Error Handling ---


''' =================================
   13. Main Execution Block
   ================================= '''
# --- Main Execution Block ---
if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development
# --- End Main Execution Block ---