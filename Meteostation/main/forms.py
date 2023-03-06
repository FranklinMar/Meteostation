from django.forms import Form, FileField, FileInput


class UploadFileForm(Form):
    file = FileField(allow_empty_file=False, widget=FileInput(attrs={
                'style': 'display: contents;',
                'accept': '.xlsx, .csv, .txt',
                'id': 'file'
            }))
