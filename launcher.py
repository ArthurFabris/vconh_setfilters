import os
import importlib.util
import sys

# Step 1: Add the filters directory to sys.path
filters_path = os.path.join(os.path.dirname(__file__), 'filters')
if filters_path not in sys.path:
    sys.path.append(filters_path)

# Step 2: List Python files in the /filters folder
def list_filters():
    filter_modules = []
    
    for file in os.listdir(filters_path):
        if file.endswith('.py') and file != '__init__.py':  # Ignore __init__.py
            module_name = file[:-3]  # Strip the '.py' from the module name
            filter_modules.append(module_name)
    
    return filter_modules

# Step 3: Dynamically import and load the modules
def import_module(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"Module {module_name} not found")
        return None
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Step 4: Try to run the main function of the module
def run_module_main(module):
    if hasattr(module, 'main') and callable(getattr(module, 'main')):
        print(f"Running {module.__name__}.main()...")
        module.main()
    else:
        print(f"The module {module.__name__} has no callable main() function.")

# Launcher logic to list and load modules
if __name__ == '__main__':
    filters = list_filters()
    
    print("Efeitos disponíveis:")
    for f in filters:
        print(f)
    
    # Optionally import a specific module and run its main function
    chosen_module = input("Enter the module to load: ")
    if chosen_module in filters:
        mod = import_module(chosen_module)
        if mod:
            print(f"Loaded module: {chosen_module}")
            run_module_main(mod)  # Run the main function if it exists
    else:
        print(f"Module {chosen_module} not found.")
