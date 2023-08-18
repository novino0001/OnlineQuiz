from django.shortcuts import render ,redirect
from django.http import HttpResponse
from . import forms
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from . import models 
from django.contrib.auth.decorators import login_required
import random


# unique_id = random.randint(1000, 9999)
# Create your views here.
def home(request):
    return render(request , 'home.html')

def register(request):
    msg = None
    form = forms.RegisterUser
    if request.method == "POST":
        form = forms.RegisterUser(request.POST)
       
        if form.is_valid():
            form.save()
            msg = "account create successfully"
            return redirect('login/')

    return render(request,"registration/register.html" , {'form':form , 'msg':msg})
@login_required 
def student_info(request,category_id):
    category = models.QuizCategory.objects.get(id = category_id)

    # print("-------------------------------------------->",category.id)
    context = {}
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        institute_name = request.POST.get('institute_name')
        Qualification = request.POST.get('Qualification')
        select_level = request.POST.get('select_level')
        
        # const c_level = select_level
        # question = models.QuizQuestion.objects.filter(category=category , que_level = level)
        models.Student.objects.create(name = student_name , institute = institute_name,Qualification = Qualification , level=select_level)
        return redirect(f"/category-questions/{category.id}/{select_level}")
         
        
    return render(request,"student_info.html")

 

def all_category(request):
    category_data = models.QuizCategory.objects.all()
    return render(request , 'all_category.html' , {'category_data' : category_data   })


 
@login_required
def category_questions(request,category_id, level):
    # print("level==>", level)
     
    print("----------------before--------------------->",level)
    global unique_id
    unique_id = random.randint(1000, 9999)
    category = models.QuizCategory.objects.get(id = category_id)
  
    question = models.QuizQuestion.objects.filter(category=category, que_level=level ).order_by('id').first()
    print("-----------------after-------------------->",level)
    return render(request,"category_questions.html",{'question':question  , 'category':category  , 'unique_id':unique_id , 'level':level})


 
# def filter_level(request,category_id):
#     category = models.QuizCategory.objects.get(id = category_id)
#     question_data = models.QuizQuestion.objects.filter(category=category).order_by('id').first()

#     print(" ------------------>>>>>>>",question_data)
#     return render(request , 'filter_level.html' , {'category' : category   , 'question_data':question_data })
def user_profile(request):
    student_data = models.Student.objects.all();

    return render(request,"user_profile.html",{'student_data':student_data})   

@login_required
def submit_answer(request,category_id,question_id,level ):
    
    if request.method == "POST":
        category = models.QuizCategory.objects.get(id = category_id)
        question = models.QuizQuestion.objects.filter(category=category ,que_level=level , id__gt = question_id).exclude(id=question_id).order_by('id').first()
        print("-----------------after_answer-------------------->",level)
        if 'skip' in request.POST:
            # print("test")   
            if question:
                quest = models.QuizQuestion.objects.get(id=question_id)
                user = request.user
                answer = 'Not Submitted'
                # print(f"user==> {user}, quetion = {quest}, right_ans==>{answer}")
                models.UserSubmittedAnswer.objects.create(user = user ,question = quest, right_answer = answer , usid = unique_id  )
               
            else:
                quest = models.QuizQuestion.objects.get(id=question_id)
                user = request.user
                answer = 'Not Submitted'
                # print(f"user==> {user}, quetion = {quest}, right_ans==>{answer}")
                models.UserSubmittedAnswer.objects.create(user = user ,question = quest, right_answer = answer , usid = unique_id   )    
        else:
            # cateogy = models.QuizCategory.objects.filter()
            quest = models.QuizQuestion.objects.get(id=question_id)
            user = request.user
            answer = request.POST['answer']
            models.UserSubmittedAnswer.objects.create(user = user , question = quest , right_answer = answer, usid = unique_id  )
            
        if question:
            return render(request,"category_questions.html",{'question':question  , 'category':category , 'level' : level ,'unique_id':unique_id })
         

        else:
            print()
            category = models.QuizCategory.objects.get(id = category_id)
            result = models.UserSubmittedAnswer.objects.filter(user = request.user, usid = unique_id  )
           
            skipped = models.UserSubmittedAnswer.objects.filter(user = request.user, usid = unique_id , right_answer = 'Not Submitted').count()
            Attempted = models.UserSubmittedAnswer.objects.filter(user = request.user ,usid = unique_id ).exclude(right_answer = 'Not Submitted').count()
            Wrong = 0
            right = 0
            passing = 0
            fail = 0
            for row in result:
                if row.question.right_opt == row.right_answer :
                    right+=1
                else:
                    if row.right_answer != 'Not Submitted':
                        Wrong+=1
            percentage = (right*100)/(result.count()) 
            per = format(percentage,'.2f')    
            percentage = per  
            if percentage >= '60' :
                passing = percentage
            else:
                fail = percentage      

            return render(request,"result.html",{'result':result , 'category' : category , 'total_skipped':skipped , 'Attempted_skipped':Attempted , 'right':right , 'wrong':Wrong , 'passing':passing , 'fail':fail})
    
    else:
        return HttpResponse("Method not allowed") 
    


