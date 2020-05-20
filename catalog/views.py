from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from catalog.models import Book,bookInstance,Author,Language,Genre
from django.views import generic
from django.urls import reverse,reverse_lazy
import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView,UpdateView,DeleteView

@login_required
def index(request):
    num_books=Book.objects.all().count()
    num_instances=bookInstance.objects.all().count()
    num_instances_available=bookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.all().count()
    num_visits=request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1
   # del request.session['num_visits']
   # request.session.modified = True
    num_genres_a=Genre.objects.filter(name__icontains='a').count()
    print("helooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",num_visits)
    #print(num_authors)
    #print(num_instances,num_instances_available,num_books)
    context={
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_visits':num_visits,
    }
    return render(request,'index.html',context=context)

class BookListView(LoginRequiredMixin,generic.ListView):
    model=Book
    context_object_name='list'
    template_name='book.html'
    paginate_by=10

class BookDetailView(generic.DetailView):
    model=Book
    template_name='Book_detail.html'

class AuthorListView(LoginRequiredMixin,generic.ListView):
    model=Author
    template_name='authors.html'
    context_object_name='list'
    paginate_by=10

class AuthorDetailView(generic.DetailView):
    model=Author
    template_name='author_detail.html'
    context_object_name='list'

#class MyView(LoginRequiredMixin, AuthorListView):
   # print("Chal ja bhai bas bhai dil se bura lagta hai")
 #   login_url = 'login/'
  #  redirect_field_name = 'redirect_to'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model=bookInstance
    template_name='bookinstance_list_borrowed_user.html'
    paginate_by=10

    def get_queryset(self):
        return bookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        #print(bookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back'))


class BorrowedBooksListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model=bookInstance
    template_name='borrowed_books_list.html'
    paginate_by=10

    def get_queryset(self):
        return bookInstance.objects.filter(status__exact='o').order_by('due_back')
  
from catalog.forms import RenewalBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    book_instance=get_object_or_404(bookInstance,pk=pk)
    print("The function is being called so no errors!",book_instance)
    if request.method=='POST':
        form=RenewalBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back=form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('borrowedBooks'))

    else:
        proposed_renewal_date=datetime.date.today()+datetime.timedelta(weeks=3)
        form=RenewalBookForm(initial={'renewal_date':proposed_renewal_date })

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model=Author
    fields='__all__'
    initial={'date_of_death':'05/01/2019'}
    template_name='author_form.html'

class AuthorUpdate(UpdateView):
    model=Author
    fields=['first_name','last_name','date_of_birth','date_of_death']
    template_name='author_form.html'

class AuthorDelete(DeleteView):
    model=Author
    success_url=reverse_lazy('authors')
    template_name='author_confirm_delete.html'