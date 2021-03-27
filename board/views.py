from django.shortcuts import render

def main(request):
    return render(request, 'board/main.html')

def detail(request):
    return render(request, 'board/detail.html')