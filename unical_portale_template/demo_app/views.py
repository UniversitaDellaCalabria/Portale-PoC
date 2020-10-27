from django.shortcuts import render

# Create your views here.


def index(request):
    """
    """
    template = "demo_index.html"
    d = {}
    return render(request, template, d)
