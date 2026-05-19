from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Avg
import json
from datetime import timedelta

from brewsko_pos.utils import role_required
from .models import MenuItem, InventoryItem, CATEGORY_CHOICES
from .forms import InventoryItemForm, MenuItemForm, UserForm
from accounts.models import User
from cashier.models import Order


@role_required(['admin'])
def dashboard(request):
    today = timezone.localdate()
    today_orders = Order.objects.filter(created_at__date=today, status='completed')
    total_sales = today_orders.aggregate(s=Sum('total'))['s'] or 0
    order_count = today_orders.count()
    avg_order = today_orders.aggregate(a=Avg('total'))['a'] or 0
    low_stock_count = sum(1 for item in InventoryItem.objects.all() if item.status in ['low', 'critical'])

    weekly = [
        {
            'date': (today - timedelta(days=i)).strftime('%a'),
            'total': float(Order.objects.filter(created_at__date=today - timedelta(days=i), status='completed').aggregate(s=Sum('total'))['s'] or 0),
        }
        for i in range(6, -1, -1)
    ]

    hourly = [
        {
            'hour': f'{hour}:00',
            'count': Order.objects.filter(created_at__date=today, created_at__hour=hour).count(),
        }
        for hour in range(6, 23)
    ]

    context = {
        'total_sales': total_sales,
        'order_count': order_count,
        'avg_order': avg_order,
        'low_stock_count': low_stock_count,
        'weekly_data': json.dumps(weekly),
        'hourly_data': json.dumps(hourly),
        'today': today,
    }
    return render(request, 'panel/dashboard.html', context)


@role_required(['admin'])
def manage_menu(request):
    query = request.GET.get('q', '')
    show = request.GET.get('show', 'active')
    if show == 'achieved':
        items = MenuItem.objects.filter(achieved=True)
    else:
        items = MenuItem.objects.filter(achieved=False)
    if query:
        items = items.filter(name__icontains=query)

    context = {
        'items': items,
        'categories': CATEGORY_CHOICES,
        'query': query,
        'show_achieved': show == 'achieved',
        'form': MenuItemForm(),
    }
    return render(request, 'panel/menu.html', context)


@role_required(['admin'])
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added successfully.')
        else:
            messages.error(request, 'Please correct the menu item details.')
    return redirect('panel:menu')


@role_required(['admin'])
def edit_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully.')
        else:
            messages.error(request, 'Unable to update menu item.')
    return redirect('panel:menu')


@role_required(['admin'])
def delete_menu_item(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(MenuItem, pk=pk)
        item.delete()
    return redirect('panel:menu')


@role_required(['admin'])
def toggle_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    item.status = 'unavailable' if item.status == 'available' else 'available'
    item.save()
    return redirect('panel:menu')


@role_required(['admin'])
def achieve_menu_item(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(MenuItem, pk=pk)
        item.achieved = True
        item.save()
        messages.success(request, 'Menu item moved to Achieve list.')
    return redirect('panel:menu')


@role_required(['admin'])
def inventory(request):
    query = request.GET.get('q', '')
    show = request.GET.get('show', 'active')
    if show == 'achieved':
        items = InventoryItem.objects.filter(achieved=True)
    else:
        items = InventoryItem.objects.filter(achieved=False)
    if query:
        items = items.filter(name__icontains=query)

    context = {
        'items': items,
        'critical_count': sum(1 for item in items if item.status == 'critical'),
        'low_count': sum(1 for item in items if item.status == 'low'),
        'query': query,
        'show_achieved': show == 'achieved',
        'units': ['kg', 'L', 'pcs', 'pack'],
        'form': InventoryItemForm(),
    }
    return render(request, 'panel/inventory.html', context)


@role_required(['admin'])
def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item added successfully.')
        else:
            messages.error(request, 'Please correct the inventory details.')
    return redirect('panel:inventory')


@role_required(['admin'])
def edit_inventory_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated successfully.')
        else:
            messages.error(request, 'Unable to update inventory item.')
    return redirect('panel:inventory')


@role_required(['admin'])
def delete_inventory_item(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(InventoryItem, pk=pk)
        item.delete()
    return redirect('panel:inventory')


@role_required(['admin'])
def achieve_inventory_item(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(InventoryItem, pk=pk)
        item.achieved = True
        item.save()
        messages.success(request, 'Inventory item moved to Achieve list.')
    return redirect('panel:inventory')


@role_required(['admin'])
def security(request):
    tab = request.GET.get('tab', 'accounts')
    users = User.objects.all()
    completed = Order.objects.filter(status='completed')
    total_trans = completed.aggregate(s=Sum('total'))['s'] or 0
    cash_trans = completed.filter(payment_method='cash').aggregate(s=Sum('total'))['s'] or 0
    gcash_trans = completed.filter(payment_method='gcash').aggregate(s=Sum('total'))['s'] or 0
    transactions = completed.order_by('-created_at')[:50]

    context = {
        'users': users,
        'transactions': transactions,
        'total_transactions': total_trans,
        'cash_payments': cash_trans,
        'gcash_payments': gcash_trans,
        'active_tab': tab,
    }
    return render(request, 'panel/security.html', context)


@role_required(['admin'])
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['password']:
                messages.error(request, 'Password is required for new users.')
            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, 'A user with that username already exists.')
            else:
                form.save()
                messages.success(request, 'User created successfully.')
        else:
            messages.error(request, 'Please correct the user details.')
    return redirect('panel:security')


@role_required(['admin'])
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
        else:
            messages.error(request, 'Unable to update user.')
    return redirect('panel:security')


@role_required(['admin'])
def delete_user(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            user.delete()
    return redirect('panel:security')


@role_required(['admin'])
def get_menu_item_data(request, pk):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET required'}, status=405)
    item = get_object_or_404(MenuItem, pk=pk)
    return JsonResponse({
        'id': item.id,
        'name': item.name,
        'price': str(item.price),
        'category': item.category,
        'status': item.status,
    })


@role_required(['admin'])
def get_inventory_item_data(request, pk):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET required'}, status=405)
    item = get_object_or_404(InventoryItem, pk=pk)
    return JsonResponse({
        'id': item.id,
        'name': item.name,
        'stock': str(item.stock),
        'unit': item.unit,
        'min_level': str(item.min_level),
    })


@role_required(['admin'])
def get_user_data(request, pk):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET required'}, status=405)
    user = get_object_or_404(User, pk=pk)
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'password_display': '••••••••',
    })
