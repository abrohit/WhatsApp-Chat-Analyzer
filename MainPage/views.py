import os

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .Main import ExtractData, StatGenerator
from .forms import DocumentForm


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def Home(request):
    return(render(request, 'main/home.html'))

def Analyze(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        file_path = BASE_DIR + '\media\\' + name

        ed = ExtractData(file_path)
        ed.Main_Process()
        dataframe = ed.Change_Dataframe()

        stats = StatGenerator(dataframe)

        totalemojis = stats.TotalEmojis()
        uniqueemojis = stats.UniqueEmojis()
        totalmessages = stats.TotalMessages()

        activity = stats.ActivityOverDates()
        mostusedwords = stats.MostUsedWords(5)
        mostactivemembers = stats.MostActive(5)
        nightowls = stats.NightOwls(5)
        earlybirds = stats.EarlyBirds(5)
        emojispammers = stats.EmojiSpammers(5)
        frequentemojis = stats.FrequentEmojis(5)

        html_data = {'Name': uploaded_file.name, 'TotalEmojis' : totalemojis, 'UniqueEmojis' : uniqueemojis, 'TotalMessages' : totalmessages,'Activity' : activity, 'MostUsedWords' : mostusedwords , 
        'MostActiveMembers' : mostactivemembers, 'NightOwls' : nightowls, 'EarlyBirds' : earlybirds, 'EmojiSpammers' : emojispammers, 'FrequentEmojis' : frequentemojis}

        os.remove(file_path)

        return(render(request, 'main/analyze.html', html_data))
    else:
        return(render(request, 'main/analyze.html'))
