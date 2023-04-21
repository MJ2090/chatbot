from django.shortcuts import render


def home(request):
    ret = {'msg': 'Hi Done.'}
    return render(request, 'embedding/home.html', ret)


def test(request):
    ret = {'msg': 'Hi Tester.'}
    return render(request, 'embedding/home.html', ret)