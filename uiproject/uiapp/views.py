from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import EmailaddressForm
from .models import Emailaddress
from azure.storage.blob import BlobServiceClient
import uuid
from django import forms


# Create your views here.

class EmailaddressCreateView(CreateView):
    model = Emailaddress
    form_class = EmailaddressForm
    success_url = reverse_lazy('uiapp:emailaddress_create')
    def form_valid(self, form):
        # https://storagetexte.blob.core.windows.net/uploadzip?sp=racwdli&st=2022-12-12T22:56:11Z&se=2023-02-01T06:56:11Z&spr=https&sv=2021-06-08&sr=c&sig=5PU8S07Bywy85cfd24b3BLhemdICje7ucRKxVM%2Fq720%3D

        blob_service_client = BlobServiceClient.from_connection_string("***REMOVED***")
        container_name = "uploadzip"
        container_client = blob_service_client.get_container_client(container_name)
        if form.cleaned_data["uploadfile"].content_type != 'application/zip':
            raise forms.ValidationError('The uploaded file must be a zip file')
        blob_client = container_client.upload_blob(data=form.cleaned_data["uploadfile"], name=str(uuid.uuid4()))
        form.save()
        return super().form_valid(form)

"""
from django.views.generic import View
from django.http import HttpResponse

from azure.storage.blob import BlobServiceClient


class FileUploadView(View):
    def post(self, request):
        # Get the uploaded file from the request
        uploaded_file = request.FILES['file']

        # Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string("<your_connection_string>")

        # Get the container where the file will be uploaded
        container_name = "<your_container_name>"
        container_client = blob_service_client.get_container_client(container_name)

        # Upload the file
        blob_client = container_client.upload_blob(uploaded_file, blob_name=uploaded_file.name)

        # Return a successful response
        return HttpResponse("File uploaded successfully.")

"""