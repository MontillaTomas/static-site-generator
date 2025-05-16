from copystatic import replace_content
from generate_page import generate_page


def main():
    replace_content("static/", "public/")
    print("Content replaced successfully.")
    generate_page("content/index.md", "template.html", "public/")
    generate_page("content/contact/index.md", "template.html", "public/contact/")
    generate_page(
        "content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/"
    )
    generate_page(
        "content/blog/majesty/index.md", "template.html", "public/blog/majesty/"
    )
    generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/")


if __name__ == "__main__":
    main()
