from datetime import date
from framework.templator import render
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.сreational_patterns import Logger, Engine, MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import ListView, CreateView


site = Engine()
logger = Logger('main')

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes = {}


# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# контроллер 404
class PageNotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/field-list/')
class FieldListView(ListView):
    template_name = 'field-list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('field')
        return mapper.all()


@AppRoute(routes=routes, url='/create-field/')
class FieldCreateView(CreateView):
    template_name = 'create_field.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_table('field', name)
        site.fields.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()

@AppRoute(routes=routes, url='/add-field/')
class AddFieldByServiceCreateView(CreateView):
    template_name = 'add_field.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['tables'] = site.tables
        context['fields'] = site.fields
        return context

    def create_obj(self, data: dict):
        table_name = data['table_name']
        table_name = site.decode_value(table_name)
        table = site.get_table(table_name)
        field_name = data['field_name']
        field_name = site.decode_value(field_name)
        field = site.get_field(field_name)
        table.add_client(field)



