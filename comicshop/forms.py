from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile, Product, Category #<--- add this to add Product


class ProductForm(forms.ModelForm):
    artist_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artist Name'}))
    #publisher = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publisher'}))
    publisher = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Publisher", widget=forms.Select(attrs={'class': 'form-control'}))
    comics = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comics'}))
    work_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work Link'}))
    price = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}))
    image = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}))
    image1 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image2 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image3 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image4 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image5 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image6 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image7 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image8 = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Product
        fields = ['artist_name', 'publisher', 'comics', 'work_link', 'price', 'image', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8']



class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country']



class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<span class="form-text text-muted"><small>Your password can\'t be too similar to your other personal information.<br>Your password must contain at least 8 characters.<br>Your password can\'t be a commonly used password.<br>Your password can\'t be entirely numeric.</small></span>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Your password can\'t be too similar to your other personal information.<br>Your password must contain at least 8 characters.<br>Your password can\'t be a commonly used password.<br>Your password can\'t be entirely numeric.</small></span>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

