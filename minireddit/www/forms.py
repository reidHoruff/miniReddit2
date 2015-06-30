from django import forms

class SiForm(forms.Form):
  def get_errors(self):
    return self.errors.items()[0][1]

  def get_first_error(self):
    errors = self.get_errors()

    if errors:
      return errors[0]

    return None

class PasswordField(forms.CharField):
  def __init__(self, *args, **kwargs):
    kwargs['widget'] = forms.PasswordInput()
    forms.CharField.__init__(self, *args, **kwargs)

def field_with_errors(field, name, *args, **kwargs):
  kwargs['error_messages'] = { 
    'invalid': '%s field is invalid.'%name,
    'required': '%s field is required'%name,
    'min_length': '%s field is too short.'%name,
    'max_length': '%s field is too Long.'%name,
    'invalid_choice': 'invalid choice for %s field.'%name,
  }
  return field(*args, **kwargs)

def text_input(name, min=1, max=1000, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.TextInput(attrs={'placeholder': name, 'class': 'form-control'}),
  )

def hidden_input():
  return forms.CharField(
    required=False,
    widget=forms.HiddenInput(),
  )

def password_input(name, min=1, max=100, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.PasswordInput(attrs={'placeholder': name, 'class': 'form-control'}),
  )

def email_input(name, min=1, max=100, required=True):
  return field_with_errors(
    field=forms.EmailField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.TextInput(attrs={'placeholder': name}),
  )

def date_input(name, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    required=required,
    widget=forms.TextInput(attrs={'placeholder': name, 'class': 'datepicker'}),
  )

def select(name, required=True, choices=()):
  return field_with_errors(
    field=forms.ChoiceField,
    name=name,
    required=required,
    choices=choices,
    widget=forms.Select(attrs={'class': 'btn'}),
  )

def textarea(name, min=1, max=100, required=True):
  return field_with_errors(
    field=forms.CharField,
    name=name,
    min_length=min,
    max_length=max,
    required=required,
    widget=forms.Textarea(attrs={'placeholder': name, 'class': 'form-control'}),
  )

def hidden_integer(required=True):
  return forms.IntegerField(
    required=required,
    widget=forms.HiddenInput(),
  )

"""
Start actual forms
"""

class Register(SiForm):
  password1 = password_input(name='Password')
  password2 = password_input(name='Confirm Password')
  username = text_input(name='username') 

class SubmitPost(SiForm):
  def set_sub(self, sub):
    self.fields['subreddit'].initial = sub
    return self

  title = text_input(name='title') 
  nsfw = forms.BooleanField()
  subreddit = text_input(name='subreddit') 
  url = text_input(name='url', required=False) 
  body = textarea(name='body', required=False) 

class CreateSub(SiForm):
  name = text_input(name='name') 

class LoginForm(SiForm):
  username = text_input(name='username')
  password = password_input(name='Password')

class PostComment(SiForm):
  def set_parent_id(self, parent):
    self.fields['parent_id'].initial = parent
    return self

  def set_post_id(self, postid):
    self.fields['post_id'].initial = postid
    return self

  body = textarea(name='body')
  post_id = hidden_integer()
  parent_id = hidden_integer()
