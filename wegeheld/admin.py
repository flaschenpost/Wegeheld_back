from django.contrib import admin
from .models import *

@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'hexValue']
    list_editable=['name','hexValue']
    list_filter=['name']

@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display=['id','postalcode','name']
    list_editable=['name','postalcode']
    list_filter=['name','postalcode']


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display=['id', 'name']
    list_editable=['name']
    list_filter=['name']

@admin.register(Obstruction)
class ObstructionAdmin(admin.ModelAdmin):
    list_display=['id', 'name','remark']
    list_editable=['name', 'remark']
    list_filter=['name','remark']

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display=['id', 'name_map', 'name_app']
    list_editable=['name_map', 'name_app']
    list_filter=['name_map', 'name_app']

@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'town']
    list_editable=['name']
    list_display_links=['town']
    list_filter=['name']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display=['id', 'town', 'street','streetnumber']
    list_editable=['streetnumber']

@admin.register(Offense)
class OffenseAdmin(admin.ModelAdmin):
    list_display=['id','name','fee' ]
    list_editable=['name','fee']
    list_filter=['name']

@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display=['id','email','nickname','zip','city']
    list_editable=['email','nickname','zip','city']
    list_filter=['email','nickname','zip','city']


@admin.register(Funnysaying)
class FunnySayingAdmin(admin.ModelAdmin):
    list_display=['id','text','valid_offenses']
    list_editable=['text']
    list_filter=['text','valid_offenses']

@admin.register(EmailText)
class PublicAffairsOfficeAdmin(admin.ModelAdmin):
    list_display=['id','postalcode','offense','template', 'hidden']
    list_editable=['postalcode','offense','template', 'hidden']
    list_filter=['postalcode','offense']

@admin.register(PublicAffairsOffice)
class PublicAffairsOfficeAdmin(admin.ModelAdmin):
    list_display=['id','postalcode','email','name']
    list_editable=['postalcode','email','name']
    list_filter=['postalcode','email','name']

# Register your models here.
