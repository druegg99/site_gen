import os
import shutil
from text_func import *


def main():
    delete_public("./public/")
    generate_public("./static/", "./public/")
    generate_pages_recursive("./content/", "./template.html", "./public/")


def delete_public(path):
    if os.path.exists(path):
        print(f"Path: {path} already exists, deleting...")
        shutil.rmtree(path)
    else:
        print("Folder doesn't exist.")

def generate_public(path, dest):
    files = os.listdir(path)
    print("Files to copy:")
    print(files)
    os.mkdir(dest)
    print(f"Folder {dest} created")
    for file in files:
        filepath = os.path.join(path, file)
        print(f"Working on {filepath}")
        if os.path.isfile(filepath):
            shutil.copy(filepath, dest)
        else:
            generate_public(filepath, os.path.join(dest, file))

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.strip()[:2] == "# ":
            return line[2:]
    raise Exception("Header not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(markdown)
    print(f"title: {title}")

    html = markdown_to_html_node(markdown)
    html_string = html.to_html()
    titleless = template.replace("{{ Content }}", html_string)
    with_title = titleless.replace("{{ Title }}", title)
    if not os.path.exists(dest_path):
        os.mkdirs(dest_path)
    with open(os.path.join(dest_path, "index.html"), "x") as f:
        f.write(with_title)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    for file in files:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            if file[-3:] == ".md":
                generate_page(os.path.join(dir_path_content, file), template_path, dest_dir_path)
        else:
            os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))


main()
