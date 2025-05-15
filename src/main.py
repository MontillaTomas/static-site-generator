from copystatic import replace_content
from generate_page import generate_page


def main():
    replace_content("static/", "public/")
    print("Content replaced successfully.")
    generate_page("content/index.md", "template.html", "public/")


if __name__ == "__main__":
    main()
