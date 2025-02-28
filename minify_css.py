# minify_css.py
import cssmin
import sys
import argparse
import logging

def minify_css(input_file, output_file):
    """Minifies a CSS file using cssmin."""
    try:
        with open(input_file, 'r') as f_in:
            css_content = f_in.read()
        minified_css = cssmin.cssmin(css_content)
        with open(output_file, 'w') as f_out:
            f_out.write(minified_css)
        logging.info(f"Successfully minified '{input_file}' to '{output_file}'")
    except FileNotFoundError:
        logging.error(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Minify a CSS file.")
    parser.add_argument("input_css_file", help="The input CSS file to be minified.")
    parser.add_argument("output_css_file", help="The output file for the minified CSS.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    minify_css(args.input_css_file, args.output_css_file)

if __name__ == "__main__":
    main()