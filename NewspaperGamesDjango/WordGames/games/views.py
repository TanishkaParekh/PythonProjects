from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')
def scrabble(request):
    return render(request, 'scrabble.html')
def scramble(request):
    return render(request, 'scramble.html')
def spellathon(request):
    return render(request, 'spellathon.html')