import uuid

from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
from django.views.generic import TemplateView, CreateView

from invoices.models import UploadedFile
from invoices.tasks import process_csv_file


class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context["token"] = str(uuid.uuid4())
        return context


class UploadedFileCreateView(TemplateView):


    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        if files:
            files_name = []
            files_id = []
            for file in files:
                #Create register
                new_csv = UploadedFile.objects.create(
                    file=file,
                    separator=request.POST.get('separator'),
                    token=request.POST.get('token')
                )
                files_name.append(new_csv.file.name.replace('uploaded_files/', ''))
                files_id.append(new_csv.pk)

                process_csv_file.delay(new_csv.id, new_csv.token, new_csv.file.path, new_csv.separator)

            return JsonResponse(
                data={
                    "token": request.POST.get('token'),
                    "file_name": files_name,
                    "id": files_id
                },
                status=200
            )

        else:
            return JsonResponse(
                data={
                    "token": request.POST.get('separator')
                },
                status=400
            )
