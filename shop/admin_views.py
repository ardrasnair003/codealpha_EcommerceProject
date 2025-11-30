from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Product


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('admin_login')

        user = authenticate(username=user.username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, 'Admin login successful!')
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, 'Invalid admin credentials!')
            return redirect('admin_login')

    return render(request, 'Shop/login.html')



def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        if name and category and price and stock and image:
            # ✅ Create an instance, then call save() on it
            product = Product(
                name=name,
                category=category,
                price=price,
                stock=stock,
                image=image
            )
            product.save()  # ✅ instance method
            messages.success(request, "✅ Product added successfully!")
            return redirect('view_products')
        else:
            messages.error(request, "❌ Please fill in all required fields.")

    return render(request, 'Shop/add_product.html')


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name  # store name before deleting
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('view_products')

    # Render confirmation page if accessed directly
    return render(request, 'Shop/delete_product.html', {'product': product})


def view_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'Shop/view_product.html', {'products': products})


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            add_quantity = int(request.POST.get('add_quantity'))
            if add_quantity < 0:
                messages.error(request, "Quantity cannot be negative.")
            else:
                product.stock += add_quantity
                product.save()
                messages.success(request, f"Stock updated successfully! New stock: {product.stock}")
                return redirect('view_products')
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid number.")

    return render(request, 'Shop/update_product.html', {'product': product})



def admin_dashboard(request):
    total_products = Product.objects.count()
    context = {'total_products': total_products}
    return render(request, 'Shop/admin_dashboard.html', context)