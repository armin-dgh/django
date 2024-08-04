from django import forms
from .models import *

class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهاد", "پیشنهاد"),
        ('انتقاد','انتقاد'),
        ('گزارش','گزارش')
    )
    massage = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={"placeholder": "massage"}))
    email = forms.EmailField()
    phone = forms.CharField(max_length=11)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عدد نیست")
            else:
                return phone

class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data["name"]
        if name:
            if len(name) < 3 :
                raise forms.ValidationError("نام کوتاه است")
            else:
                return name

    class Meta:
        model = Comment
        fields = ["name", "massage"]
        widgets = {
            "name": forms.TextInput(attrs={
                                    "placeholder": 'نام',
                                    "style": 'cm-name'}),
            "massage": forms.TextInput(attrs={
                "placeholder": 'متن',
                "style": 'cm-body'}),

        }


class CreatPostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول")
    image2 = forms.ImageField(label="تصویر دوم")
    def clean_title(self):
        title = self.cleaned_data["title"]
        if title:
            if len(title) < 3:
                raise forms.ValidationError("نام کوتاه است")

            else:
                return title
    def clean_description(self):
        description = self.cleaned_data["description"]
        if description:
            if len(description) > 250:
                raise forms.ValidationError("متن بلند است")
            else:
                return description

    class Meta:
        model = Post
        fields =["title", "description", "reading_time"]

class SearchForm(forms.Form):
    query = forms.CharField()


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=250, required=True)
#     password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)
#
#

class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, label="پسورد", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, label="تکرار پسورد", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password2"] != cd["password"]:
            raise forms.ValidationError("پسورد ها مطابقت ندارند.")
        return cd["password2"]
