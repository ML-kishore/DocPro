from django.db import models

# Create your models here.
class Document(models.Model):
    #id = models.IntegerField()
    file = models.FileField(upload_to='documents')
    STATUS_CHOICES = (('QUEUED','Queued'),('PROCESSING','Processing'),('DONE','Done'),('FAILED','Failed'),)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,default='QUEUED',choices=STATUS_CHOICES)
    word_count = models.PositiveIntegerField(default=0)
    word_frequency_count = models.JSONField(default=dict,blank=True)
    error_message = models.TextField(default="",blank=True)
    processing_started_at = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return f"Job Id #{self.id}"

