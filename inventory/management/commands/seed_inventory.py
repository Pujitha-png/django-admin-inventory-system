from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from inventory.models import Product, Profile, StockAudit


class Command(BaseCommand):
    help = 'Seed the inventory admin database with users, profiles, products, and audit history.'

    def handle(self, *args, **options):
        User = get_user_model()
        credentials = {
            'superuser': {
                'username': 'superuser',
                'email': 'superuser@test.com',
                'password': 'superuser123!',
                'is_superuser': True,
                'is_staff': True,
            },
            'electronics_staff': {
                'username': 'electronics_staff',
                'email': 'electronics@test.com',
                'password': 'electronics123!',
                'is_superuser': False,
                'is_staff': True,
                'managed_category': 'Electronics',
            },
            'books_staff': {
                'username': 'books_staff',
                'email': 'books@test.com',
                'password': 'books123!',
                'is_superuser': False,
                'is_staff': True,
                'managed_category': 'Books',
            },
        }

        for user_key, data in credentials.items():
            user, created = User.objects.get_or_create(username=data['username'], defaults={'email': data['email']})
            user.email = data['email']
            user.is_staff = data['is_staff']
            user.is_superuser = data['is_superuser']
            user.set_password(data['password'])
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User ready: {user.username} (created={created})'))

            if not user.is_superuser:
                Profile.objects.update_or_create(
                    user=user,
                    defaults={'managed_category': data['managed_category']},
                )
                # Ensure staff users have model-level permissions so the app appears in the admin index
                try:
                    perms = Permission.objects.filter(codename__in=['view_product', 'change_product'])
                    if perms.exists():
                        user.user_permissions.add(*perms)
                except Exception:
                    # If permissions aren't available yet (migrations not run), skip silently
                    pass

        categories = [
            ('Electronics', 'ELEC'),
            ('Books', 'BOOK'),
            ('Apparel', 'APP'),
            ('Home', 'HOME'),
        ]

        for category_index, (category, code) in enumerate(categories, start=1):
            for number in range(1, 26):
                stock = (number * category_index) % 65
                if number <= 4:
                    stock = number + category_index
                price = Decimal('19.99') + (Decimal(str(category_index)) * Decimal('25.00')) + Decimal(str(number))
                product, created = Product.objects.update_or_create(
                    sku=f'{code}-{number:03d}',
                    defaults={
                        'name': f'{category} Product {number:03d}',
                        'price': price.quantize(Decimal('0.01')),
                        'stock': stock,
                        'category': category,
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created product {product.sku}'))

                if number <= 3 and not product.audit_logs.exists():
                    StockAudit.objects.create(
                        product=product,
                        delta=stock,
                        reason=f'Initial stock seed for {product.name}.',
                        performed_by=None,
                    )

        self.stdout.write(self.style.SUCCESS('Inventory seed completed.'))
