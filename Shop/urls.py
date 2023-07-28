from django.urls import path
from Shop import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import UserLogin, UserPasswordChange, ResetPassword,SetPassword
from django.conf.urls.static import static
urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart,name='remove_cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='Shop/passwordchange.html',form_class=UserPasswordChange, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='Shop/passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='Shop/password_reset.html',form_class=ResetPassword),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='Shop/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Shop/password_reset_confirm.html',form_class=SetPassword),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='Shop/password_reset_complete.html'),name='password_reset_complete'),

    path('man/', views.man, name='man'),
    path('man/<slug:data>', views.man, name='manshoes'),
    path('woman/', views.woman, name='woman'),
    path('woman/<slug:data>', views.woman, name='womanshoes'),
    path('kids/', views.kids, name='kid'),
    path('kids/<slug:data>', views.kids, name='kidshoes'),
    path('gift/',views.gift_card,name='gift'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='Shop/login.html',authentication_form=UserLogin), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('search/',views.search,name='search')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)