<!--<main>
    <h2>{% if filename == 'new_file.md' %}Create New File{% else %}Editing: {{ filename }}{% endif %}</h2>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="flash-messages">
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <form method="POST">  <!-- FORM tag START here, enclosing form-actions -->
        <div class="form-actions">
            <button type="submit" class="save-button">Save</button>
            <a href="{{ url_for('readme_page', filename=filename.replace('.md', '')) }}" class="view-page-button">View Page</a>
            <a href="{{ url_for('admin') }}" class="admin-button">Admin Panel</a>
        </div>


        <input type="hidden" name="action" id="action" value="save"> <!-- Hidden input for action type - default is 'save' -->

        {% if filename == 'new_file.md' %}
            <div class="form-group">
                <label for="new_filename">New Filename (without .md extension):</label>
            <input type="text" class="form-control" id="new_filename" name="new_filename" required placeholder="Enter filename">
        </div>
        {% endif %}

        <div class="form-group">
            <div class="form-check">
                <input type="checkbox" class="form-check-input" id="save_as_new" name="save_as_new">
                <label class="form-check-label" for="save_as_new">Save As New File</label>
            </div>
        </div>

        <div id="new_filename_group" class="form-group" style="display: none;"> <!-- Initially hidden -->
            <label for="new_filename_save_as">New Filename (for Save As):</label>
            <input type="text" class="form-control" id="new_filename_save_as" name="new_filename_save_as" placeholder="Enter new filename">
        </div>


        <div class="editor-container">
            <div class="editor-pane">
                <textarea id="markdown-editor" name="markdown_content" class="form-control editor-textarea" placeholder="Write your Markdown here...">{{ markdown_content|e }}</textarea>
            </div>
            <div class="preview-pane">
                <h2>Preview</h2>
                <div id="markdown-preview" class="preview-content">
                    <!-- Preview will be loaded here by JavaScript -->
                </div>
            </div>
        </div>
    </form>  <!-- FORM tag END here, after all form elements -->
</main>-->