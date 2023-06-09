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

class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VersionForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Задаем класс для кнопки "Создать версию"
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_active'].label_attrs = {'class': 'form-check-label'}

    def clean_is_active(self):
        """
        нельзя дабавить более одной активной версии
        """
        is_active = self.cleaned_data['is_active']
        if is_active and self.instance.product.version_set.filter(is_active=True).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Нельзя добавить более одной активной версии')
        return is_active
    def save(self, commit=True):
        super(VersionForm, self).save()

class CategoryForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Задаем класс для кнопки "Создать версию"
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_active'].label_attrs = {'class': 'form-check-label'}

class ProductsForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Задаем класс для кнопки "Создать версию"
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_active'].label_attrs = {'class': 'form-check-label'}

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

    