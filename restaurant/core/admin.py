from django.contrib import admin
from .models import Category,Momo,Contact
# Register your models here.

admin.site.register(Category)
admin.site.register(Contact)

@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display=['id','title','desc','price','image']