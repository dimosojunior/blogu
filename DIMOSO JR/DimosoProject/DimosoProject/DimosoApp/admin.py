from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from DimosoApp.models import *


# Register your models here.
class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'company_name', 'profile_image', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'first_name', 'middle_name', 'last_name', 'company_name', 'phone', 'profile_image', 'password1', 'password2'),
        }),
    )

    ordering=('email',)



class PostAdmin(admin.ModelAdmin):
	list_display = ["title_tag", "name" ,"post_date"]
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "numbers"]
	prepopulated_fields={'slug':('name',)}

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["user", "facebook_url", "instagram_url" ,"whatsapp_url"]

class UploadFilesAdmin(admin.ModelAdmin):
    list_display = ["name", "cover", "owner", "year"]

class FileCourseAdmin(admin.ModelAdmin):
    list_display = ["name", "year"]
    prepopulated_fields={'slug':('name',)}

class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "date_created"]

class chatMessagesAdmin(admin.ModelAdmin):
    list_display = ["user_from", "user_to", "date_created"]




admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Comment)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(UploadFiles, UploadFilesAdmin)
admin.site.register(FileCourse, FileCourseAdmin)

admin.site.register(Room)
admin.site.register(Messages)
admin.site.register(Message, MessageAdmin)
admin.site.register(chatMessages, chatMessagesAdmin)