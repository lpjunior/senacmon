from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def balance_view(request):
    return render(request, "wallet/balance.html", {"balance": 100})

@login_required()
def transactions_view(request):
    return render(request, "wallet/transactions.html", {"transactions": []})