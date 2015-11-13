from django.forms import ModelForm

from TestCases.models import ToDoNotes


class ToDoNotesForm(ModelForm):

    class Meta:
        model = ToDoNotes
        exclude = ['created', 'modified', 'done', 'discarded']
