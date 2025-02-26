CSS_DIR = static/Project
EDITOR_CSS = $(CSS_DIR)/editor.css
PREVIEW_CSS = $(CSS_DIR)/Preview.css
MINIFIED_PREVIEW_CSS = $(CSS_DIR)/Preview.min.css # Output minified Preview CSS
MINIFIED_EDITOR_CSS = $(CSS_DIR)/editor.min.css   # Output minified Editor CSS
PYTHON_SCRIPT = minify_css.py                      # Path to your Python script

all: $(MINIFIED_PREVIEW_CSS) $(MINIFIED_EDITOR_CSS)

$(MINIFIED_PREVIEW_CSS): $(PREVIEW_CSS) $(PYTHON_SCRIPT)
	python $(PYTHON_SCRIPT) $< $@

$(MINIFIED_EDITOR_CSS): $(EDITOR_CSS) $(PYTHON_SCRIPT)
	python $(PYTHON_SCRIPT) $< $@

minify_css: $(MINIFIED_PREVIEW_CSS) $(MINIFIED_EDITOR_CSS) # Target to minify both

clean:
	rm -f $(MINIFIED_PREVIEW_CSS) $(MINIFIED_EDITOR_CSS)

.PHONY: all clean minify_css