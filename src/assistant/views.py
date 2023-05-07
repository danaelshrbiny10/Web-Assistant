from django.shortcuts import render, redirect
import openai
from .secret_key import API_KEY


openai.api_key = API_KEY


def home(request):
    try:
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]
        if request.method == 'POST':
            
            prompt = request.POST.get('prompt')
            temperature = float(request.POST.get('temperature', 0.1))
            request.session['messages'].append({"role": "user", "content": prompt})
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )
            
            formatted_response = response['choices'][0]['message']['content']
            
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
        
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home.html', context)
        else:
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'assistant/home.html', context)
    except Exception as e:
        print(e)
        return redirect('error_handler')


def new_chat(request):
    request.session.pop('messages', None)
    return redirect('home')


def error_handler(request):
    return render(request, 'assistant/404.html')
