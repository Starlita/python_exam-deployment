from django.shortcuts import render, redirect
from .models import User, Thought, UserManager, ThoughtManager
from django.contrib import messages
import bcrypt
from django.db.models import Count

def index(request):
    return render(request, 'index.html')

def createUser(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                firstname=request.POST['first_name'],
                lastname=request.POST['last_name'],
                email=request.POST['email'],
                password=hashed_pw)
    return redirect('/')

def loginUser(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id #IMPORTANT!!!
                return redirect('/thoughts')
    return redirect('/')

def logout(request):
    if request.session['user_id']:
        request.session.clear()
    return redirect('/')

def showThoughts(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    else:
        context={
            'user': User.objects.get(id=request.session['user_id']),
            'all_thoughts': Thought.objects.annotate(likes=Count('users_who_like')).
            order_by('-likes')
        }
        return render(request, 'thoughts.html', context)

def addThought(request):
    if request.method == "POST":
        errors = Thought.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user = User.objects.get(id=request.session['user_id'])
            thought = Thought.objects.create(
                thought_text=request.POST['thought_text'],
                uploaded_by=User.objects.get(id=request.session['user_id'])
            )
            # thought.users_who_like.add(user)
    return redirect ('/thoughts')

def show_one_thought(request, thought_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    else:
        thought_with_id = Thought.objects.filter(id=thought_id)
        if thought_with_id:
            context = {
                "thought": Thought.objects.get(id=thought_id),
                "user":User.objects.get(id=request.session['user_id'])

            }
            return render(request, "oneThought.html", context)
        else:
            return redirect('/')

def deleteThought(request, thought_id):
    thought= Thought.objects.get(id=thought_id)
    thought.delete()
    return redirect('/thoughts')

def makeLike(request, thought_id):
    thought_with_id = Thought.objects.filter(id=thought_id)
    if thought_with_id: 
        thought = thought_with_id[0]
        user = User.objects.get(id=request.session['user_id'])
        user.liked_thoughts.add(thought)
            #user.cats_voted_for.add(cat) ------> alternative to the above ORM
    return redirect (f'/onethought/{thought_id}')

def unlike(request, thought_id):
    if request.method == "POST":
        thought_with_id = Thought.objects.filter(id=thought_id)
        if thought_with_id: 
            thought = thought_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            thought.users_who_like.remove(user)
                #user.cats_voted_for.remove(cat) ------> alternative to the above ORM
    return redirect (f'/onethought/{thought_id}')


