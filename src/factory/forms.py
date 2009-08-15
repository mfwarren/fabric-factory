from django.forms.models import ModelForm

from factory.models import Build, FabfileRecipe

class BuildForm(ModelForm):
    class Meta:
        model = Build
        exclude = ('fabfile_recipe',) 