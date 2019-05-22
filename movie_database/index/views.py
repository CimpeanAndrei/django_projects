from django.shortcuts import render
from index.models import Title, Year, Keyword, Genre

from django.core.paginator import Paginator
# Create your views here.


def home_page(request):
    return render(request, "home.html")


def yearSearch(request):
    obj = Year()
    if request.GET.get('y') is not None:
        searchYear = request.GET.get('y')
        if request.GET.get('p') is not None and request.GET.get('p') != '':
            page = request.GET.get('p')
        else:
            page = '1'
        yearData = obj.getDataByYear(searchYear, page)
        Items = yearData.get("Items", [])
        index = int(page)
        count = int(yearData['Total_Pages'])
        context = {
            'Year': searchYear,
            'yearData': yearData,
            'searchYear': True,
            'index': index,
            'count': count,
        }
        return render(request, 'searchYear.html', context)
    else:
        return render(request, 'home.html')


def genreSearch(request):
    obj = Genre()
    if request.GET.get('g') is not None:
        searchGenre = request.GET.get('g')
        getGenreId = obj.switchGenre_Id(searchGenre)
        page = request.GET.get('p')
        genreData = obj.getDataByGenre(getGenreId, page)
        context = {
            'genreData': genreData,
            'searchGenre': True
        }
        return render(request, 'searchGenre.html', context)
    else:
        return render(request, 'home.html')


def keywordSearch(request):
    obj = Keyword()
    if request.GET.get('k') is not None:
        searchKeyword = request.GET.get('k')
        page = request.GET.get('p')
        keywordData = obj.getKeywordData(searchKeyword, page)
        context = {
            'keywordData': keywordData,
            'searchKeyword': True
        }
        return render(request, 'searchKeyword.html', context)
    else:
        return render(request, 'home.html')


def titleSearch(request):
    obj = Title()
    if request.GET.get('t') is not None:
        searchTitle = request.GET.get('t')
        movieData = obj.getDataByTitle(searchTitle)
        context = {
            'movieData': movieData,
            'searchTitle': True
        }
        return render(request, 'searchTitle.html', context)
    else:
        return render(request, 'home.html')
