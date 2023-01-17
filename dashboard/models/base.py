from django.db import models


class BaseModelAbstract(models.Model):

    createdAt = models.DateTimeField(db_column='createdAt',
                                     auto_now_add=True)
    updatedAt = models.DateTimeField(db_column='updatedAt', auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ('-createdAt', )
