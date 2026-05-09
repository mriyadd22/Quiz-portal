from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import *
from .forms import *
import random



# Create your views here.


def user_register(request):
    if request.method == 'POST':
        form_data = UserRegiserForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'User Registered')
            return redirect('login_page')
        
    form_data = UserRegiserForm()
    con = {
        'data' : form_data
    }

    return render(request, 'register.html', con)



def user_login(request):
    if request.method == 'POST':
        form_data = UserLoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            messages.success(request, 'User Loged-in')
            return redirect('profiel_update')
        
    form_data = UserLoginForm()
    con = {
        'data' : form_data
    }
        

    return render(request, 'login.html', con)


@login_required
def user_logout(request):
    logout(request)

    return redirect('login_page')

def profile(request):

    return render(request, 'profile.html')



def dashboard(request):
    quizzes = QuizModel.objects.all()
    return render(request, 'dashboard.html', {'quizzes': quizzes})


@login_required
def profiel_update(request):
    try:
        data = request.user.user_profile
    except ParticipantModel.DoesNotExist:
        data = None

    if request.method == 'POST':
        form_data = ProfileForm(request.POST, instance = data)
        if form_data.is_valid():
            pd = form_data.save(commit=False)
            pd.usr = request.user
            pd.save()
            messages.success(request, 'profile updated')
            return redirect('profile')
        

    form_data = ProfileForm(instance = data)
        
    con = {
        'title' : 'User profile update',
        'data' : form_data,
        'btn' : 'Update'
    }

    return render(request, 'base-form.html', con)




@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(QuizModel, id=quiz_id)
    questions = list(QuestionModel.objects.filter(Quiz=quiz))
    random.shuffle(questions)

    if request.method == 'POST':
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected:
                option = OptionModel.objects.get(id=selected)
                if option.is_correct:
                    score += 1

        participant = ParticipantModel.objects.get(usr=request.user)
        ResultModel.objects.create(
            user=participant, 
            quiz=quiz, 
            score=score
        )

        return redirect('result', quiz_id=quiz.id)
        

    for q in questions:
        options = list(OptionModel.objects.filter(quesion=q))
        random.shuffle(options)
        q.options = options

    con = {
        'quiz': quiz, 
        'questions': questions
        }

    return render(request, 'quiz.html', con)




@login_required
def result_view(request, quiz_id):
    quiz = QuizModel.objects.get(id=quiz_id)
    results = ResultModel.objects.filter(quiz=quiz).order_by('-score')

    participant = ParticipantModel.objects.get(usr=request.user)
    user_result = results.filter(user=participant).first()
    position = list(results).index(user_result) + 1 if user_result else None

    con = {
        'score': user_result.score if user_result else 0,
        'position': position
    }

    return render(request, 'result.html', con)




@staff_member_required
def add_quiz(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        quiz = QuizModel.objects.create(title=title, description=description)

        questions = request.POST.getlist('questions')

        for i, q_text in enumerate(questions):
            question = QuestionModel.objects.create(quiz=quiz, question=q_text)

            options = request.POST.getlist(f'options_{i}')
            correct = request.POST.get(f'correct_{i}')

            for j, opt in enumerate(options):
                OptionModel.objects.create(
                    question=question,
                    option=opt,
                    is_correct=(str(j) == correct)
                )

        return redirect('dashboard')

    return render(request, 'add-quiz.html')





@staff_member_required
def add_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save()

            questions = question_formset.save(commit=False)
            for q in questions:
                q.quiz = quiz
                q.save()

            return redirect('admin_dashboard')

    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet()

    con =  {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
    }

    return render(request, 'add-quiz.html', con)