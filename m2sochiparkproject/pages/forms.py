from django import forms
from base.utils import prettify_phone_number

class LeadForm(forms.Form):
    """
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    text = models.TextField(blank=True, default='')
    user_agent = models.TextField(blank=True, default='')
    request_from = models.URLField(max_length=1000, blank=True, default='')
    form_name = models.CharField(max_length=250, blank=True, default='')
    block_id = models.CharField(max_length=250, blank=True, default='')
    """
    first_name = forms.CharField(
        label='Имя',
        max_length=150,
        required=True
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=150,
        required=False
    )

    email = forms.EmailField(
        label='Email',
        required=False
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=50,
        required=True
    )
    text = forms.CharField(
        label='Сообщение',
        max_length=1000,
        required=False
    )
    form_name = forms.CharField(
        label='Название формы',
        max_length=250,
        required=False
    )
    block_id = forms.CharField(
        label='ID блока формы',
        max_length=250,
        required=False
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name is not None:
            last_name = last_name.title()
        else:
            last_name = ''
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is not None:
            email = email.lower()
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_number = prettify_phone_number(raw_phone=phone)
        return phone_number
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text is None:
            text = ''
        return text
    
    def clean_form_name(self):
        form_name = self.cleaned_data.get('form_name')
        if form_name is None:
            form_name = ''
        return form_name
    
    def clean_block_id(self):
        block_id = self.cleaned_data.get('block_id')
        if block_id is None:
            block_id = ''
        return block_id
    
    def get_lead_data(self):
        data = {
            'email': self.cleaned_data.get('email'),
            'phone': self.cleaned_data.get('phone'),
            'first_name': self.cleaned_data.get('first_name').title().strip(),
            'last_name': self.cleaned_data.get('last_name').title().strip(),
            'text': self.cleaned_data.get('text'),
            'form_name': self.cleaned_data.get('form_name'),
            'block_id': self.cleaned_data.get('block_id'),
        }
        return data
