from django.db import models


class Iso(models.Model):
    iso = models.CharField(max_length=3)

    class Meta:
        db_table = 'iso'

    def __str__(self):
        return self.iso


class Language(models.Model):
    language_name = models.TextField()
    language_of = models.TextField()
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    alternate_names = models.TextField()
    autonym = models.TextField()
    user_population = models.TextField()
    location = models.TextField()
    language_maps = models.TextField()
    language_status = models.TextField()
    classification = models.TextField()
    dialects = models.TextField()
    typology = models.TextField()
    language_use = models.TextField()
    language_development = models.TextField()
    language_resource = models.TextField()
    writing = models.TextField()
    other_comments = models.TextField()

    class Meta:
        db_table = 'language'

    def __str__(self):
        return f'name: {self.language_name}; iso: {self.iso}'


class MapPoint(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    north = models.FloatField()
    south = models.FloatField()
    east = models.FloatField()
    west = models.FloatField()

    class Meta:
        db_table = 'map_point'

    def __str__(self):
        return str(self.iso)
