from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Room, User, Property


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    name = forms.CharField(max_length=200, required=False, help_text='Optional. Your full name.')
    
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.name = self.cleaned_data.get('name', '')
        if commit:
            user.save()
        return user


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'rent_amount', 'location', 'address',
            'bedrooms', 'bathrooms', 'area_sqft', 'description', 'amenities',
            'date_available', 'main_image'
        ]
        widgets = {
            'date_available': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'amenities': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., WiFi, Parking, Pool, Gym'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class PropertySearchForm(forms.Form):
    location = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter location'}))
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Min price'}))
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Max price'}))
    property_type = forms.ChoiceField(choices=[('', 'Any Type')] + Property.PROPERTY_TYPES, required=False)
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Min bedrooms'}))
