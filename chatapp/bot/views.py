from django.shortcuts import render
from src.main import handle_chat


def home(request):
    ret = {'msg': 'Hi Done.'}
    return render(request, 'bot/home.html', ret)


def test(request):
    ret = {'msg': 'Hi Tester.'}
    return render(request, 'bot/home.html', ret)