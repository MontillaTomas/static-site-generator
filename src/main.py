import sys

from copystatic import replace_content
from generate_page import generate_pages_recursively


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    replace_content("static/", "docs/")
    print("Content replaced successfully.")
    generate_pages_recursively("content/", "template.html", "docs/", basepath)


if __name__ == "__main__":
    main()
