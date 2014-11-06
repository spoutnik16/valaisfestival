# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from associations.models import Association, RegionChild2
from crm.models import CustomUser



# Create your models here.
class Artiste(models.Model):
    name = models.CharField(max_length=512)
    association = models.ManyToManyField(Association)
    role = models.CharField(max_length=512,
                            null=True,
                            blank=True)
    fonction = models.CharField(max_length=512,
                                null=True,
                                blank=True)
    allowed_users = models.ManyToManyField(CustomUser,
                                           verbose_name=_('utilisateur authorise'),
                                           null=True,
                                           blank=True)
    status = models.SmallIntegerField(verbose_name=_("status"),
                                      help_text=_(
                                          "0 = en création, 1 = en validation, 3 = public, "
                                          "4 = exporté vers le cahier spécial"),
                                      blank=True,
                                      null=True)

    class Meta:
        verbose_name = _("artiste")
        verbose_name_plural = _("artistes")

    def __str__(self):
        return self.name


class CategorieSpectacle(models.Model):
    name = models.CharField(max_length=512,
                            verbose_name=_("categorie"))
    parent = models.ForeignKey("self",
                               null=True,
                               blank=True)

    class Meta:
        verbose_name = _('categorie')
        verbose_name_plural = _('categorie')

    def __str__(self):
        return self.name


class Festival(models.Model):
    name = models.CharField(max_length=512)
    startdate = models.DateField()
    enddate = models.DateField()

    class Meta:
        verbose_name = _("festival")
        verbose_name_plural = _("festivals")

    def __str__(self):
        return self.name


class Spectacle(models.Model):
    name = models.CharField(max_length=512,
                            help_text=_("le titre du spectacle"),
                            verbose_name=_('nom du spectacle'))
    associations = models.ManyToManyField(Association,
                                          help_text=_("associations participantes"),
                                          verbose_name=_('participant'),
                                          null=True,
                                          blank=True)
    website = models.CharField(max_length=512,
                               null=True,
                               blank=True,
                               verbose_name=_("le site web du spectacle"),
                               help_text=_("site web qui parle du spectacle, page de réservation"))
    participants = models.ManyToManyField(Artiste,
                                          null=True,
                                          blank=True,
                                          verbose_name=_("artiste"))
    presentation_cahier = models.TextField(max_length=600,
                                           null=True,
                                           blank=True,
                                           help_text=_("présentation qui apparaîtra dans le cahier spécial"),
                                           verbose_name=_("présentation courte"))
    presentation = models.TextField(help_text=_("présentation pour le site web, sans limitation de taille"),
                                    null=True,
                                    blank=True,
                                    verbose_name=_("présentation longue"))
    phone = models.CharField(max_length=25,
                             null=True,
                             blank=True,
                             help_text=_("le numéro auquel appelé pour réserver"),
                             verbose_name=_("numéro de téléphone pour les réservations"))
    photo = models.ImageField(upload_to="images-spectacle",
                              null=True,
                              blank=True,
                              verbose_name=_("image"))
    parent = models.ManyToManyField('self',
                                    null=True,
                                    blank=True,
                                    help_text=_(
                                        "dans le cas d'un festival, les différents événements qui s'y passent sont des "
                                        "sous-événements"),
                                    verbose_name=_("Festival"))
    status = models.SmallIntegerField(verbose_name=_("status"),
                                      blank=True,
                                      null=True,
                                      help_text=_(
                                          "0 = en création, 1 = en validation, 3 = public, 4 = exporté vers le cahier "
                                          "spécial"))
    old_id = models.IntegerField(help_text=_("n'existe plus"),
                                 blank=True,
                                 null=True)
    categorie = models.ForeignKey(CategorieSpectacle)
    allowed_user = models.ManyToManyField(CustomUser,
                                          null=True,
                                          blank=True,
                                          verbose_name=_("utilisateurs authorisés"))

    class Meta:
        verbose_name = _('spectacle')
        verbose_name_plural = _('spectacles')

    def __str__(self):
        return self.name


class Lieu(models.Model):
    name = models.CharField(max_length=512,
                            help_text=_("nom du lieu"),
                            verbose_name=_("lieu de la représentation"))
    # allowed_users = models.ManyToManyField(CustomUser,
    # null = True,
    # blank = True,
    # verbose_name = _('utilisateur authorisé'))
    phoneNumber = models.CharField(max_length=512,
                                   null=True,
                                   blank=True,
                                   verbose_name=_("numéro de téléphone du lieu"))
    city = models.CharField(max_length=512,
                            verbose_name=_("ville"))
    zipCode = models.CharField(max_length=64,
                               null=True,
                               blank=True,
                               verbose_name=_("code postal"))
    adress = models.CharField(max_length=512,
                              verbose_name=_("adresse"))
    adress2 = models.CharField(max_length=512,
                               null=True,
                               blank=True,
                               verbose_name=_("suite de l'adresse"))
    website = models.URLField(null=True,
                              blank=True,
                              verbose_name=_("site web"))
    region = models.ForeignKey(RegionChild2,
                               blank=True,
                               null=True,
                               verbose_name=_("commune"))
    status = models.SmallIntegerField(verbose_name=_("status"),
                                      null=True,
                                      blank=True,
                                      help_text=_(
                                          "0 = en création, 1 = en validation, 3 = public, 4 = exporté vers le cahier "
                                          "spécial"))
    lat = models.FloatField(null=True,
                            blank=True,
                            verbose_name=_("latitude"))
    long = models.FloatField(verbose_name=_("longitude"),
                             null=True,
                             blank=True)
    old_id = models.IntegerField(null=True,
                                 blank=True)
    """location = LocationField(based_fields=[city],
                             zoom=12,
                             default=Point(1,1),
                             verbose_name = _("Accès"),
                             help_text = _("Cliquez sur la carte"),
                             null = True,
                             blank = True)
    objects = models.GeoManager()"""

    class Meta:
        verbose_name = _('lieu')
        verbose_name_plural = _('lieux')

    def __str__(self):
        return self.name


class Representation(models.Model):
    lieu = models.ForeignKey(Lieu,
                             help_text=_("lieu où se passe le spectacle"),
                             verbose_name=_('lieu'),
                             null=True,
                             blank=True)
    spectacle = models.ForeignKey(Spectacle)
    datetime = models.DateTimeField()
    allowed_users = models.ManyToManyField(CustomUser,
                                           null=True,
                                           blank=True,
                                           verbose_name=_('utilisateur authorisé'))
    status = models.SmallIntegerField(verbose_name=_("status"),
                                      null=True,
                                      blank=True,
                                      help_text=_(
                                          "0 = en création, 1 = en validation, 3 = public, 4 = exporté vers le cahier "
                                          "spécial"))
    festival = models.ManyToManyField(Festival,
                                      null=True,
                                      blank=True,
                                      verbose_name=_('festival auquel participe le spectacle'))

    class Meta:
        verbose_name = _('représentation')
        verbose_name_plural = _('représentations')

    def __str__(self):
        return self.spectacle.name + ' à ' + self.lieu.name + ' à ' + self.datetime.__str__()