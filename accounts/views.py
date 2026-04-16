from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.db.models import Count
from books.models import Book
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import localtime
from .forms import ProfileUpdateForm


def generate_username_from_email(email):
    base_username = email.split('@')[0]
    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not first_name or not email or not password1 or not password2:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'accounts/register.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'accounts/register.html')

        username = generate_username_from_email(email)

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, 'accounts/login.html')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')


@login_required
def profile_view(request):
    user_obj = request.user

    total_books = getattr(user_obj, "books", []).count() if hasattr(user_obj, "books") else 0

    from books.models import Book

    user_books = Book.objects.filter(owner=user_obj)
    total_books = user_books.count()
    reading_books = user_books.filter(status="reading").count()
    planned_books = user_books.filter(status="plan_to_read").count()
    completed_books = user_books.filter(status="completed").count()

    favorite_genre_obj = (
        user_books.values("genre")
        .order_by("genre")
    )

    favorite_genre = "Not enough data"
    if user_books.exists():
        genre_counts = {}
        for book in user_books:
            genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1
        favorite_genre = max(genre_counts, key=genre_counts.get)

    insights = [
        f"You have {total_books} books in your library.",
        f"You completed {completed_books} book(s).",
        f"You are currently reading {reading_books} book(s).",
        f"You planned {planned_books} book(s) for later.",
        f"Your favorite genre is {favorite_genre}."
    ]

    member_since = localtime(user_obj.date_joined).strftime("%b %Y")

    if completed_books >= 10:
        reader_status = "Advanced Reader"
    elif completed_books >= 5:
        reader_status = "Consistent Reader"
    elif reading_books > 0:
        reader_status = "Active Reader"
    else:
        reader_status = "Casual Reader"

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=user_obj)

    context = {
        "user_obj": user_obj,
        "form": form,
        "gender": request.GET.get("gender", "female"),
        "favorite_genre": favorite_genre,
        "total_books": total_books,
        "reading_books": reading_books,
        "planned_books": planned_books,
        "completed_books": completed_books,
        "insights": insights,
        "member_since": member_since,
        "reader_status": reader_status,
    }

    return render(request, "accounts/profile.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('logged_out.html')