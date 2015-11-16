from django.forms import ModelForm

from TestCases.models import ToDoNote


class CreateToDoNoteForm(ModelForm):

    class Meta:
        model = ToDoNote
        exclude = ['created', 'modified', 'done', 'discarded']


class EditToDoNoteForm(ModelForm):

    class Meta:
        model = ToDoNote
        exclude = ['created', 'modified']
