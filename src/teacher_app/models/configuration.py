from django.db import models
from django.utils import timezone
import uuid


class Configuration(models.Model):
    user = models.ForeignKey(
        "teacher_app.User", related_name="users", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    comment = models.CharField(max_length=1024, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=256, null=True, blank=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.pk:
            self.date_created = timezone.now()
            self.uuid = uuid.uuid4()
        super(Configuration, self).save()

    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурации"

    def __str__(self):
        if self.name:
            return self.name
        return str(self.uuid)


class ConfigurationStatistics(models.Model):
    student = models.ForeignKey(
        "teacher_app.Student",
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="Студент",
    )
    file = models.FileField(
        default=None, null=True, verbose_name="Файл с результатами проверки"
    )
    time_started = models.DateTimeField(verbose_name="Время начала")
    time_ended = models.DateTimeField(
        null=True, blank=True, verbose_name="Время окончания"
    )
    configuration = models.ForeignKey(
        "teacher_app.Configuration",
        on_delete=models.CASCADE,
        related_name="stats_configurations",
        verbose_name="Конфигурация",
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.pk:
            self.time_started = timezone.now()
        super(ConfigurationStatistics, self).save()

    class Meta:
        verbose_name = "Статистика конфигурации"
        verbose_name_plural = "Статистика конфигурации"
