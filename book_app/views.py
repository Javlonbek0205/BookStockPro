from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewCreateForm, AdditionalInfoCreateForm, BookCreateForm
from book_app.models import Book, Review, AdditionalInfo


# Create your views here.
@login_required
def book_list_view(request):
    books = Book.objects.all().order_by('-id')
    context = {'books': books}
    return render(request, 'book_list.html', context)

@login_required
def my_book_list_view(request):
    books = Book.objects.filter(owner=request.user).order_by('-id')
    context = {'books': books}
    return render(request, 'my_book_list.html', context)

@login_required
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    categories = book.category.all()
    additional_info = AdditionalInfo.objects.filter(book=book).first()
    reviews = Review.objects.filter(book=book).order_by('-created_at')
    review_form = ReviewCreateForm(request.POST)
    average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    average_rating = round(average_rating)
    if request.method in ('POST', 'GET'):
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=pk)
    context = {'book': book,
               'additional_info': additional_info,
               'reviews':reviews,
               'categories': categories,
               'review_form':review_form,
               'average_rating':average_rating}
    return render(request, 'book_detail.html', context)


@login_required
def book_create_view(request):
    book = BookCreateForm(request.POST, request.FILES or None)
    additional_info = AdditionalInfoCreateForm(request.POST or None)

    if request.method == "POST" and  book.is_valid() and additional_info.is_valid():
        book_item = book.save(commit=False)
        book_item.owner = request.user
        book_item.save()
        book.save_m2m()

        additional_info_item = additional_info.save(commit=False)
        additional_info_item.book = book_item
        additional_info_item.save()
        additional_info.save_m2m()
        return redirect('book_list')
    context = {'book': book, 'additional_info': additional_info}
    return render(request, 'book_create.html', context)

@login_required
def book_update_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.owner != request.user:
        raise PermissionDenied("Siz faqat o'zingiz yaratgan kitobni taxrirlashingiz  mumkin!")

    additional_info = AdditionalInfo.objects.get(book=book)
    book_form = BookCreateForm(request.POST or None, request.FILES or None,  instance=book)
    additional_info_form = AdditionalInfoCreateForm(request.POST or None, instance=additional_info)

    if request.method == "POST" and book_form.is_valid() and additional_info_form.is_valid():
        book_instance = book_form.save(commit=False)
        book_instance.owner = request.user
        book_instance.save()
        book_form.save_m2m()

        additional_info_instance = additional_info_form.save(commit=False)
        additional_info_instance.book = book_instance
        additional_info_instance.save()
        additional_info_form.save_m2m()

        return redirect('book_detail', pk=book.pk)
    context = { 'book': book,
                'book_form': book_form,
                'additional_info_form': additional_info_form}
    return render(request, 'book_update.html', context)


@login_required
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.owner != request.user:
        raise PermissionDenied("Siz faqat o'zingiz yaratgan kitobni o'chirishingiz  mumkin!")
    if request.method == "POST" and book.owner == request.user:
        book.delete()
        return redirect('book_list')
    return render(request, 'book_delete.html', {'book': book})




