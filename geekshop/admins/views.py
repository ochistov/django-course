from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryUpdateFormAdmin, ProductsForm
from authapp.models import User
from mainapp.admin import Product
from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin
from mainapp.models import ProductCategory, Products
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

# index

class IndexTemplateView(TemplateView):
    template_name = 'admins/admin.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(IndexTemplateView, self).dispatch(request, *args, **kwargs)

# for users CRUD

class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Изменение пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Удаления пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


# for categories CRUD
class CategoryCreateView(CreateView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    success_url = reverse_lazy('admins:admin_category')
    form_class = CategoryUpdateFormAdmin
    title = 'Админка | Создание категории'

class CategoryListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    title = 'Админка | Список категорий'
    context_object_name = 'categories'


    def get_queryset(self):
        if self.kwargs:
           return ProductCategory.objects.filter(id=self.kwargs.get('pk'))
        else:
           return ProductCategory.objects.all()

class CategoryUpdateView(UpdateView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = CategoryUpdateFormAdmin
    title = 'Админка | Обновления категории'
    success_url = reverse_lazy('admins:admin_category')

class CategoryDeleteView(DeleteView,BaseClassContextMixin,CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.product_set.update(is_active=False)
        self.object.is_active = False if self.object.is_active else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# for products CRUD
class ProductsCreateView(CreateView, BaseClassContextMixin,CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductsForm
    title = 'Админка | Создание товара'
    success_url = reverse_lazy('admins:admins_product')

class ProductListView(ListView,BaseClassContextMixin,CustomDispatchMixin):
    model = Products
    template_name = 'admins/admin-product-read.html'
    title = 'Админка | Список товаров'

class ProductsUpdateView(UpdateView, BaseClassContextMixin,CustomDispatchMixin):
    model = Products
    template_name = 'admins/admin-product-update-delete.html'
    form_class = ProductsForm
    title = 'Админка | Обновление товара'
    success_url = reverse_lazy('admins:admins_product')

class ProductsDeleteView(DeleteView, CustomDispatchMixin):
    model = Products
    template_name = 'admins/admin-product-read.html'
    success_url = reverse_lazy('admins:admins_product')
    #
    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.is_active = False if self.object.is_active else True
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())