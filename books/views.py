from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from .forms import BookForm
from .models import Book
from collections import Counter
from django.db.models import Q
import random

def home_view(request):
    return render(request, 'home.html')
from django.db.models import Q

@login_required
def book_list_view(request):
   
    if request.user.is_superuser:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(owner=request.user)

    q = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()
    status = request.GET.get('status', '').strip()

    print("---- DEBUG BOOK FILTER ----")
    print("q =", q)
    print("genre =", genre)
    print("status =", status)
    print("all statuses in db =", list(Book.objects.values_list('status', flat=True)))
    print("before filters count =", books.count())

    if q:
        books = books.filter(
            Q(title__icontains=q) | Q(author__icontains=q)
        )

    if genre:
        books = books.filter(genre=genre)

    if status:
        books = books.filter(status=status)

    print("after filters count =", books.count())
    print("---------------------------")

    return render(request, 'books/book_list.html', {
        'books': books,
    })

def get_recommended_books_for_user(user):
    user_books = Book.objects.filter(owner=user)

    if not user_books.exists():
        return []

    favorite_genre_data = (
        user_books.values("genre")
        .annotate(total=Count("id"))
        .order_by("-total")
        .first()
    )

    if not favorite_genre_data:
        return []

    favorite_genre = favorite_genre_data["genre"]
    user_book_titles = user_books.values_list("title", flat=True)

    recommendations = Book.objects.filter(
    owner=user,
    status='plan_to_read'
).order_by('-created_at')[:4]
    
    return recommendations
@login_required
def library_insights(request):
    if request.user.is_superuser:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(owner=request.user)

    total_books = books.count()
    completed_books = books.filter(status='completed').count()
    reading_books = books.filter(status='reading').count()
    planned_books = books.filter(status='planned').count()

    genres = [book.genre for book in books if book.genre]
    most_read_genre = None
    if genres:
        most_read_genre = Counter(genres).most_common(1)[0][0]

    insights = []

    if total_books == 0:
        insights.append("No books have been added yet.")
    else:
        insights.append(f"You have {total_books} books in your library.")
        insights.append(f"{completed_books} books are completed.")
        insights.append(f"{reading_books} books are currently being read.")
        insights.append(f"{planned_books} books are planned for future reading.")

        if most_read_genre:
            insights.append(f"{most_read_genre} is the most read genre.")

        if completed_books > reading_books and completed_books > planned_books:
            insights.append("You tend to finish the books you add.")
        elif reading_books > completed_books:
            insights.append("You are actively reading several books.")
        elif planned_books > 0:
            insights.append("You like planning your future reading list.")

        # 1. Active reader
        if total_books >= 10:
            insights.append("You are an active reader with a large collection.")

        # 2. Low activity
        if total_books > 0 and total_books <= 3:
            insights.append("You are just starting to build your reading habit.")

        # 3. Reading vs Completed ratio
        if completed_books > 0 and total_books > 0:
            completion_rate = round ((completed_books / total_books) * 100, 1)
            if completion_rate >= 70:
                insights.append("You have a high completion rate for your books.")
            elif completion_rate < 30:
                insights.append("You may want to focus on finishing more books.")

        # 4. No reading books
        if reading_books == 0 and total_books > 0:
            insights.append("You are not currently reading any books.")

        # 5. Favorite genre suggestion
        if most_read_genre:
            insights.append(f"You might enjoy exploring more {most_read_genre} books.")

        # 6. Balanced reader
        if reading_books > 0 and completed_books > 0:
            insights.append("You maintain a balanced reading habit.")

    context = {
        'total_books': total_books,
        'completed_books': completed_books,
        'reading_books': reading_books,
        'planned_books': planned_books,
        'most_read_genre': most_read_genre,
        'insights': insights,
    }

    return render(request, 'books/library_insights.html', context)

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        books = Book.objects.select_related('owner').all()
        users_count = Book.objects.values('owner').distinct().count()
    else:
        books = Book.objects.filter(owner=request.user)
        users_count = 1

    recommendations = get_recommended_books_for_user(request.user)[:3]
    recent_books = books.order_by('-created_at')[:4]
    color_classes = ['color-blue', 'color-green', 'color-orange', 'color-red', 'color-purple']

    random.shuffle(color_classes)

    recommendation_cards = []
    for i, book in enumerate(recommendations):
        color = color_classes[i % len(color_classes)]
        recommendation_cards.append({
            'book': book,
            'color': color
        })


    context = {
        'books_count': books.count(),
        'users_count': users_count,
        'completed_count': books.filter(status='completed').count(),
        'recommendation_cards': recommendation_cards,
        'recent_books': recent_books,
    }

    return render(request, 'books/dashboard.html', context)



@login_required
def book_create_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            messages.success(request, 'Book added successfully.')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Add Book'})


@login_required
def book_update_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_superuser and book.owner != request.user:
        return HttpResponseForbidden('You do not have permission to edit this book.')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'books/book_form.html', {'form': form, 'title': 'Edit Book'})


@login_required
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_superuser and book.owner != request.user:
        return HttpResponseForbidden('You do not have permission to delete this book.')

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

