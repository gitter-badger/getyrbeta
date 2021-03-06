from django import forms

from django.forms.widgets import NumberInput

from account_info.models import User

from .models import Trip, TripLocation, TripMember, TripGuest, \
    Item, ItemOwner

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Field, Div
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'start_date', 'number_nights']

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-TripForm'
        self.helper.form_class = 'trip_forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'col-md-9'
        self.fields['number_nights'].label = 'Number of Nights'
        self.fields['title'].label = 'Trip Title'
        self.helper.layout = Layout (
            'title',
            Field('start_date', id='start_date'),
            HTML('''
                <div class="col-md-9">
                    <div class="date-picker">
                    	<div class="input">
                    		<div class="result">Select Date: <span></span></div>
                    		<button type=button><i class="fa fa-calendar"></i></button>
                    	</div>
                    	<div class="calendar"></div>
                    </div>
                </div>
            '''),
            'number_nights',
            FormActions(
                Submit('submit', '{{ submit_button_title }}', css_class='btn btn-success btn-lg click-disable'),
                HTML('<a class="btn btn-secondary" href="{% url cancel_button_path %}" name="cancel">Cancel</a>')
            )
        )

class LocationForm(forms.ModelForm):
    class Meta:
        model = TripLocation
        fields = ['trip', 'location_type', 'title', 'date',
            'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        location_type = kwargs.pop('location_type')
        super(LocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-LocationForm'
        self.helper.form_class = 'trip_forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.fields['title'].label = 'Title for Trip Plan'
        self.fields['date'].label = 'Date'
        self.fields['date'] = forms.ChoiceField(choices=choices)
        self.fields['latitude'].widget = NumberInput(attrs={
            'step': 'any',
            'max': 90,
            'min': -90
        })
        self.fields['longitude'].widget = NumberInput(attrs={
            'step': 'any',
            'max': 180,
            'min': -180
        })
        self.helper.layout = Layout (
            'title',
            Div(
                'latitude',
                'longitude',
                css_class='coordinate-fields'
            ),
            'date',
            Field('trip', type='hidden'),
            Field('location_type', type='hidden'),
            FormActions(
                Submit('submit', '{{ submit_button_title }}', css_class='btn btn-success btn-lg click-disable'),
                HTML('<a class="btn btn-secondary" href="{% url cancel_button_path trip_id %}" name="cancel">Cancel</a>')
            )
        )
        if location_type == TripLocation.BEGIN:
            self.helper['date'].wrap(Field, type='hidden')

class SearchForm(forms.Form):
    class Meta:
        fields = ['email_search']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'trip-member-search'
        self.helper.form_class = 'trip-forms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'search-field trip-info'
        self.helper.layout = Layout (
            FieldWithButtons('email_search', StrictButton("Search", css_class="btn-success", css_id="email-search-button"))
        )

    email_search = forms.EmailField(
        label='Enter email address below:',
        max_length=255,
        required=False
    )

class TripMemberForm(forms.ModelForm):
    class Meta:
        model = TripMember
        fields = []

class TripGuestForm(forms.ModelForm):
    class Meta:
        model = TripGuest
        fields = []

class ItemModelForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["description", "trip_id"]

    description = forms.CharField(
        max_length=100,
        help_text="description"
    )

    trip_id = forms.IntegerField(widget=forms.HiddenInput())

class ItemOwnerModelForm(forms.ModelForm):
    class Meta:
        model = ItemOwner
        fields = ["quantity", "item_id", "owner_id", "accept_reqd"]

    quantity = forms.IntegerField(min_value=0, max_value=999)
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    owner_id = forms.IntegerField(widget=forms.HiddenInput())
    accept_reqd = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False
    )
