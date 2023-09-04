from django import forms

from main.models import Mailing, MailingLogs, Client, Message

forbidden_words = 'казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар'


class StyleFormMixin:
    pass

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'name', 'photo', 'comment')


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject_letter', 'body_letter', 'mailing')


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('frequency', 'time_mailing', 'mailing_status', 'client')

    # def clean_name(self):
    #     cleaned_data = self.cleaned_data['name']
    #
    #     if cleaned_data in forbidden_words:
    #         raise forms.ValidationError('Запрещенный продукт')
    #
    #     return cleaned_data
    #
    # def clean_description(self):
    #     cleaned_data = self.cleaned_data['description']
    #
    #     if cleaned_data in forbidden_words:
    #         raise forms.ValidationError('Запрещенное описание продукта')
    #
    #     return cleaned_data


class MailingLogsForm(StyleFormMixin, forms.ModelForm):
    model = MailingLogs
    fields = ('datetime_of_last_try', 'status_of_try', 'response_of_mail_server', 'client', 'mailing')

    class Meta:
        model = MailingLogs
        fields = '__all__'
