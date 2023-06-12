from django.contrib import admin

from teacher_app.admin.configuration import ConfigurationAdmin, ConfigurationStatisticsAdmin
from teacher_app.admin.limitation import LimitationAdmin
from teacher_app.models import Configuration
from teacher_app.models.configuration import ConfigurationStatistics
from teacher_app.models.limitation import *
admin.site.site_header = 'Административная панель экзаменатора'
admin.site.register(LimitationConfiguration)
admin.site.register(Limitation, LimitationAdmin)
admin.site.register(ConfigurationLimitationParameter)
admin.site.register(LimitationParameter)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(ConfigurationStatistics, ConfigurationStatisticsAdmin)
