import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command helps to create views ,forms, templates.\n" \
           "Enter app name with preceding '/'  followed by model name\n" \
           "eg: python manage.p sample /apps/app_name  model_name"


    # flags
    flags = os.O_RDWR | os.O_CREAT

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs='+')
        parser.add_argument('model_name', nargs='+')

    def create_urls(self, path, model):
        file = path + '/urls.py'
        createview = f'{model}CreateView'
        detailview = f'{model}DetailView'
        listview = f'{model}ListView'
        deleteview = f'{model}DeleteView'
        try:
            with open(file, 'a') as fp:
                fp.write("# New file created \n"
                         "from django.urls import path, include\n"
                         "urlpatterns = ["
                                        f"path('{model}/', include([\n"
                                        f"path('', {listview}.as_view(), name='{model.lower()}-list'),\n"
                                        f"path('create/', {createview}.as_view(), name='{model.lower()}-create'),\n"
                                        f"path('<int:pk>/update/', {detailview}.as_view(), name='{model.lower()}-update'),\n"
                                        f"path('<int:pk>/delete/', {deleteview}.as_view(), name='{model.lower()}-delete'),\n"
                                    "]))]\n"
                         )
            print(f"File {file.split('/')[-1]} created")
        except Exception as e:
            print(e)
            print("File '%s' already exist" % file)

    def create_view_files(self, file, model):
        print("Inside cretae view file")
        createview = f'{model}CreateView(CreateView)'
        detailview = f'{model}DetailView(DetailView)'
        listview = f'{model}ListView(ListView)'
        deleteview = f'{model}DeleteView(DeleteView)'
        try:
            # os.open(file, self.flags)
            with open(file, 'a') as fp:
                fp.write("# New file created \n"
                         "from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView\n\n"
                         f"class {createview}:\n"
                         f"\tqueryset = {model}.objects.all()\n"
                         f"\ttemplate_name = 'templates/{model.lower()}_create.html'\n"
                         f"\tmodel = {model}\n\n\n"
                         f"class {detailview}:\n"
                         f"\tqueryset = {model}.objects.all()\n"
                         f"\ttemplate_name = 'templates/{model.lower()}_detail.html'\n"
                         f"\tmodel = {model}\n\n\n"
                         f"class {listview}:\n"
                         f"\tqueryset = {model}.objects.all()\n"
                         f"\ttemplate_name = 'templates/{model.lower()}_list.html'\n"
                         f"\tmodel = {model}\n\n\n"                         
                         f"class {deleteview}:\n"
                         f"\tqueryset = {model}.objects.all()\n"
                         f"\ttemplate_name = 'templates/{model.lower()}_delete.html'\n"
                         f"\tmodel = {model}\n\n\n"                         ""
                         ""
                         "")
            print(f"File {file.split('/')[-1]} created")
        except Exception as e:
            print(e)
            print("File '%s' already exist" % file)

    def create_form_files(self, file, model):
        print("Inside cretae form file")

        try:
            with open(file, 'a') as fp:
                fp.write(
                    "# New file created \n"
                     "from django import forms\n"
                     f"class {model}Form(forms.ModelForm):\n\tclass Meta:\n\t\tmodel = {model}\n\t\tfields = ()"
                     )
            print(f"{file.split('/')[-1]} created")
        except Exception as e:
            print(e)
            print("File '%s' already exist" % file)

    def create_template_files(self, path, model):
        print("Inside create template  file")
        list_file = path + f'{model}_list.html'
        create_file = path + f'{model}_create.html'
        detail_file = path + f'{model}_detail.html'
        form_file = path + f'{model}_form.html'
        list_content = "{% extends 'paper/layout.html' %}\n"\
                    "{% block content%}\n" \
                     "<div class=''>\n"\
                        "<div class='row'>\n"\
                            "<div class='col-12'>\n"\
                                "<div class='card'>\n"\
                                    "<div class='card-body'>\n"\
                                        "<div class='table-responsive'>\n"\
                                        "</div>\n"\
                                    "</div>\n"\
                                "</div>\n"\
                                "<div class='card'>\n"\
                                    "<div class='card-body'>\n"\
                                        "<h3 class='text-muted'>You do not have any <b></b>. </h3>\n"\
                                        "<p class='text-muted'>Please create one\n"\
                                            "<a href='' class='badge badge-success'>here</a>\n"\
                                        "</p>\n"\
                                    "</div>\n"\
                                "</div>\n"\
                            "</div>\n"\
                        "</div>\n"\
                    "</div>\n"\
                    "{% endblock %}"

        form_content ="{% extends 'paper/layout.html' %}\n"\
                    "{% block content%}\n"\
                    "<div class='row'>\n"\
                        "<div class='col-md-6 '>\n"\
                            "<div class='card'>\n"\
                                "<div class='card-body'>\n"\
                                    "<fieldset class='form-group '>\n"\
                                        "<form action='' method='post' >\n"\
                                            "{% csrf_token %}\n"\
                                            "{{ form | crispy  }}\n"\
                                            "<button type='submit' class='btn btn-sm btn-success'> Save </button>\n"\
                                        "</form>\n"\
                                    "</fieldset>\n"\
                                "</div>\n"\
                            "</div>\n"\
                        "</div>\n"\
                    "</div>\n"\
                    "{% endblock %}"
        for filetype in [list_file, detail_file]:
            with open(filetype, 'a') as fp:
                    fp.write(list_content)

        for filetype in [create_file, form_file]:
            with open(filetype, 'a') as fp:
                    fp.write(form_content)

    def create_template(self, path, model):
        model = model.lower()
        print("Inside create template")
        path = path + f'/templates/'
        # file = path + f'/templates/{model}_form.html'
        try:
            os.makedirs(path)
            self.create_template_files(path, model)
        except Exception as e:
            print("Directory '%s' already exist" % path)
            self.create_template_files(path, model)
        return None

    def create_views(self, path, model):
        print("Inside create Views")

        path = path + '/views/'
        file = path + f'{model.lower()}_view.py'
        try:
            os.makedirs(path)
            # create files in this dir
            self.create_view_files(file, model)
        except Exception as e:
            print("Directory '%s' already exist" %path)
            self.create_view_files(file, model)

        return None

    def create_forms(self, path, model):
        print("Inside create Forms")
        path = path + '/forms/'
        file = path + f'{model.lower()}_form.py'
        try:
            os.makedirs(path)
            self.create_form_files(file, model)
        except Exception as e:
            print("Directory '%s' already exist" %path)
            self.create_form_files(file, model)

        return None

    def handle(self, *args, **options):
        app_name = options.get('app_name')
        model_name = options.get('model_name')
        model = model_name[0]
        path = os.path.join(os.getcwd()+app_name[0])
        print(path)

        # Now change the directory
        os.chdir(path)

        # Check current working directory.
        # App path where the templates views and forms should be created
        app_path = os.getcwd()
        print("Directory changed successfully %s" % app_path)


        #template views
        self.create_views(app_path, model)

        #template forms
        self.create_forms(app_path, model)

        # template creation
        self.create_template(path, model)

        self.create_urls(path, model)



