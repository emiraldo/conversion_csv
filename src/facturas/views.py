import uuid

from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
from django.views.generic import TemplateView, CreateView

from facturas.models import UploadedFile
from facturas.tasks import process_csv_file


class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context["token"] = str(uuid.uuid4())
        return context


class UploadedFileCreateView(CreateView):

    model = UploadedFile
    fields = 'file', 'separator', 'token'

    def get_form(self, form_class=None):
        form = super(UploadedFileCreateView, self).get_form()

        for key in form.fields:
            form.fields[key].widget.attrs["class"] = "form-control"
        return form

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


    def form_valid(self, form):
        self.object = form.save()
        print("se crea el registro")
        process_csv_file.delay(self.object.token, self.object.file.path)
        print("envio la tarea asincrona")
        return JsonResponse(
            data={"token": self.object.token},
            status=200
        )
