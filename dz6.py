import os
import shutil
import zipfile

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

def move_file(src_path, dst_path):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    shutil.move(src_path, dst_path)

def remove_empty_directories(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            remove_empty_directories(item_path)
            if not os.listdir(item_path):
                os.rmdir(item_path)

def extract_archive(archive_path, dst_path):
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(dst_path)

def sort_files(directory):
    global KNOWN_EXTENSIONS, UNKNOWN_EXTENSIONS
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
    
        if os.path.isdir(item_path):
            sort_files(item_path)
            if not os.listdir(item_path):
                os.rmdir(item_path)
        else:
            _, ext = os.path.splitext(item)
            ext = ext[1:].upper()  
            KNOWN_EXTENSIONS.append(ext) 
           
            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                    category_path = os.path.join(directory, category)
                    move_file(item_path, category_path)
                    if ext == 'ZIP':
                        extract_archive(os.path.join(category_path, item), category_path)
    remove_empty_directories(directory)
