from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg

import json

from .models import Book, Review, Author, Category
from .forms import BookForm, ReviewForm, AuthorForm, CategoryForm


class BookListView(ListView):
    model = Book
    template_name = "index.html"
    context_object_name = "books"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        category_id = self.request.GET.get("category")

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["query"] = self.request.GET.get("q", "")
        context["category_id"] = self.request.GET.get("category", "")
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(book=self.object)
        paginator = Paginator(reviews, 3)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["review_form"] = ReviewForm()
        return context


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'add_book.html'
    success_url = '/'


class AddAuthorView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'add_author.html'
    success_url = '/'


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    success_url = '/'


@csrf_exempt
@login_required
def add_review(request, book_id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        rating = data.get("rating")

        if content and rating:
            book = get_object_or_404(Book, pk=book_id)
             # Check if the user has already reviewed this book
            existing_review = Review.objects.filter(book=book, reviewer=request.user).first()
            if existing_review:
                return JsonResponse({"success": False, "message": "You have already reviewed this book."})
            review = Review.objects.create(
                book=book,
                reviewer=request.user,
                content=content,
                rating=rating,
            )
            review.save()
            book.refresh_from_db()  # Refresh the book to get the updated average rating
            return JsonResponse({"success": True, "new_average_rating": book.average_rating})
        else:
            return JsonResponse({"success": False, "message": "Content and rating are required."})
    return JsonResponse({"success": False, "message": "Invalid request method."})
