import datetime

from django.db import models
from django.utils import timezone

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from rest_framework import serializers
from django.utils.html import format_html


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):              # __unicode__ on Python 2
        return self.question_text
    def was_published_recently(self):
	    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    status = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            0xff4342,
            self.question,
            self.pub_date,
        )
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    name = models.CharField(max_length=200, default="")
    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text

class TestChoice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    name = models.CharField(max_length=200, default="")
    pic = models.FileField()
    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text





class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=6)
    birthday = models.DateField()

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            self.color_code,
            self.first_name,
            self.last_name,
        )
    def birth_date_view(self, obj):
         return obj.birth_date

    birth_date_view.empty_value_display = 'unknown'
