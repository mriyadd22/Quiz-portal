from django.db import models
from django.contrib.auth.models import User




class ParticipantModel(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    ]

    name = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, choices=GENDER, null=True)
    age = models.PositiveIntegerField(null=True)
    prt_class = models.CharField(max_length=200, null=True)
    institute = models.CharField(max_length=255, null=True)
    usr = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='user_profile',
        null=True
    )


class QuizModel(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    


class QuestionModel(models.Model):
    question = models.CharField(max_length=255, null=True)
    Quiz = models.ForeignKey(
        QuizModel,
        on_delete=models.CASCADE,
        related_name='quiz_question',
        null=True
    )
    
    def __str__(self):
        return self.question
    


class OptionModel(models.Model):
    option = models.CharField(max_length=255, null=True)
    is_correct = models.BooleanField(default=False)
    quesion = models.ForeignKey(
        QuestionModel,
        on_delete=models.CASCADE,
        related_name='opt_question',
        null=True
    )


    def __str__(self):
        return self.option
    


class ResultModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, related_name='quiz_result')
    user = models.ForeignKey(ParticipantModel, on_delete=models.CASCADE, related_name='participent')
    score = models.IntegerField(null=True)

    def __str__(self):
        return self.score
    


