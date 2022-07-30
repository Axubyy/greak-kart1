from django.contrib import admin

from store.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'stock', 'is_available',
                    'category', 'price', 'created_date', ]
    prepopulated_fields = {'slug': ('product_name',)}


# Register your models here.
admin.site.register(Product, ProductAdmin)
