from django.shortcuts import render
from .forms import DocumentForm

def Home(request):
    return(render(request, 'main/home.html'))

def Analyze(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return(redirect('home'))
    else:
        form = DocumentForm()
    return(render(request, 'main/home.html', {'form': form}))

    #return(render(request, 'main/analyze.html'))
