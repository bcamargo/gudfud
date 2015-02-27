from cStringIO import StringIO
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from foodie.storage import OverwriteStorage


class BaseUser(AbstractBaseUser):
    email = models.CharField('email', max_length=254, unique=True)
    first_name = models.CharField('first name', max_length=32, blank=True, null=True)
    last_name = models.CharField('last name', max_length=32, blank=True, null=True)
    image = models.ImageField('image', upload_to='user_profile/images', blank=True, null=True,
                              storage=OverwriteStorage())
    thumbnail_image = models.ImageField('thumbnail', upload_to='user_profile/thumbnails', blank=True, null=True,
                                        storage=OverwriteStorage())
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

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


class Customer(BaseUser):
    pass


class Operator(BaseUser):
    pass