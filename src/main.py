from copystatic import replace_content
from generate_page import generate_pages_recursively


def main():
    replace_content("static/", "public/")
    print("Content replaced successfully.")
    generate_pages_recursively("content/", "template.html", "public/")


if __name__ == "__main__":
    main()
