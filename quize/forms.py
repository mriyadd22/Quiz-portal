from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import inlineformset_factory
from .models import *



class UserRegiserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})




# class ParticipantForm(forms.ModelForm):
#     class Meta:
#         model = ParticipantModel
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         for f in self.fields.values():
#             f.widget.attrs.update({'class': 'form-control'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ParticipantModel
        fields = '__all__'
        exclude = ['usr']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})




class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizModel
        fields = ['title', 'description']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ['question']


class OptionForm(forms.ModelForm):
    class Meta:
        model = OptionModel
        fields = ['option', 'is_correct']


# Formsets
QuestionFormSet = inlineformset_factory(
    QuizModel, QuestionModel,
    form=QuestionForm,
    extra=1,
    can_delete=True
)

OptionFormSet = inlineformset_factory(
    QuestionModel, OptionModel,
    form=OptionForm,
    extra=2,
    can_delete=True
)