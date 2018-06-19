from django.contrib import admin
# Register your models here.
from .models import Question
from .models import Choice
from .models import TestChoice
from .models import Poll
from .models import Person
from django.contrib.admin import DateFieldListFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.utils.html import format_html
from .DecadeBornListFilter import DecadeBornListFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.db import models


# admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(TestChoice)


# admin.site.register(Poll)

def make_published(modeladmin, request, queryset):
    print(request)
    print(queryset)
    print(modeladmin)
    queryset.update(status='p')


make_published.short_description = "Mark selected stories as published"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['question'],
        }),
        ('Date information', {
            'fields': ['pub_date', 'status', 'url'],
            'classes': ['collapse'],
        }),
    ]
    list_display = ('question', 'pub_date', 'colored_name', 'was_published_recently', 'status', 'show_url')
    '''
    list_filter = ['pub_date', 'question', ('pub_date', DateFieldListFilter),
                  # ('pub_date', DateRangeFilter),
                   ('pub_date', DateTimeRangeFilter),

                   ]
'''
    list_filter = ['question', 'status']
    advanced_filter_fields = ['question', 'status']

    search_fields = ['question']
    date_hierarchy = 'pub_date'
    actions = [make_published]

    def show_url(self, obj):
        return '<a href="%s">url </a>' % (obj.url)

    show_url.allow_tags = True


class ProfileAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('question', 'pub_date', 'colored_name', 'was_published_recently', 'status', 'show_url')
    advanced_filter_fields = ['question', 'status', 'pub_date']
    list_filter = [
        ('pub_date', DateTimeRangeFilter),
    ]

    def show_url(self, obj):
        return '<a href="%s">url </a>' % (obj.url)
    show_url.allow_tags = True
#
admin.site.register(Poll, ProfileAdmin)


class PersonAdmin(admin.ModelAdmin):
    # list_filter = [('birthday', DecadeBornListFilter)]
    list_display = ['colored_name']
    list_filter = (DecadeBornListFilter,)
    pass


admin.site.register(Person, PersonAdmin)
