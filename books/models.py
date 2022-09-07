from django.db import models


class Author(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    last_updated = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Authors"  # A human-readable name for the object, plural
        verbose_name = "Author"  # A human-readable name for the object, singular


class Book(models.Model):
    name = models.TextField(null=False, blank=False)
    isbn = models.TextField(null=False, blank=False) # isbn is 13 + 4 hyphens/space making 17 ==> (978-3-16-148410-0)
    author = models.ForeignKey(Author, related_name="author_books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    last_updated = models.DateTimeField(null=True, auto_now=True)

    @property
    def author_name(self):
        return self.author.full_name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-last_updated']
        verbose_name_plural = "Books"  # A human-readable name for the object, plural
        verbose_name = "Book"  # A human-readable name for the object, singular

