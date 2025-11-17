from django.db import models
from django.conf import settings


class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							 on_delete=models.CASCADE)
	product_or_course_name = models.CharField(
		max_length=255, verbose_name="نام محصول یا دوره")
	rating = models.IntegerField(choices=[(1, '۱ ستاره'), (2, '۲ ستاره'), (
		3, '۳ ستاره'), (4, '۴ ستاره'), (5, '۵ ستاره')], verbose_name="رتبه‌بندی")
	review_text = models.TextField(verbose_name="متن نظر")
	created_at = models.DateTimeField(
		auto_now_add=True, verbose_name="تاریخ ایجاد")

	def __str__(self):
		return f"نظر توسط {self.user.username} در {self.product_or_course_name}"

