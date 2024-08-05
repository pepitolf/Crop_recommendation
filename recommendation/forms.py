from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Crop, Knowledge, KnowledgeRule, KnowledgeFuzzyValue

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('admin', 'Admin'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    security_key = forms.CharField(max_length=100, required=False, help_text='Required for admin accounts only.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'security_key']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirmation"

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_farmer', 'is_admin']
        widgets = {
            'is_farmer': forms.CheckboxInput(attrs={'disabled': 'disabled'}),
            'is_admin': forms.CheckboxInput(attrs={'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['is_farmer'].initial = self.instance.is_farmer
        self.fields['is_admin'].initial = self.instance.is_admin  # Change is_superuser to is_admin

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name']

class KnowledgeForm(forms.ModelForm):
    class Meta:
        model = Knowledge
        fields = ['name']  

class KnowledgeRuleForm(forms.ModelForm):
    knowledges = forms.ModelMultipleChoiceField(
        queryset=Knowledge.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = KnowledgeRule
        fields = ['crop', 'knowledges']

    def __init__(self, *args, **kwargs):
        super(KnowledgeRuleForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['knowledges'].initial = self.instance.details.values_list('knowledge', flat=True)

    def clean_knowledges(self):
        knowledges = self.cleaned_data.get('knowledges')
        crop = self.cleaned_data.get('crop')

        for knowledge in knowledges:
            if not KnowledgeFuzzyValue.objects.filter(crop=crop, knowledge=knowledge).exists():
                self.add_error('knowledges', forms.ValidationError(
                    f"No Fuzzy Value exists for the knowledge '{knowledge.name}' and crop '{crop.name}'. Please create a Fuzzy Value for this combination."
                ))

        return knowledges

class KnowledgeFuzzyValueForm(forms.ModelForm):
    class Meta:
        model = KnowledgeFuzzyValue
        fields = ['crop', 'knowledge', 'fuzzy_set_type', 'x1', 'x2', 'x3', 'x4']