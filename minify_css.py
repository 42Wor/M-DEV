# minify_css.py
import cssmin
import sys

def minify_css(input_file, output_file):
    """Minifies a CSS file using cssmin."""
    try:
        with open(input_file, 'r') as f_in:
            css_content = f_in.read()
        minified_css = cssmin.cssmin(css_content)
        with open(output_file, 'w') as f_out:
            f_out.write(minified_css)
        print(f"Successfully minified '{input_file}' to '{output_file}'")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python minify_css.py <input_css_file> <output_css_file>")
        sys.exit(1)
    input_css = sys.argv[1]
    output_css = sys.argv[2]
    minify_css(input_css, output_css)