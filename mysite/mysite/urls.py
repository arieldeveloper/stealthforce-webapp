"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from main_app import views as main_app_views
from django.contrib.auth import views as auth_views
from feed import views as feed_views
app_name = 'accounts'
urlpatterns = [
    path('accounts/logout/', user_views.logout_view, name='logout'),
    path('', feed_views.FeedListView.as_view(), name='home'), #main homepage
    path('admin/', admin.site.urls),
    path('p/new/', feed_views.ItemCreateView.as_view(template_name='feed/create-item.html'), name="create-item"),
    path('p/<int:pk>/', feed_views.FeedItemDetailView.as_view(template_name="feed/feed-item.html"), name='feed-detail-view'),
    path('accounts/edit/', user_views.account_edit_view, name='edit'),
    path('accounts/profile/', user_views.user_profile_view, name="profile"),
    path('accounts/register/', user_views.register_view, name='register'),
    path('accounts/login/', user_views.login_view, name='login'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password-reset.html', html_email_template_name='users/password-reset-email.html'),
                                                                        name="password_reset"),
    path('accounts/password-reset-sent', auth_views.PasswordResetDoneView.as_view(template_name='users/password-reset-sent.html'),
         name="password_reset_done"),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password-reset-confirm.html'),
         name="password_reset_confirm"),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password-reset-done.html'),
         name="password_reset_complete")]
