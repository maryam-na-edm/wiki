from django.shortcuts import render, Http404, redirect
from .util import list_entries, get_entry, save_entry, delete_entry
from . import util
import random

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)


def search(request):
    query = request.GET.get('q', '').lower()
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query in entry.lower()]
    if len(matching_entries) == 1:
        return redirect('entry', title=matching_entries[0])
    else:
        return render(request, 'encyclopedia/search_results.html', {
            'query': query,
            'entries': matching_entries
        })
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": {
                "title": title,
                "entry_content": entry_content,
            }
        })
    else:
        raise Http404("Entry not found")



def new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) is not None:
            return render(request, 'encyclopedia/error.html', {
                'error_message': 'An entry with this title already exists.'
            })
        util.save_entry(title, content)
        return redirect('entry', title=title)

    return render(request, 'encyclopedia/new_page.html')



def edit_page(request, title):
    existing_content = get_entry(title)

    if existing_content is None:
        raise Http404("Entry not found")

    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')
        if new_title != title:
            delete_entry(title)
        save_entry(new_title, new_content)
        return redirect('entry', title=new_title)

    return render(request, 'encyclopedia/edit_page.html', {
        'title': title,
        'existing_content': existing_content
    })
