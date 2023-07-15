from django.shortcuts import render
from rest_framework import serializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from services.commands import create_school, update_school, delete_school
from services.queries import get_schools

from models import Student, School, Batch

# Create your views here.

class SchoolApi(serializers.ModelSerializer, APIView):
    paginator = PageNumberPagination()
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = School
            fields = ['school_name']
    class OutputSerializer(serializers.ModelSerializer):
        school_id = serializers.IntegerField(source="id")
        
        class Meta:
            model = School
            fields = ['batch', 'school_id', 'school_name']
    def get(self, request, *args, **kwargs):
        
        if 'school_id' in self.kwargs:
            school = get_object_or_404(School, id=self.kwargs['school_id'])
            serializer = self.OutputSerializer(school)
            return Response(serializer.data, status=status.HTTP_200_OK)
        params = request.GET.dict()
        schools = get_schools()
        custom_map = {}
        schools = apply_get_filters(model=School, queryset=schools,
                                         params=params,
                                         custom_map=custom_map)
        no_pagination = request.GET.get('no_pagination', False) == 'true'
        if no_pagination:
            return Response(self.OutputSerializer(schools, many=True, context={'request': request}).data,      
                            status=status.HTTP_200_OK)
        self.paginator.page_size = request.GET.get('count', 10)
        result_page = self.paginator.paginate_queryset(schools, request)
        serializer = self.OutputSerializer(result_page, many=True, context={'request': request})
        return self.paginator.get_paginated_response(serializer.data)
    def post(self, request, *args, **kwargs):
       
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school = create_school(**serializer.validated_data)
        return Response(self.OutputSerializer(school).data, status=status.HTTP_201_CREATED)
    def put(self, request, school_id, *args, **kwargs):
        school = get_object_or_404(School, id=school_id)
       
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school = update_school(school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(school).data, status=status.HTTP_202_ACCEPTED)
    def delete(self, request, school_id, *args, **kwargs):
        school = get_object_or_404(School, id=school_id)
       
        delete_school(school=school)
        return Response(status=status.HTTP_204_NO_CONTENT)
