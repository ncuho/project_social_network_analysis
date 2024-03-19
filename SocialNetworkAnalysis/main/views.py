from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        return render(request, 'main/index.html', {'result': "Hello World!"})
    return render(request, 'main/index.html')
