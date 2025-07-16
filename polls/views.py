from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods

from polls.models import Quote


def index(request):
    return render(request, "index.html")


def change_quote(request):
    new_quote = Quote.get_random_quote()
    if(new_quote == None):
        return render(request, "quote.html")
    Quote.increment_view(new_quote.id)
    return redirect("polls:get_quote_by_id", quote_id=new_quote.id)


@require_http_methods(["GET"])
def get_quote_by_id(request, quote_id):
    new_quote = get_object_or_404(Quote, id=quote_id)
    return render(request, "quote.html", {"quote": new_quote})


@require_http_methods(["POST"])
def get_quote_by_id_incr(request, quote_id):
    new_quote = get_object_or_404(Quote, id=quote_id)
    Quote.increment_view(quote_id)
    return redirect("polls:get_quote_by_id", quote_id=new_quote.id)

def add_quote(request):
    if request.method == "POST":
        print(request.POST)
        source = request.POST.get('source')
        text = request.POST.get('text')
        weight = int(request.POST.get('weight', 0))
        try:
            _ = Quote.create(source, text, weight)
        except ValidationError as e:
            return render(request, "add_quote.html", {"messages": e.messages})
        return redirect("polls:index")
    return render(request, "add_quote.html")


@require_http_methods(["POST"])
def update_quote_weight(request, quote_id):
    if request.method == 'POST':
        quote = get_object_or_404(Quote, id=quote_id)
        weight = request.POST.get('new_weight')
        Quote.set_weight(quote.id, weight)
        return redirect("polls:get_quote_by_id", quote_id=quote.id)


@require_http_methods(["POST"])
def like(request, quote_id):
    Quote.like_quote(quote_id)
    return redirect("polls:get_quote_by_id", quote_id=quote_id)


@require_http_methods(["POST"])
def dislike(request, quote_id):
    Quote.dislike_quote(quote_id)
    return redirect("polls:get_quote_by_id", quote_id=quote_id)

@require_http_methods(["GET"])
def get_top_quotes(request):
    ALLOWED_ORDER_FIELDS = ['views', 'likes', 'dislikes', 'weight', 'text', 'source']
    order_by = request.GET.get('order', 'likes')
    if order_by not in ALLOWED_ORDER_FIELDS:
        return JsonResponse({'error': 'Invalid order field'}, status=400)
    desc = request.GET.get('desc', 'true').lower() == 'true'
    number = request.GET.get('number_max', 10)
    if number:
        number = int(number)
    else:
        number = 10
    ordering = f"-{order_by}" if desc else order_by
    ordered_queryset = Quote.get_top_quotes(ordering, number)
    return render(request, "top_quotes.html", {"top_quotes": ordered_queryset})
