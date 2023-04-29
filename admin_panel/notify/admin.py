from django.contrib import admin
from notify.models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'type', 'created', 'modified',)
    list_filter = ('modified', 'created',)
    search_fields = ('title',)
    exclude = ('source', 'status',)

