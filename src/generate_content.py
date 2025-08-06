import os
from block_markdown import markdown_to_html_node, extract_title
from pathlib import Path

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path, "r", encoding='utf-8') as f:
            markdown = f.read()
        #make html node from markdown and then extract title
        html_node = markdown_to_html_node(markdown)
        title = extract_title(markdown)

        #make html from node
        html = html_node.to_html()

        with open(template_path, "r", encoding='utf-8') as f:
            template = f.read()
        #Replace template title with actual title
        titled_page = template.replace("{{ Title }}", title)
        #Replace content with content from html
        full_page = titled_page.replace("{{ Content }}", html)
        href_replaced = full_page.replace("href=\"/", f"href=\"{basepath}")
        src_replaced = href_replaced.replace("src=\"/", f"src=\"{basepath}")

        #prepare destination directory
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)

        #write content to directory
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(src_replaced)

    except Exception as e:
        raise Exception(f"Error: {e} while generating page at {from_path}") 
    
def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    try:
        for filename in os.listdir(dir_path_content):
            from_path = os.path.join(dir_path_content, filename)
            dest_path = os.path.join(dest_dir_path, filename)
            #If content is a file, generate page
            if os.path.isfile(from_path):
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(basepath, from_path, template_path, dest_path)
            else:
                generate_pages_recursive(basepath, from_path, template_path, dest_path)
    except Exception as e:
        raise Exception(f"Error: {e} while generating pages")