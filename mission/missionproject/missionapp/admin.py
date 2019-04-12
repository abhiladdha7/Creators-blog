from django.contrib import admin

# Register your models here.
from missionapp.models import Post,Comment,Category,UserProfile
from mediumeditor.widgets import MediumEditorTextarea


class MediumEditorAdmin(object):

    def formfield_for_dbfield(self, db_field, **kwargs):

        if not hasattr(self, 'mediumeditor_fields'):
            raise ValueError('mediumeditor_fields is required on model')

        if db_field.name in self.mediumeditor_fields:
            return db_field.formfield(widget=MediumEditorTextarea())
        return super(MediumEditorAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
