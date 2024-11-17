from django import forms
from django.utils.safestring import mark_safe

class ShoelaceCheckBox(forms.Widget):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'shoelace-input'}
        if attrs:
            default_attrs.update(attrs)
        self.attrs = default_attrs
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs=self.attrs
        is_checked = 'checked' if value else ''
        shoelace_checkbox = f'''
            <div x-data="{{
                checked: { 'true' if value else 'false' }
            }}">
                <sl-checkbox
                    x-model="checked"
                    id="shoelace_{name}"
                    name="{name}"
                    { 'required' if attrs.get('required') else '' }
                    { is_checked }
                >
                    {attrs.get('label', '')}
                </sl-checkbox>
                <input type="hidden" name="{name}" :value="checked ? 'on' : ''">
            </div>
        '''
        return mark_safe(shoelace_checkbox)


class ShoelaceInput(forms.Widget):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'shoelace-input'}
        if attrs:
            default_attrs.update(attrs)
        self.attrs = default_attrs
        super().__init__(default_attrs)


    def render(self, name, value, attrs=None, renderer=None):
        attrs = self.attrs
        # Use Alpine.js x-model for seamless binding between Shoelace and hidden input
        shoelace_input = f'''
            <div x-data="{{ value: '{value or ''}' }}">
                <sl-input
                    x-model="value"
                    id="shoelace_{name}"
                    placeholder="{attrs.get('placeholder')}"
                    autocomplete="{attrs.get('autocomplete')}"
                    label="{attrs.get('label')}"
                    type="{attrs.get('type', 'text')}"
                    { 'required' if attrs.get('required') else '' }
                    { 'password-toggle' if attrs.get('password-toggle') else '' }
                    { 'clearable' if attrs.get('clearable') else '' }>
                </sl-input>
                <input type="hidden" name="{name}" :value="value">
            </div>
        '''
        return mark_safe(shoelace_input)
