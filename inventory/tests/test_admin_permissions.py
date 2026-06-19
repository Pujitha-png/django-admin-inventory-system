from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from inventory.admin import ProductAdmin
from inventory.models import Product, Profile


class ProductAdminPermissionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.product_admin = ProductAdmin(Product, self.site)

        self.superuser = User.objects.create_superuser('superuser', 'super@test.com', 'superuser123!')
        self.staff_user = User.objects.create_user('electronics_staff', 'electronics@test.com', 'electronics123!', is_staff=True)
        Profile.objects.create(user=self.staff_user, managed_category='Electronics')

        self.product_electronics = Product.objects.create(
            name='Laptop',
            sku='ELEC-LAP-001',
            price='1200.00',
            stock=25,
            category='Electronics',
        )
        self.product_books = Product.objects.create(
            name='Django Book',
            sku='BOOK-DJ-001',
            price='50.00',
            stock=30,
            category='Books',
        )

    def test_staff_user_can_change_product_in_category(self):
        request = self.factory.get('/')
        request.user = self.staff_user

        has_perm = self.product_admin.has_change_permission(request, self.product_electronics)
        self.assertTrue(has_perm)

    def test_staff_user_cannot_change_product_out_of_category(self):
        request = self.factory.get('/')
        request.user = self.staff_user

        has_perm = self.product_admin.has_change_permission(request, self.product_books)
        self.assertFalse(has_perm)
