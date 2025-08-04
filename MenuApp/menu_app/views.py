from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Item, MEAL_TYPE, Cart, CartItem  # imports from the models table


class MenuList(LoginRequiredMixin, generic.ListView):
    queryset = Item.objects.order_by("-date_created")
    template_name = "index.html"#connects views to index html file
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)#key and value tells html code what the keys value is
        context["meals"] = MEAL_TYPE
        # Get user's cart
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context["cart"] = cart
        return context


class MenuItemDetail(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = "menu_item_detail.html"#connects views to menu item html file
    login_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('menu')


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{item.meal} added to cart!')
    return redirect('home')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item_name = cart_item.item.meal
    cart_item.delete()
    messages.success(request, f'{item_name} removed from cart!')
    return redirect('cart')


@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        messages.success(request, 'Cart updated!')
    return redirect('cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def clear_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.cartitem_set.all().delete()
    messages.success(request, 'Cart cleared!')
    return redirect('cart')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to our menu app.')
            return redirect('menu')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})





