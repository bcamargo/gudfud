from cStringIO import StringIO
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager as AuthBaseUserManager
from foodie.storage import OverwriteStorage
import models_mixins


class BaseUserManager(AuthBaseUserManager):
    def create_user(self, email, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True)
        user.save()
        return user


class BaseUser(AbstractBaseUser):
    email = models.CharField('email', max_length=64, unique=True)
    first_name = models.CharField('first name', max_length=32, blank=True, null=True)
    last_name = models.CharField('last name', max_length=32, blank=True, null=True)
    image = models.ImageField('image', upload_to='base_user/images', blank=True, null=True,
                              storage=OverwriteStorage())
    thumbnail = models.ImageField('thumbnail', upload_to='base_user/thumbnails', blank=True, null=True,
                                  storage=OverwriteStorage())
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    @property
    def username(self):
        return self.email

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        try:
            if self.image.file is not None:
                img = Image.open(self.image.file)

                thumbnail = img.resize((settings.GUDFUD_USER_THUMBNAIL_WIDTH, settings.GUDFUD_USER_THUMBNAIL_HEIGHT),
                                       Image.ANTIALIAS)

                temp_handle_img = StringIO()
                img.save(temp_handle_img, 'jpeg')
                temp_handle_img.seek(0)

                temp_handle_thumbnail = StringIO()
                thumbnail.save(temp_handle_thumbnail, 'jpeg')
                temp_handle_thumbnail.seek(0)

                fname_thumbnail = str(self.id) + ".jpeg"
                suf_thumbnail = SimpleUploadedFile(fname_thumbnail, temp_handle_thumbnail.read(),
                                                   content_type='image/jpeg')
                fname_img = str(self.id) + ".jpeg"
                suf_img = SimpleUploadedFile(fname_img, temp_handle_img.read(), content_type='image/jpeg')

                self.thumbnail_image.save(fname_thumbnail, suf_thumbnail, save=False)
                self.image.save(fname_img, suf_img, save=False)
        except ValueError:
            pass

        super(BaseUser, self).save(force_insert, force_update, using, update_fields)


class Customer(models_mixins.BaseUserMixin, models.Model):
    base_user = models.OneToOneField('BaseUser', related_name='customer')
    address = models.CharField(max_length=256, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=32, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)


class Dispatcher(models_mixins.BaseUserMixin, models.Model):
    base_user = models.OneToOneField('BaseUser', related_name='dispatcher')


class Operator(models_mixins.BaseUserMixin, models.Model):
    base_user = models.OneToOneField('BaseUser', related_name='operator')


class MenuItem(models.Model):
    menu_item_category = models.ForeignKey('MenuItemCategory', related_name='menu_items')
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField('image', upload_to='menu_items/images', blank=True, null=True,
                              storage=OverwriteStorage())
    thumbnail = models.ImageField('thumbnail', upload_to='menu_items/thumbnails', blank=True, null=True,
                                  storage=OverwriteStorage())
    is_active = models.BooleanField(default=True)


class Menu(models.Model):
    datetime = models.DateTimeField()
    menu_items = models.ManyToManyField('MenuItem')


class MenuItemCategory(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField('image', upload_to='menu_items/images', blank=True, null=True,
                              storage=OverwriteStorage())
    thumbnail = models.ImageField('thumbnail', upload_to='menu_items/thumbnails', blank=True, null=True,
                                  storage=OverwriteStorage())
    is_active = models.BooleanField(default=True)


class ServiceRating(models.Model):
    customer = models.ForeignKey('Customer', related_name='service_rating')
    order = models.ForeignKey('Order', related_name='service_rating')
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    taste = models.BooleanField(default=True)
    delivery = models.BooleanField(default=True)
    packaging = models.BooleanField(default=True)
    support = models.BooleanField(default=True)
    comments = models.TextField(null=True, blank=True)


class Order(models.Model):
    STATUS_RECEIVED = 'RECEIVED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_DELIVERED = 'DELIVERED'
    STATUS_CHOICES = ((STATUS_RECEIVED, STATUS_RECEIVED), (STATUS_CANCELLED, STATUS_CANCELLED),
                      (STATUS_DELIVERED, STATUS_DELIVERED))

    customer = models.ForeignKey('Customer', related_name='order')
    dispatcher = models.ForeignKey('Dispatcher', related_name='order')
    menu_items = models.ManyToManyField('MenuItem', related_name='order')
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=32)
    delivery_time_from = models.DateTimeField()
    delivery_time_to = models.DateTimeField()



