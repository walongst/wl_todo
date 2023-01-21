from django import forms
from .models import Ticket 
from .admin import UserExtend

class NewTicket(forms.ModelForm):

    def __init__(self,user):
        self.business.queryset=business.objects.filter(client.id=userextend.client_id)

    class Meta:
        model=Ticket
        fields = ('subject','business')