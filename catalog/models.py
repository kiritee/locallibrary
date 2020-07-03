from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date


class Genre(models.Model):
    '''Model to represent book genres'''
    name = models.CharField(
        max_length=50, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        '''string for representing the model object'''
        return self.name


class Book(models.Model):
    '''Class to define properties of a book. Not a specific copy though'''
    title = models.CharField(max_length=200, help_text='Title of book')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    imprint = models.CharField(
        max_length=30, help_text='Enter publisher imprint')
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for the book')
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()])



class BookInstance(models.Model):
    '''Model to represent an individual book can be loaned from the library'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library'
    )
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('r', 'Reserved'),
        ('o', 'On-Loan'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availability'
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank= True)

    class Meta:
        ordering = ['id','status','due_back']
        permissions = (('can_mark_returned','Return Book'),)

    def __str__(self):
        '''String for representing the Model object'''
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() >self.due_back:
            return True
        return False

class Author(models.Model):
    '''Model to represent authors'''
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField('Born', null = True, blank = True)
    date_of_death = models.DateField('Died', null = True, blank = True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        '''Returns the url to access a particular author instance'''
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    '''Model to represent languages'''
    name = models.CharField(
        max_length=50, help_text='Enter the language the book is written in')

    def __str__(self):
        '''string for representing the model object'''
        return self.name
    