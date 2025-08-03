from django.shortcuts import render , redirect
from .forms import *
# Create your views here.
def home(request):
    return render(request, 'home.html')

def scrabble(request):
    if request.method == 'POST':
        form = PlayerInfo(request.POST)
        if form.is_valid():
            player_num = int(form.cleaned_data['num_players'])
            return redirect('start_scrabble',player_num)
            # Redirect to the scrabble start view with the number of players
            # redirect('start_scrabble', player_num=player_num)
        else:
            form = PlayerInfo()
    else:
        form = PlayerInfo()
    return render(request, 'scrabble.html',{'form': form})

#   redirect(viewname, *args, **kwargs) is used to redirect to a specific view with arguments
#   In this case, we are redirecting to the 'start_scrabble' view with the player_num as an argument
#   positional arguments need to be passsed matching to your urls.py pattern or named keyword arguments like player_num=player_num
def scrabble_start(request,player_num):
    return render(request, 'scrabble_start.html', {'player_num': player_num})

def scramble(request):
    return render(request, 'scramble.html')

def spellathon(request):
    return render(request, 'spellathon.html')