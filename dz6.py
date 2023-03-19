import os
import shutil

CATEGORIES = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'music': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}

KNOWN_EXTENSIONS = []
UNKNOWN_EXTENSIONS = []

def normalize(name):
    
    name = name.translate(str.maketrans('абвгдеёжзийклмнопрстуфхіыэюя', 
                                        'abvgdeejzijklmnoprstufhiyejya'))
    name = ''.join(c if c.isalnum() else '_' for c in name)
    return name

def sort_files(directory):
    global KNOWN_EXTENSIONS, UNKNOWN_EXTENSIONS
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
    
        if os.path.isdir(item_path):
            sort_files(item_path)
        else:
            
            _, ext = os.path.splitext(item)
            ext = ext[1:].upper()  
            KNOWN_EXTENSIONS.append(ext) 
           
            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                   
                    category_path = os.path.join(directory, category)
                    if not os.path.exists(category_path):
                        os.mkdir(category_path)
                
