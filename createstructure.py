import os

def generate_file_structure_md(root_dir='.', output_file='structurefiles.md'):
    """
    Generates a Markdown file with the directory structure and content of Python files.

    Args:
        root_dir (str): The root directory to start from. Defaults to the current directory.
        output_file (str): The name of the output Markdown file. Defaults to 'structurefiles.md'.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # First, write the file structure
            f.write("# File Structure\n\n")
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # To ignore hidden directories like .git, .idea, etc. and venv folders
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and 'venv' not in d]
                
                # Normalize path to handle both Windows and Unix-like systems
                normalized_dirpath = os.path.normpath(dirpath)
                level = normalized_dirpath.replace(root_dir, '').count(os.sep)
                
                # Indent based on the directory level
                indent = ' ' * 4 * (level)
                
                # To handle the root directory properly
                if dirpath == root_dir:
                    f.write(f"- {os.path.basename(root_dir)}/\n")
                else:
                    f.write(f"{indent}- {os.path.basename(dirpath)}/\n")
                
                sub_indent = ' ' * 4 * (level + 1)
                for filename in filenames:
                    f.write(f"{sub_indent}- {filename}\n")

            # Then, write the content of each Python file
            f.write("\n# Python Files Content\n")
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Again, ignore hidden directories and venv
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and 'venv' not in d]

                for filename in filenames:
                    if filename.endswith('.py'):
                        file_path = os.path.join(dirpath, filename)
                        # Use a relative path for cleaner output
                        relative_path = os.path.relpath(file_path, root_dir)
                        
                        f.write(f"\n---\n\n")
                        f.write(f"### `{relative_path}`\n\n")
                        f.write("```python\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as py_file:
                                content = py_file.read()
                                # Prevent empty file content from breaking markdown
                                if not content.strip():
                                    f.write("# This file is empty.\n")
                                else:
                                    f.write(content)
                        except Exception as e:
                            f.write(f"# Error reading file: {e}")
                        f.write("\n```\n")
        
        print(f"Successfully generated '{output_file}' in the current directory.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    # Run the function in the current directory where the script is executed
    current_directory = os.getcwd()
    generate_file_structure_md(current_directory)