from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre, Language
from .forms import RenewBookForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime

def index(request):
    '''View function for homepage of the site'''

    # Generate counts
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # no of available books
    num_available = BookInstance.objects.filter(status__exact='a').count()

    # no of authors
    num_authors = Author.objects.count()

    #

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_instances': num_instances,
        'num_available': num_available,
    }

    # render the html index.html with data in the context variable

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author


class BookInstanceListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model=BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user2.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model=BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    '''View function for renewing a specific bookinstance by librarian'''
    bookinstance = get_object_or_404(BookInstance,pk=pk)

    #if this is a POST request, process form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        #Check if form is valid
        if form.is_valid():
            bookinstance.due_back = form.cleaned_data['renewal_date']
            bookinstance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        default_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        default_form_data= {'renewal_date':default_renewal_date}
        form = RenewBookForm(initial = default_form_data)

    context = {
        'form':form,
        'bookinstance':bookinstance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)
 