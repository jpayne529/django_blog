from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.

class Tag(models.Model):
    name = models.CharField("Tag", max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField("Title", max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    text_body = models.TextField("Post Body")
    image = models.FileField("Thumbnail", null=True, blank=True)
    draft = models.BooleanField("Draft", default=False)
    author = models.CharField("Author", max_length=50, default='Admin')
    orig_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-orig_time']

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    query = Post.objects.filter(slug=slug).order_by("-id")
    exists = query.exists()
    if exists:
        new_slug = "%s-%s" %(slug, query.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug 

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    
pre_save.connect(pre_save_post_receiver, sender=Post)

