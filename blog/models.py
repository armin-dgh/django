from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django.views.decorators.http import require_POST
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify

# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    CATEGORY_CHOICES= (
        ("تکنولوژی","تکنولوژی"),
        ("هوش مصنوعی", "هوش مصنوعی"),
        ("برنامه نویسی", "برنامه نویسی"),
        ("بلاکچین", "بلاکچین"),
        ("سایر", "سایر"),

    )
    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name="نویسنده")
    # data fields
    title = models.CharField(max_length=250, verbose_name="عنوان")
    slug = models.SlugField(max_length=25, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    # date
    publish = models.DateTimeField(default=timezone.now, verbose_name="انتشار")
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")
    # choices field
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PUBLISHED,verbose_name="وضعیت")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="سایر")
    objects = models.Manager()
    published = PublishManager()
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("blog:post-detail", args=[self.id])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)

class Ticket(models.Model):
    massage = models.TextField(verbose_name="توضیحات")
    name = models.CharField(max_length=250, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    subject = models.CharField(max_length=250)

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=250, verbose_name="نام")
    massage = models.TextField(verbose_name="توضیحات")
    create = jmodels.jDateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name}: {self.post}"


class Image(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image_file = ResizedImageField(upload_to="armin", size=[500, 500], quality=70, crop=['middle', 'center'])
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    create = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        import os
        self.title = os.path.basename(f"{self.image_file}")
        return os.path.basename(f"{self.image_file}")



class Account(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(verbose_name="بایو", null=True, blank=True)
    photo = ResizedImageField(upload_to="account_images/", size=[500, 500], quality=60, crop=['middle', 'center'], blank=True, null=True)
    job = models.CharField(verbose_name="شغل", null=True, blank=True)


    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها"

    def delete(self, *args, **kwargs):
        storage, path = self.photo.storage, self.photo.path
        storage.delete(path)
        super().delete(*args, **kwargs)

