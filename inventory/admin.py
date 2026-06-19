from decimal import Decimal

from django.contrib import admin, messages
from django.db import transaction
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html

from .models import Product, Profile, StockAudit


class StockAuditInline(admin.TabularInline):
	model = StockAudit
	extra = 0
	can_delete = False
	fields = ('product', 'delta', 'reason', 'performed_by', 'created_at')
	readonly_fields = fields
	show_change_link = False

	def has_add_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_queryset(self, request):
		return super().get_queryset(request).select_related('performed_by', 'product')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	inlines = [StockAuditInline]
	list_display = ('name', 'sku', 'price', 'stock', 'category', 'low_stock_warning')
	list_filter = ('category',)
	search_fields = ('name', 'sku')
	list_editable = ('stock',)
	actions = ['mark_clearance']

	def low_stock_warning(self, obj):
		if obj.stock < 10:
			cls = 'low'
			text = 'Low Stock'
		elif obj.stock <= 50:
			cls = 'mid'
			text = 'Acceptable'
		else:
			cls = 'high'
			text = 'Good'
		return format_html('<span class="stock-badge {}">{}</span>', cls, text)

	low_stock_warning.short_description = 'Stock Status'

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='inventory-dashboard'),
		]
		return custom_urls + urls

	def dashboard_view(self, request):
		total_value_expression = ExpressionWrapper(
			F('price') * F('stock'),
			output_field=DecimalField(max_digits=18, decimal_places=2),
		)
		total_value = Product.objects.aggregate(total_value=Sum(total_value_expression)).get('total_value') or Decimal('0.00')
		low_stock_products = Product.objects.filter(stock__lt=10).order_by('stock', 'name')[:5]

		context = dict(
			self.admin_site.each_context(request),
			total_value=total_value,
			low_stock_products=low_stock_products,
		)
		return render(request, 'admin/inventory/dashboard.html', context)

	def has_change_permission(self, request, obj=None):
		if obj is None:
			return request.user.is_staff

		if request.user.is_superuser:
			return True

		profile = getattr(request.user, 'profile', None)
		return bool(profile and obj.category == profile.managed_category)

	@admin.action(description='Mark selected products for clearance (50%% off)')
	def mark_clearance(self, request, queryset):
		try:
			with transaction.atomic():
				for product in queryset.select_for_update():
					original_price = product.price
					product.price = (product.price * Decimal('0.50')).quantize(Decimal('0.01'))
					product.save(update_fields=['price'])
					StockAudit.objects.create(
						product=product,
						delta=0,
						reason=f'Price marked for clearance from {original_price}.',
						performed_by=request.user,
					)
		except Exception as exc:
			self.message_user(request, f'An error occurred: {exc}', messages.ERROR)
			return

		self.message_user(
			request,
			f'{queryset.count()} products were successfully marked for clearance.',
			messages.SUCCESS,
		)


@admin.register(StockAudit)
class StockAuditAdmin(admin.ModelAdmin):
	list_display = ('product', 'delta', 'reason', 'performed_by', 'created_at')
	list_select_related = ('product', 'performed_by')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'managed_category')
from django.contrib import admin

# Register your models here.
