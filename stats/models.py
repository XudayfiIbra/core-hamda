from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Statistic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse("stats:dashboard", kwargs={"slug": self.slug})

    def data(self):
        return self.dataitem_set.all()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DataItem(models.Model):
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    owner = models.CharField(max_length=200)

    def __str__(self):
        return f"Data for {self.owner}: {self.value}"
