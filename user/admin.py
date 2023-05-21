from typing import Any, Optional
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from user.models import User, DragProfile, FollowManager, Transaction
from django.urls import reverse
from django import forms
from django.utils.html import format_html
# Register your models here.


class Useradmin(admin.ModelAdmin):

    list_display = ['email','is_branch_account', 'resetter', 'qr_id']

    def is_branch_account(self, obj):
        return bool(obj.is_drag_performer)

# class DragProfileAdminForm(forms.ModelForm):
#     class Meta:
#         model = DragProfile
#         fields = "__all__"

#     def clean_owner(self):
#         if self.

class DragProfileAdmin(admin.ModelAdmin):

    list_display = ['__str__','branch_user_mail','approved']
    list_editable = ['approved']
    list_per_page=20
    list_filter = ['approved', 'locked',]

    def stage_name(self, obj):
        return "{}".format(obj.owner.username)

    def branch_user_mail(self, obj):
        return obj.owner.email
    
    def get_form(self, request, obj=None, **kwargs):
        profile_users = DragProfile.objects.all().values_list('owner',flat=True)
        form = super(DragProfileAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['owner'].queryset = User.objects.exclude(pk__in = profile_users).order_by('-pk')
        else:
            form.base_fields['owner'].queryset = User.objects.filter(pk = obj.owner.pk)
        return form
    

admin.site.site_header="Arole Playstation Admin Page"
admin.site.register(User,Useradmin)
admin.site.register(DragProfile,DragProfileAdmin)
admin.site.register(Transaction)
