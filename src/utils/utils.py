from urllib.parse import urljoin
import csv
import os
def absolute_url(base_url:str,relative_url:str) -> str:
    return urljoin(base_url, relative_url)

def extract_number(text):
    
    try:
        start = text.find('(')
        if start == -1:
            return 0
        
        end = text.find(' ', start)
        
        if end == -1:
            return 0
        
        number_in_str = text[start + 1:end]
        
        return int(number_in_str)
    except (ValueError, IndexError) as e:
        print(f"Error extracting number: {e}")
        return -1

def save_list_to_csv(filename, data_list):
    
    current_script_dir = os.path.dirname(os.path.abspath( __file__ ))
    
    project_dir = os.path.dirname(current_script_dir)
    
    data_folder = os.path.join(project_dir, 'data')
    
    os.makedirs(data_folder, exist_ok = True)
    
    file_path = os.path.join(data_folder, filename)
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_list)

