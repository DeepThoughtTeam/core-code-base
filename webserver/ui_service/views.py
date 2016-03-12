from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'ui_service/index.html', context)
