from celery import shared_task
import os
from collections import Counter
import string
from django.utils import timezone
from datetime import timedelta
from .models import Document


@shared_task()
def count_words_from_file(id):
    
    document = Document.objects.get(id=id)
    
    try:
        count = 0
        counter = Counter()
        file=document.file.path
        if not os.path.exists(file):
            return "File not Exist"
        
        with open(file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.lower()
                line = line.translate(str.maketrans('','',string.punctuation))
                words = line.split()
                count+=len(words)
                counter.update(words)
            document.word_count = count
            document.word_frequency_count = dict(counter)
            document.status='COMPLETED'
            document.save()
    except Exception as exc:
        document.status = 'FAILED'
        document.error_message = str(exc)
        document.save(update_fields=['status','error_message','updated_at'])

        raise

    return {
        "Status" : "SUCCESS",
        "Words_count" : count,
        "words" : dict(counter)
    }



@shared_task()
def mark_stuckjobs():
    threshold = timezone.now() - timedelta(minutes=15)
    docs = Document.objects.filter(status='PROCESSING',processing_started_at__lt = threshold)

    for doc in docs:
        doc.status = 'FAILED'
        doc.save(update_fields='status')
        print(doc.status)

    return {"Status":"Pending Jobs cleared", "doc_status" : docs.status}

    

