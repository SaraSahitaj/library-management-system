from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from books.models import Book


@login_required
def ai_query_view(request):
    query = ""
    answer = ""
    table_data = []
    table_headers = []

    if request.user.is_superuser:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(owner=request.user)

    if request.method == "POST":
        query = request.POST.get("query", "").strip().lower()

        # 1. Who owns the most books (vetëm për admin ka kuptim)
        if "most books" in query or "who owns" in query:
            if request.user.is_superuser:
                top_owner = (
                    books.values("owner__username")
                    .annotate(total_books=Count("id"))
                    .order_by("-total_books")
                    .first()
                )

                if top_owner:
                    answer = f"{top_owner['owner__username']} owns the most books ({top_owner['total_books']})."
                else:
                    answer = "No books found."
            else:
                answer = "This question is only available for admin."

        # 2. Most popular book
        elif "most popular book" in query or "popular book" in query:
            popular_book = (
                books.values("title")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            if popular_book:
                answer = f"The most popular book is '{popular_book['title']}'."
            else:
                answer = "No books found."

        # 3. 5 most expensive
        elif "five most expensive" in query or "most expensive" in query:
            expensive_books = books.order_by("-price")[:5]

            if expensive_books:
                table_headers = ["Title", "Author", "Price", "Owner"]
                table_data = [
                    [b.title, b.author, b.price, b.owner.username]
                    for b in expensive_books
                ]
                answer = "Here are the most expensive books."
            else:
                answer = "No books found."

        # 4. Most common genre
        elif "genre" in query or "common genre" in query:
            genre_data = (
                books.values("genre")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            if genre_data:
                answer = f"The most common genre is '{genre_data['genre']}' ({genre_data['total']} books)."
            else:
                answer = "No books found."

        # 5. Completed books
        elif "completed books" in query:
            total_completed = books.filter(status="completed").count()
            answer = f"There are {total_completed} completed books."

        # 6. Total books
        elif "total books" in query or "how many books" in query:
            total_books = books.count()
            answer = f"There are {total_books} books."

        else:
            answer = "I do not understand this question yet."

    return render(request, "ai_assistant/ai_query.html", {
        "query": query,
        "answer": answer,
        "table_headers": table_headers,
        "table_data": table_data,
    })