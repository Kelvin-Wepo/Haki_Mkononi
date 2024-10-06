from django.contrib import admin
from .models import Case, Document

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('category', 'status')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    raw_id_fields = ('created_by', 'assigned_to')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('case', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('case__title',)
    raw_id_fields = ('case',)
