from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
	name = models.CharField(max_length=200)
	sku = models.CharField(max_length=50, unique=True, verbose_name='SKU')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.IntegerField(default=0)
	category = models.CharField(max_length=100, db_index=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class StockAudit(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='audit_logs')
	delta = models.IntegerField()
	reason = models.CharField(max_length=200)
	performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.product} audit at {self.created_at:%Y-%m-%d %H:%M:%S}'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	managed_category = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f'{self.user.username} -> {self.managed_category or "unassigned"}'
