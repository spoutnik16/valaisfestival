# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class CustomUser(models.Model):
    phone = models.CharField(max_length=50,
                             verbose_name=_("numéro de téléphone"),
                             null=True,
                             blank=True)
    user = models.ForeignKey(User,
                             blank=True,
                             null=True)