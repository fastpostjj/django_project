from django import forms
from products.models import Category, Products, Version


LIST_FORBIDDEN_WORD =["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

def is_text_valid(text:str) -> bool:
    """
    :param text:
    :return: True, if text does not contains forbidden words
    """
    text = text.lower()
    for word in LIST_FORBIDDEN_WORD:
        if text.find(word, 0, len(text)) != -1:
            return False
    return True

class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        """
        нельзя добавлять слова: казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар
        """
        name = self.cleaned_data['name']
        if not is_text_valid(name):
            raise forms.ValidationError('Название не должно содержать словa: ' + ", ".join(LIST_FORBIDDEN_WORD))
        return name

    def clean_description(self):
        """
        нельзя добавлять слова: казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар
        """
        description = self.cleaned_data['description']
        if not is_text_valid(description):
            raise forms.ValidationError('Описание товара не должно содержать словa: ' + ", ".join(LIST_FORBIDDEN_WORD))
        return description