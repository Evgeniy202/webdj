from django.contrib import admin
from django.forms import ModelChoiceField
from .models import *


#hooks
class HooksAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'hooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#robs
class RobsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'rods'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#coils
class CoilsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'coils'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#cargo
class CargoAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'cargo'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#wobblers
class WobblersAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'wobblers'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#soft_baits
class Soft_baitsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'soft_baits'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#spinners
class SpinnersAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'spinners'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#corbs_and_lines
class Corbs_and_linesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'corbs_and_lines'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#groundbaits_ozzles
class Groundbaits_ozzelsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'groundbaits_ozzles'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#feeders
class FeedersAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'feeders'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#leashes
class LeashesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'leashes'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#fishing_accessories
class Fishing_accessoriesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug = 'fishing_accessories'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)

#Products category
admin.site.register(Hooks, HooksAdmin)
admin.site.register(Rods, RobsAdmin)
admin.site.register(Coils, CoilsAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Wobblers, WobblersAdmin)
admin.site.register(Soft_baits, Soft_baitsAdmin)
admin.site.register(Spinners, SpinnersAdmin)
admin.site.register(Corbs_and_lines, Corbs_and_linesAdmin)
admin.site.register(Groundbaits_ozzles, Groundbaits_ozzelsAdmin)
admin.site.register(Feeders, FeedersAdmin)
admin.site.register(Leashes, LeashesAdmin)
admin.site.register(Fishing_accessories, Fishing_accessoriesAdmin)
