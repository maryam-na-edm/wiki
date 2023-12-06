import re
import markdown2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    """
    Returns a list of all names of valid encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    
    entries = [re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")]
    
    valid_entries = [entry for entry in entries if get_entry(entry)]
    
    return list(sorted(valid_entries))


def save_entry(title, content):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def delete_entry(title):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)


def get_entry(title):
    try:
        with default_storage.open(f"entries/{title}.md", 'rb') as f:
            try:
                content = f.read().decode("utf-8")
            except UnicodeDecodeError:
                content = f.read().decode("latin-1")

        html_content = markdown2.markdown(content)
        return html_content
    except FileNotFoundError:
        return None