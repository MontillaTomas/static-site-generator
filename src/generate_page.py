import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    title = None
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if title is None:
        raise ValueError("No title found in the markdown content.")
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    with open(os.path.join(dest_path, "index.html"), "w") as f:
        f.write(template)
