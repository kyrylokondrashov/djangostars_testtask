from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView
from django import forms
from django.urls import reverse_lazy
from bookstore.models import Book,Author,Requests
from django.contrib.auth.decorators import *
from django.utils.decorators import method_decorator


# Create your views here.
class BookList(ListView):
    model = Book
    template_name = 'bookList.html'
    title = 'Main Page'

    def get(self, request, *args, **kwargs):
        queryset = Book.objects.all().order_by('-publish_date')
        self.request.session['ordered'] = 'asc'
        return render(request,self.template_name,{'object_list':queryset,'title':self.title})

    def post(self,request):
        queryset = Book.objects.all()
        if self.request.session['ordered'] == 'asc':
            self.request.session['ordered'] = 'desc'
            queryset = queryset.order_by('publish_date')
        else:
            self.request.session['ordered'] = 'asc'
            queryset = queryset.order_by('-publish_date')
        return render(request, self.template_name, {'object_list': queryset, 'title':self.title})

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BookDetails(DetailView):
    model = Book
    template_name = 'bookInfo.html'
    context_object_name = 'book'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'ISBN', 'price', 'publish_date']
        widgets = {
            'title' : forms.TextInput(attrs={'size' : '40',  'class':'form-control'}),
            'author': forms.Select(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={"type":"number",'class':'form-control'}),
            'ISBN': forms.TextInput(attrs={'size' : '40', 'class':'form-control'}),
            'publish_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class AddBook(CreateView):
    model = Book
    template_name = 'bookCreate.html'
    success_url = reverse_lazy('bookstore-main')
    form_class = BookForm

    @method_decorator(login_required)
    @method_decorator(permission_required('bookstore.change_book', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class EditBook(UpdateView):
    model = Book
    template_name = 'bookUpdate.html'
    form_class = BookForm

    @method_decorator(login_required)
    @method_decorator(permission_required('bookstore.change_book', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('bookstore-bookinfo', kwargs={'pk': self.kwargs['pk']})


class AuthorDetails(DetailView):
    model = Author
    template_name = 'authorInfo.html'
    context_object_name = 'author'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname']
        widgets = {
             'name': forms.TextInput(attrs={'size' : '40',  'class':'form-control'}),
             'surname': forms.TextInput(attrs={'size' : '40',  'class':'form-control'}),
        }


class AddAuthor(CreateView):
    model = Author
    template_name = 'authorCreate.html'
    success_url = reverse_lazy('bookstore-main')
    form_class = AuthorForm

    @method_decorator(login_required)
    @method_decorator(permission_required('bookstore.add_author', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class EditAuthor(UpdateView):
    model = Author
    template_name = 'authorUpdate.html'
    form_class = AuthorForm

    @method_decorator(login_required)
    @method_decorator(permission_required('bookstore.add_author', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('bookstore-authorinfo', kwargs={'pk': self.kwargs['pk']})


class RequestInfo(ListView):
    model = Requests
    template_name = 'requestList.html'
    title = 'Request Page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['list'] = Requests.objects.all().order_by('-time')[:10]
        except:
            context['list'] = Requests.objects.all().order_by('-time')
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required('is_superuser', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


