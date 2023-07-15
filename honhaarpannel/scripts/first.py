from django.forms.models import model_to_dict
import re
from honhaarpannel.models import Student, Batch
model =Batch
def camel_to_snake(string):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
def get_serializer_fields(indent):
    fields = ''
    for field in model._meta.get_fields():
        _type = field.get_internal_type()
        if _type in ['DateField', 'DateTimeField']:
            fields += f'{field.name} = serializers.{_type}()\n{" " * indent}'
        elif field.name == 'id':
            fields += f'{camel_to_snake(model.__name__)}_id = serializers.IntegerField(source="id")\n{" " * indent}'
    return fields
def set_create_kwrgs(model_dict):
    def model_type_to_py_type(field):
        type_dict = {'CharField': 'str', 'TextField': 'str', 'DateField': 'datetime.date',
                     'ForeignKey': model._meta.get_field(
                         field.field.name).remote_field.model.__name__ if field.field.get_internal_type() == 'ForeignKey' else None,
                     'BooleanField': 'bool', 'IntegerField': 'int'}
        return type_dict.get(field.field.get_internal_type(), 'str')
    kwrgs = ''
    for field in model_dict.values():
        if field.field.name in ['id']:
            continue
        _type = field.field.get_internal_type()
        kwrgs += f'{field.field.name}:{model_type_to_py_type(field)}, '
    return kwrgs[:-2]
def assign_kwrgs(fields, pefix='', seperated_by="", indent=0):
    args = f'\n{" " * indent}'
    for field in [i.split(':')[0] for i in fields.split(',')]:
        args += f'{pefix}{field.strip()}={field.strip()}{seperated_by} \n{" " * indent}'
    return args
def run():
    model_dict = model_to_dict(model)
    model_name = camel_to_snake(model.__name__)
    api_str = f'''
class {model.__name__}Api(ExceptionHandlerMixin, APIView):
    paginator = PageNumberPagination()
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = {model.__name__}
            fields = {[i for i in model_dict if i not in ['id']]}
    class OutputSerializer(serializers.ModelSerializer):
        {get_serializer_fields(8)}
        class Meta:
            model = {model.__name__}
            fields = {[f'{model_name}_id' if i.name == 'id' else i.name for i in model._meta.get_fields()]}
    def get(self, request, *args, **kwargs):
        check_permission(
            has_{model_name}_perm, user=request.user, permission=QLSPermissions.PERM_VIEW, {model_name}=None
        )
        if '{model_name}_id' in self.kwargs:
            {model_name} = get_object_or_404({model.__name__}, id=self.kwargs['{model_name}_id'])
            serializer = self.OutputSerializer({model_name})
            return Response(serializer.data, status=status.HTTP_200_OK)
        params = request.GET.dict()
        {model_name}s = get_{model_name}s()
        custom_map = {{}}
        {model_name}s = apply_get_filters(model={model.__name__}, queryset={model_name}s,
                                         params=params,
                                         custom_map=custom_map)
        no_pagination = request.GET.get('no_pagination', False) == 'true'
        if no_pagination:
            return Response(self.OutputSerializer({model_name}s, many=True, context={{'request': request}}).data,
                            status=status.HTTP_200_OK)
        self.paginator.page_size = request.GET.get('count', 10)
        result_page = self.paginator.paginate_queryset({model_name}s, request)
        serializer = self.OutputSerializer(result_page, many=True, context={{'request': request}})
        return self.paginator.get_paginated_response(serializer.data)
    def post(self, request, *args, **kwargs):
        check_permission(
            has_{model_name}_perm, user=request.user, permission=QLSPermissions.PERM_ADD, {model_name}=None
        )
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        {model_name} = create_{model_name}(**serializer.validated_data)
        return Response(self.OutputSerializer({model_name}).data, status=status.HTTP_201_CREATED)
    def put(self, request, {model_name}_id, *args, **kwargs):
        {model_name} = get_object_or_404({model.__name__}, id={model_name}_id)
        check_permission(
            has_{model_name}_perm, user=request.user, permission=QLSPermissions.PERM_EDIT, {model_name}={model_name}
        )
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        {model_name} = update_{model_name}({model_name}={model_name}, **serializer.validated_data)
        return Response(self.OutputSerializer({model_name}).data, status=status.HTTP_202_ACCEPTED)
    def delete(self, request, {model_name}_id, *args, **kwargs):
        {model_name} = get_object_or_404({model.__name__}, id={model_name}_id)
        check_permission(
            has_{model_name}_perm, user=request.user, permission=QLSPermissions.PERM_DELETE, {model_name}={model_name}
        )
        delete_{model_name}({model_name}={model_name})
        return Response(status=status.HTTP_204_NO_CONTENT)
def has_{model_name}_perm(user: User, permission: QLSPermissions, {model_name}: {model.__name__} = None) -> bool:
    if user.is_anonymous:
        return False
    if user.type in ['ctrm']:
        return True
    return False
def create_{model_name}({set_create_kwrgs(model_dict)}) -> {model.__name__}:
    logger.info(f'Creating {model_name} {{}}')
    {model_name} = {model.__name__}.objects.create({assign_kwrgs(set_create_kwrgs(model_dict), seperated_by=',', indent=4)})
    return {model_name}
def update_{model_name}({model_name}: {model.__name__}, {set_create_kwrgs(model_dict)}) -> {model.__name__}:
    logger.info(f'Updating {model_name} {{{model_name}}}')
    {assign_kwrgs(set_create_kwrgs(model_dict), pefix=f'{model_name}.', seperated_by='', indent=4)}
    {model_name}.save()
    return {model_name}
def delete_{model_name}({model_name}: {model.__name__}) -> None:
    logger.info(f'Deleting {model_name} {{{model_name}}}')
    {model_name}.delete()
    return
def get_{model_name}s() -> QuerySetType[{model.__name__}]:
    return {model.__name__}.objects.all()
    '''
    print(api_str)
    print(api_str, file=open('auto_generated_code.py', 'w'))