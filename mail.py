
import df
import robot
import secrets
import string
import pandas as pd
import os
import numpy as np
import openai
import json
import openai


relative_path = '~/embedding/data/'


def complete_chat(messages, model):
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.4,
        max_tokens=3000,
        messages=messages,
    )
    return response


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


def embedding_question(question, random_str):
    file_path = relative_path + random_str + '.csv'
    if not os.path.exists(file_path):
        return "I don't know."
    my_df = pd.read_csv(file_path, index_col=0)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    ans = robot.answer_question(my_df, question=question)
    return ans


def embedding_training(text):
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


def embedding_action(question, model):
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


def handle_chat(request):
    new_message = request.POST['message']
    use_embedding = True
    use_gpt = True
    use_action = True
    return_dict = {}

    if use_embedding:
        answer = embedding_question(new_message, '~/chatbot/done_embedding.csv')
        if not answer == "I don't know.":
            return_dict['ai_message'] = answer
            # return HttpResponse(json.dumps({'ai_message': answer}))
    if use_action:
        openai_response = embedding_action(new_message, model='gpt-3.5-turbo')
        action_score = openai_response["choices"][0]["message"]["content"]
        action_score = action_score.replace('.', '').replace('\n', '').replace(' ', '')
        print('action_score= ', action_score, action_score.isnumeric())
        if action_score.isnumeric() and int(action_score) >= 80:
            answer = "You can do a free self assessment by clicking the link below."
            return_dict['action_message'] = answer
            return_dict['ai_action'] = 1
        
    if len(return_dict) > 0:
        return wrap(json.dumps(return_dict))
    
    if not use_gpt:
        return wrap(json.dumps({'ai_message': 'Sorry, but I cannot help you with that.'}))

    predefined_history = """
    [{"role": "system", "content": "You are a virtual assistant for donefirst.com. You help users."}, 
    {"role": "assistant", "content": "OK I got it, I am an assistant on the donefirst.com, I help users by answering their questions."}]
    """
    messages = json.loads(predefined_history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Msg sent to openai: ", messages)

    openai_response = complete_chat(messages, model='gpt-3.5-turbo')
    ai_message = openai_response["choices"][0]["message"]["content"]

    return wrap(json.dumps({'ai_message': ai_message}))


def wrap(response):
    return response

    
def run_test():
    history_msg = """
    [{"role":"user","content":"Hello! How can I assist you today?"},{"role":"assistant","content":"i feel happy today"},{"role":"user","content":"That's great to hear! Is there anything specific that made you feel happy today?"}]
    """
    post_data = {'message': 'how are you?', 'history': history_msg}
    request = {}
    request['POST'] = post_data


if __name__ == "__main__":
    run_test()