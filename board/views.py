from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Game:
    name = "PACMAN"
    desc = "arcade video game"
    img_url = 'static/board/img/pacman.jpg'


def main(request):
    games = [Game()] * 31

    paginator = Paginator(games, 8) # object_list
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Set first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # Set last page, if the counter is bigger then max_page
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'games': games,
        'page_obj': page_obj,
        'page_numbers': paginator.page_range
    }
    return render(request, 'board/main.html', context=context)


def detail(request, game_id):
    return render(request, 'board/detail.html')

