import sys
from file_handling import clean_directory, copy_files_recursive
from generate_content import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    args = sys.argv
    if len(args) == 2:
        basepath = args[1]
    else:
        print("Basepath not provided, defaulting to /")
        basepath = "/"
    
    clean_directory(dir_path_public)
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(basepath, dir_path_content, template_path, dir_path_public)

if __name__ == "__main__":
    main()