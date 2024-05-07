from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from hitcount.models import HitCountMixin
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from users.models import CustomUser
from config.settings import ALLOWED_IMAGE_EXTENSIONS


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Post(models.Model,HitCountMixin):
    TOPIC = (
        ('Announcement','announcement'),
        ('Event','event'),
        ('Post','post'),
        ('Birthday','birthday'),

    )

    title = models.CharField(max_length=250)
    content = models.TextField()
    picture_content = models.ImageField(upload_to='posts/%Y/%m/%d/',default='aaaaa.jpg',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)])
    section_topic = models.CharField(max_length=100,choices=TOPIC,default='p')
    post_tag = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(default= timezone.now)
    creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250,unique=True)
    likes = models.ManyToManyField(CustomUser,related_name='likes',blank=True)
    is_published = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')


    objects = models.Manager()
    published = PublishedManager()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title} by {self.creator}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = ("post")
        verbose_name_plural = ("posts")


class Comment(models.Model):
    post_name = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created_at']


