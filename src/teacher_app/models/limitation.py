from django.db import models

from teacher_app.enums import LimitationType


class Limitation(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    type = models.CharField(
        max_length=256, choices=LimitationType.choices, verbose_name="Объекты"
    )
    function_name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ограничение"
        verbose_name_plural = "Ограничения"


class LimitationParameter(models.Model):
    parameter_name = models.CharField(max_length=256)
    parameter_in_code = models.CharField(max_length=256)
    limitation = models.ForeignKey(
        "teacher_app.Limitation", related_name="limitations", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.parameter_name

    class Meta:
        verbose_name = "Параметр ограничения"
        verbose_name_plural = "Параметры ограничения"


class ConfigurationLimitationParameter(models.Model):
    limitation_parameter = models.ForeignKey(
        "teacher_app.LimitationParameter",
        related_name="limitation_parameters",
        on_delete=models.CASCADE,
        verbose_name="параметр",
    )

    value = models.CharField(max_length=255, verbose_name="Значение")
    configuration = models.ForeignKey(
        "teacher_app.Configuration",
        related_name="limitation_configurations",
        on_delete=models.CASCADE,
        verbose_name="Конфигурация",
    )
    check_type = models.IntegerField(default=0, verbose_name="Тип проверки")

    @property
    def limitation_name(self):
        return self.limitation_parameter.limitation.name

    class Meta:
        verbose_name = "Параметр ограничения для конфигурации"
        verbose_name_plural = "Параметры ограничения для конфигурации"

    limitation_name.fget.short_description = "Название проверки"


class LimitationConfiguration(models.Model):
    configuration = models.ForeignKey(
        "teacher_app.Configuration",
        related_name="configurations",
        on_delete=models.CASCADE,
    )
    limitation = models.ForeignKey(
        "teacher_app.Limitation",
        related_name="config_limitations",
        on_delete=models.CASCADE,
    )
