from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .models import Document
from .serializer import DocumentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .tasks import count_words_from_file,mark_stuckjobs
from django.utils import timezone
# Create your views here.

@api_view(['POST'])
def upload_file(request):
    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        file_obj = serializer.validated_data['file']

        myfile = Document(file=file_obj)
        print(myfile.file.path, myfile.id)
        myfile.save()
        print(myfile.file.path, myfile.id)
        #background task of counting words in a file

        myfile.status = 'PROCESSING'
        myfile.processing_started_at = timezone.now()
        myfile.save(update_fields=['status','processing_started_at','updated_at'])
        count_words_from_file.delay(myfile.id)
        mark_stuckjobs.delay()

        return Response({"Message" : "File Uploaded and please wait until the process done..."},status=201)
    else:
        return Response({"Failed" : serializer.errors},status=400)
    


@api_view(['GET'])
def view_files(request):
    data = Document.objects.all().order_by("-created_at")
    serializer = DocumentSerializer(data,many=True)
    return Response(data=serializer.data,status=200)
    #return Response(serializer.errors,status=404)

@api_view(['GET'])
def view_file_by_id(request,id):
    data = get_object_or_404(Document,pk=id)
    serializer = DocumentSerializer(data,many=False)
    return Response(data=serializer.data,status=200)


@api_view(['PATCH'])
def update_file(request,id):
    file_instance = get_object_or_404(Document,pk=id)
    serializer = DocumentSerializer(data=request.data,instance=file_instance,partial=True)
    if serializer.is_valid():
        
        serializer.save()
        return Response({"Message" : "File Updated...."},status=201)
    else:
        return Response(serializer.errors,status=404)

@api_view(['DELETE'])
def delete_files(request,id):
    file_instance = get_object_or_404(Document,pk=id)
    file_instance.delete()
    return Response({"Message" : "File Deleted"},status=200)
    