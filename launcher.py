import os
import importlib
import importlib.util


FILTERS_DIR = './filters'

def list_filter_files():
    """Lists Python files in the filters directory that start with 'FILTER_'."""
    filter_files = [
        f for f in os.listdir(FILTERS_DIR)
        if f.startswith('FILTER_') and f.endswith('.py')
    ]
    return filter_files

def display_filters(filter_files):
    """Displays the available filters for the user to select."""
    print("Available filters:")
    for idx, filter_file in enumerate(filter_files):
        print(f"{idx} = {filter_file.replace('.py', '')}")

def prompt_user_choice(filter_files):
    """Prompts the user to choose a filter by index."""
    try:
        choice = int(input("Choose a filter by number: "))
        if 0 <= choice < len(filter_files):
            return filter_files[choice]
        else:
            print("Invalid choice. Please choose a valid index.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def import_filter(filter_file):
    """Dynamically imports the selected filter module."""
    module_name = filter_file.replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(FILTERS_DIR, filter_file))
    filter_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(filter_module)
    return filter_module

def main():
    filter_files = list_filter_files()
    if not filter_files:
        print("No filters found in the directory.")
        return

    display_filters(filter_files)
    chosen_filter_file = prompt_user_choice(filter_files)

    if chosen_filter_file:
        print(f"Importing filter: {chosen_filter_file}")
        filter_module = import_filter(chosen_filter_file)
        filter_module.main()

if __name__ == "__main__":
    main()
