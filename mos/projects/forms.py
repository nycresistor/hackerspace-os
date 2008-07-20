from models import Project
from django.forms.models import ModelForm


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name','teaser','wikiPage','finished_at')
