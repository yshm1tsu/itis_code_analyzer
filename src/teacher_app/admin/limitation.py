from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpResponseRedirect

from teacher_app.models import Configuration
from teacher_app.models.limitation import (
    LimitationConfiguration,
    LimitationParameter,
    ConfigurationLimitationParameter,
)


class LimitationAdmin(ModelAdmin):
    @admin.action(description="Выбрать проверки для конфигурации")
    def choose_for_limitation(modeladmin, request, queryset):
        configuration = Configuration.objects.create(
            user=request.user,
        )
        for limitation in queryset:
            LimitationConfiguration.objects.create(
                limitation=limitation, configuration=configuration
            )
        for limitation in queryset:
            parameters = LimitationParameter.objects.filter(limitation=limitation)
            for parameter in parameters:
                ConfigurationLimitationParameter.objects.create(
                    limitation_parameter=parameter,
                    value="*" if parameter.parameter_name == "*" else "",
                    configuration=configuration,
                )

        return HttpResponseRedirect(
            f"/admin/teacher_app/configuration/{configuration.pk}/change/"
        )

    actions = [choose_for_limitation]
    list_display = ["name", "type"]
