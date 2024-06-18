from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json

from .models import Book, Review
from .forms import BookForm, ReviewForm

class BookListView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(book=self.object)
        context['review_form'] = ReviewForm()
        return context

class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'add_book.html'
    success_url = '/'


@login_required
@csrf_exempt
def add_review(request, book_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data.get('rating')
        content = data.get('content')

        book = Book.objects.get(id=book_id)
        review = Review.objects.create(
            book=book,
            reviewer=request.user,
            content=content,
            rating=rating
        )

        return JsonResponse({
            'success': True,
            'reviewer': request.user.username,
            'rating': review.rating,
            'content': review.content
        })

    return JsonResponse({'success': False}, status=400)