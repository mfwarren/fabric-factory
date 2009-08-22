from django.contrib import admin
from factory.models import FabfileRecipe, Build

class FabfileRecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
class BuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'executed', 'success')

admin.site.register(FabfileRecipe, FabfileRecipeAdmin)
admin.site.register(Build, BuildAdmin)
