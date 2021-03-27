from django.shortcuts import render

def main(request):
    games = {1, 2, 3, 4, 5, 6}
    game_name = "PACMAN"
    game_desc = "arcade video game"
    game_img_url = 'static/board/img/pacman.jpg'
    context = {
        'games': games,
        'game_name': game_name,
        'game_desc': game_desc,
        'game_img_url': game_img_url,
    }
    return render(request, 'board/main.html', context=context)

def detail(request):
    return render(request, 'board/detail.html')