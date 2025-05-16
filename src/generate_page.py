import os

from copystatic import validate_directory_path
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


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    with open(os.path.join(dest_path, "index.html"), "w") as f:
        f.write(template)


def generate_pages_recursively(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    validate_directory_path(dir_path_content)

    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        source_item = os.path.join(dir_path_content, item)
        destination_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_item):
            if source_item.endswith(".md"):
                generate_page(source_item, template_path, dest_dir_path, basepath)
        elif os.path.isdir(source_item):
            generate_pages_recursively(
                source_item, template_path, destination_item, basepath
            )
