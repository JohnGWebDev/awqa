from django import forms
from django.utils.safestring import mark_safe

class ShoelaceSelect(forms.Widget):
    def __init__(self, choices=None, attrs=None):
        default_attrs = {'class': 'shoelace-select'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        self.choices = choices or []

    def render(self, name, value, attrs=None, renderer=None):
        # Merge self.attrs with additional attrs passed to render
        final_attrs = self.build_attrs(self.attrs, extra_attrs=attrs)
        
        # Ensure `value` is a string for consistent comparison
        value = str(value) if value is not None else ""

        # Build options
        options = ''.join(
            f'<sl-option value="{opt_value}" {"selected" if str(opt_value) == value else ""}>{opt_label}</sl-option>'
            for opt_value, opt_label in self.choices
        )

        # Render the Shoelace select
        shoelace_select = f'''
            <sl-select
                id="shoelace_{name}"
                name="{name}"
                placeholder="{final_attrs.get('placeholder', 'Select one')}"
                value="{value}"
                label="{final_attrs.get('label')}"
                { 'required' if final_attrs.get('required') else '' }
                { 'disabled' if final_attrs.get('disabled') else '' }>
                {options}
            </sl-select>
        '''
        return mark_safe(shoelace_select)
    

class ShoelaceTextArea(forms.Widget):
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
                <sl-textarea
                    x-model="value"
                    id="shoelace_{name}"
                    placeholder="{attrs.get('placeholder')}"
                    label="{attrs.get('label')}"
                    maxlength="{attrs.get('maxlength')}"
                    resize="none">
                </sl-textarea>
                <textarea style="display: none;" name="{name}" :value="value"></textarea>
            </div>
        '''
        return mark_safe(shoelace_input)


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
                    maxlength="{attrs.get('maxlength')}"
                    { 'required' if attrs.get('required') else '' }
                    { 'password-toggle' if attrs.get('password-toggle') else '' }
                    { 'clearable' if attrs.get('clearable') else '' }>
                </sl-input>
                <input type="hidden" name="{name}" :value="value">
            </div>
        '''
        return mark_safe(shoelace_input)
