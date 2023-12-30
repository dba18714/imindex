from django import forms
from .models import Link


class AddForm(forms.ModelForm):
    url = forms.CharField(widget=forms.Textarea, help_text="输入多个URL，每行一个。")

    class Meta:
        model = Link
        fields = ['url']


class MultiURLForm(forms.Form):
    urls = forms.CharField(widget=forms.Textarea, help_text="输入多个URL，每行一个。")
    # urls = forms.CharField(
    #     widget=forms.Textarea(attrs={
    #         'class': 'relative w-full p-4 placeholder-transparent transition-all border rounded outline-none focus-visible:outline-none peer border-slate-200 text-slate-500 autofill:bg-white invalid:border-pink-500 invalid:text-pink-500 focus:border-stone-500 focus:outline-none invalid:focus:border-pink-500 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400',
    #         'placeholder': 'Write your message'
    #     }),
    #     help_text="输入多个URL，每行一个。"
    # )
