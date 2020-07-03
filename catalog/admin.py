from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Language, Book, BookInstance

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','language','isbn','display_genre')
    inlines = [BookInstanceInline]
    pass

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name','date_of_birth','date_of_death')
    fields = ('first_name','last_name',('date_of_birth','date_of_death'))
    inlines = [BookInline]
    pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower','due_back','id')
    list_filter = ('status','due_back')
    fieldsets = (
        (None, {
            "fields": ('id','book')
        }),
        ('Availability',{
            "fields": ('status', 'due_back','borrower')
        }),
    )
    
    pass

admin.site.register(Genre)
admin.site.register(Language)
