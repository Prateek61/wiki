from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse
from markdown2 import markdown
from random import choice

from . import util


def index(request : HttpRequest) -> HttpResponse:
    data : QueryDict = request.GET
    query = data.get('q')
    entries : list = util.list_entries()
    if query:
        query_entries : list = list()
        for entry in entries:
            if query.lower() == entry.lower():
                return HttpResponseRedirect(reverse(f"encyclopedia:entry", args=(entry,)))
            elif query.lower() in entry.lower():
                query_entries.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": query_entries,
            "query": True
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "query": False
        })

def entry(request : HttpRequest, entry : str) -> HttpResponse:
    exact_entry : str = util.get_exact_entry(entry)
    entries = util.list_entries()

    content : str = util.get_entry(exact_entry)
    if not content:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/entry.html", {
        'title': entry,
        'content': markdown(content)
    })

def create(request : HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data : QueryDict = request.POST
        title : str = data.get('title')
        content : str = data.get('content')
        
        if not title or not content:
            return render(request, "encyclopedia/create.html", {
                "message": "Fill out data properly"
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse(f"encyclopedia:entry", args=(title,)))

    else:
        return render(request, "encyclopedia/create.html")

def random(request : HttpRequest) -> HttpResponse:
    entries = util.list_entries()
    entry = choice(entries)
    return HttpResponseRedirect(reverse(f"encyclopedia:entry", args=(entry,)))

def edit(request : HttpRequest, entry : str) -> HttpResponse:
    entry = util.get_exact_entry(entry)
    if request.method == "POST":
        data : QueryDict = request.POST
        content : str = data.get('content')
        if not content:
            return render(request, "encyclopedia/edit.html", {
                "message": "Fill out data properly",
                "title": entry,
                "content": util.get_entry(entry)
            })
        else:
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse(f"encyclopedia:entry", args=(entry,)))
        
    else:
        return render(request, "encyclopedia/edit.html", {
                "title": entry,
                "content": util.get_entry(entry)
            })