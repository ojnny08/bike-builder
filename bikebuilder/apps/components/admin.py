from django.contrib import admin
from .models import ComponentSubmission


@admin.register(ComponentSubmission)
class ComponentSubmissionAdmin(admin.ModelAdmin):
    list_display = ("url", "submitted_by", "processed", "created_at")
    list_filter = ("processed", "created_at")
    search_fields = ("url",)
    list_editable = ("processed",)
    readonly_fields = ("submitted_by", "created_at")
