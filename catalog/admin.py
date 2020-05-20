from django.contrib import admin
from .models import Book,bookInstance,Author,Genre,Language

# Register your models here.
#admin.site.register(Book)
#admin.site.register(bookInstance)
admin.site.register(Genre)
admin.site.register(Language)

#admin.site.register(Author)
#Define Admin Class
class BooksInline(admin.TabularInline):
    model=Book
    extra=0

class AuthorAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','date_of_birth','date_of_death')
    fields=['first_name','last_name',('date_of_birth','date_of_death')]
    inlines=[BooksInline]
   
admin.site.register(Author,AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = bookInstance
    extra=0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(bookInstance)
class bookInstanceAdmin(admin.ModelAdmin):
    list_display=('book','status','borrower','due_back','id')
    list_filter=('status','due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )




