from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'user_interface_demo/index.html', context)
