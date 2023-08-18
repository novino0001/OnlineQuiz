from django.db import models
from django.contrib.auth.models import User
import random
from autoslug import AutoSlugField

 

class Student(models.Model):
     name = models.CharField(max_length=100)
     institute = models.CharField(max_length=200)
     Qualification = models.CharField(max_length=100)
     level = models.CharField(max_length=100)
     level_slug = AutoSlugField(populate_from='level',unique = True , null = True , default = None)


class QuizCategory(models.Model):
#     level = models.CharField(max_length=100)
    Title = models.CharField(max_length=100)
    detail = models.TextField()
    image = models.ImageField(upload_to='')
    

    class Meta:
         verbose_name_plural = 'Category'
    def __str__(self) -> str:
        return self.Title


  

class QuizQuestion (models.Model):

        category=models.ForeignKey(QuizCategory, on_delete=models.CASCADE) 
        question=models.TextField()
        opt_1=models.CharField(max_length=200)
        opt_2=models.CharField(max_length=200)
        opt_3=models.CharField(max_length=200)
        opt_4=models.CharField(max_length=200)
        que_level=models.CharField(max_length=100)
        time_limit=models.IntegerField()
        right_opt=models.CharField(max_length=100)
        
        class Meta:
             verbose_name_plural = 'Question'
        
        def __str__(self) -> str:
             return self.question  
        
# class MyUUIDModel(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
   
class UserSubmittedAnswer (models.Model):
    usid = models.IntegerField(blank=True, null=True)
    question =  models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer=models.CharField(max_length=200)

    class Meta:
       verbose_name_plural='User Submitted Answers'

    #   id, question, question_id, right_answer, user, user_id
