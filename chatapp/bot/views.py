from django.shortcuts import render


def home(request):
    ret = {'msg': 'Hi Done.'}
    return render(request, 'bot/home.html', ret)


def test(request):
    ret = {'msg': 'Hi Tester.'}
    return render(request, 'bot/home.html', ret)