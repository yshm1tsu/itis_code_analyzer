from django.contrib.admin import ModelAdmin, TabularInline
from django.http import HttpResponseRedirect
from django.urls import resolve

from teacher_app.models.configuration import ConfigurationStatistics
from teacher_app.models.limitation import ConfigurationLimitationParameter
from teacher_app.utils import create_config_file


class ConfigurationLimitationParameterInline(TabularInline):
    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs["object_id"])
        return None

    def get_queryset(self, request):
        parent_object = self.get_parent_object_from_request(request)
        return ConfigurationLimitationParameter.objects.filter(
            configuration=parent_object
        )

    model = ConfigurationLimitationParameter
    readonly_fields = ["limitation_name", "limitation_parameter"]
    can_delete = False
    extra = 0
    max_num = 0


class ConfigurationStatisticsInline(TabularInline):
    model = ConfigurationStatistics

    def has_change_permission(self, request, obj=None):
        return False

    can_delete = False
    extra = 0
    max_num = 0


class ConfigurationAdmin(ModelAdmin):
    inlines = [ConfigurationLimitationParameterInline, ConfigurationStatisticsInline]
    change_form_template = "config_change_form.html"

    def response_change(self, request, obj):
        if "_create-configuration" in request.POST:
            filename = create_config_file(obj.pk)
            obj.filename = filename
            obj.save()
            self.message_user(request, "Configuration created")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    readonly_fields = ["date_created", "uuid"]


class ConfigurationStatisticsAdmin(ModelAdmin):
    readonly_fields = ["student", "file", "time_started", "time_ended", "configuration"]

    list_display = ["student", "file", "time_started", "time_ended", "configuration"]
