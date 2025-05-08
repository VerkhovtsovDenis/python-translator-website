from django.contrib import admin
from .models import SupportLanguage, History


@admin.register(SupportLanguage)
class SupportLanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'req_date', 'language')
    list_filter = ('language', 'req_date')
    search_fields = ('input_code', 'output_code')
    readonly_fields = ('req_date',)
