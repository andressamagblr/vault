# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ActionloggerConfig(AppConfig):
    name = 'actionlogger'
    verbose_name = _("Actionlogger")
