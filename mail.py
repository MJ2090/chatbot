
import df
import robot
import secrets
import string
import pandas as pd
import os
import numpy as np
import openai

relative_path = '~/embedding/data/'


def run_it_3(my_text, qs):
    my_texts = [("embedding", my_text)]
    my_df = df.get_df(my_texts)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    ans = []
    for q in qs:
        tmp = {"Question": q, "Answer": robot.answer_question(
            my_df, question=q)}
        ans.append(tmp)

    return ans


def run_it_3_question(question, random_str):
    file_path = relative_path + random_str + '.csv'
    if not os.path.exists(file_path):
        return "I don't know."
    my_df = pd.read_csv(file_path, index_col=0)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    ans = robot.answer_question(my_df, question=question)
    return ans


def run_it_3_action(question, model):
    msg = """
    A and B are talking with each other, if A says "{}", is it logically correct for B to reply as 
    "You can take the self assessment on our website"?
    Please only give a score between 1 and 100 and don't explain, where 1 means totally not possible, and 100 means very probably.
    """.format(question)
    messages = [
        {"role": "user", "content": msg},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        max_tokens=1000,
        messages=messages,
    )

    return response


def run_it_3_training(text):
    my_texts = [("embedding", text)]
    my_df = df.get_df(my_texts)
    my_df.head()
    random_str = ''.join(secrets.choice(
        string.ascii_uppercase + string.digits) for i in range(10))

    file_path = relative_path + random_str + '.csv'
    if not os.path.exists(relative_path):
        os.mkdir(relative_path)

    my_df.to_csv(file_path)

    my_df = pd.read_csv(file_path, index_col=0)
    return random_str


def sendchat_home(request):
    new_message = request.POST['message']
    use_embedding = request.POST.get('use_embedding')
    use_embedding = True
    use_gpt = True
    use_action = True
    return_dict = {}

    if use_embedding:
        answer = run_it_3_question(new_message, 'NX32LBMJ3E')
        if not answer == "I don't know.":
            return_dict['ai_message'] = answer
            # return HttpResponse(json.dumps({'ai_message': answer}))
    if use_action:
        openai_response = run_it_3_action(new_message, model='gpt-3.5-turbo')
        action_score = openai_response["choices"][0]["message"]["content"]
        action_score = action_score.replace('.', '').replace('\n', '').replace(' ', '')
        print('action_score= ', action_score, action_score.isnumeric())
        if action_score.isnumeric() and int(action_score) >= 80:
            print('inside')
            answer = "You can do a free self assessment by clicking the link below."
            return_dict['action_message'] = answer
            return_dict['ai_action'] = 1
        
    if len(return_dict) > 0:
        return HttpResponse(json.dumps(return_dict))
    
    if not use_gpt:
        return HttpResponse(json.dumps({'ai_message': 'Sorry, but I cannot help you with that.'}))

    my_m = PromptModel.objects.get(name='Done FAQ')
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Msg sent to openai: ", messages)

    openai_response = run_it_chat(messages, model='gpt-3.5-turbo')
    ai_message = openai_response["choices"][0]["message"]["content"]

    return HttpResponse(json.dumps({'ai_message': ai_message}))
