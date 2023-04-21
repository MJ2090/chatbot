from django.shortcuts import render
from main import handle_chat


def home(request):
    ret = {'msg': 'Hi Done.'}
    return render(request, 'bot/home.html', ret)


def test(request):
    new_msg = """
    what is Done??
    """
    history_msg = """
    [{"role":"user","content":"Hello! How can I assist you today?"},{"role":"assistant","content":"i feel happy today"},{"role":"user","content":"That's great to hear! Is there anything specific that made you feel happy today?"}]
    """
    request_post_data = {'message': new_msg, 'history': history_msg}
    output = handle_chat(request_post_data)
    ret = {'msg': output}
    return render(request, 'bot/home.html', ret)