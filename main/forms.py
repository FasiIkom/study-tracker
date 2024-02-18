from django.forms import ModelForm
from main.models import Progress

class ProgressForm(ModelForm):
    class Meta:
        model = Progress
        fields = ["subject", "start_Study", "progress", "catatan"]