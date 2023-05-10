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

    list_display = ['email','is_drag_performer',]

# class DragProfileAdminForm(forms.ModelForm):
#     class Meta:
#         model = DragProfile
#         fields = "__all__"

#     def clean_owner(self):
#         if self.

class DragProfileAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'stage_name','owner_link','following','followers','approved', 'city']
    list_editable = ['approved']
    list_per_page=20
    list_filter = ['approved', 'locked',]

    def stage_name(self, obj):
        return "{}".format(obj.owner.username)

    def owner_link(self, obj):
        url = reverse('admin:user_user_change', args=(obj.owner.id,))
        return format_html("<a href='{}'>{}</a>",url,obj.owner.email)
    
    def followers(self, obj):
        f_manager = FollowManager.objects.get(owner=obj.owner)
        return "{} followers".format(f_manager.count_followers())

    def following(self, obj):
        f_manager = FollowManager.objects.get(owner=obj.owner)
        return "{} DragProfiles".format(f_manager.count_following())

    def get_form(self, request, obj=None, **kwargs):
        profile_users = DragProfile.objects.all().values_list('owner',flat=True)
        form = super(DragProfileAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['owner'].queryset = User.objects.exclude(pk__in = profile_users)
        else:
            form.base_fields['owner'].queryset = User.objects.filter(pk = obj.owner.pk)
        return form
    

admin.site.site_header="Drag4me Admin Page"
admin.site.register(User,Useradmin)
admin.site.register(DragProfile,DragProfileAdmin)
admin.site.register(Transaction)
