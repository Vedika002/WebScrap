import json
import importlib
import os
import sys
import scraping_scripts
user_input = '1'

def main():
    sys.path.append('D:\\web_scrap')
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
   
    if user_input in data:
        selected_entry = data[user_input]
        url = selected_entry['url']
        script = selected_entry['script_name']
        print(f"Selected URL: {url}")
        print(f"Associated Script: {script}")
    
        try:
            module = importlib.import_module(f"scraping_scripts.{script.replace('.py', '')}")
            print(module)
            if hasattr(module, 'run') and callable(getattr(module, 'run')):
                module.run(url, selected_entry)  
            else:
                print(f"Error: Script {script} does not have a 'run' function.")
        except ImportError:
            print(f"Error: Script {script} not found.")

if __name__ == "__main__":
    main()
   