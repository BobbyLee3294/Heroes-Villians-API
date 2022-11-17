from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super
from super_types.models import SuperType

@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':

        super_type_param = request.query_params.get('super_type')
        supers = Super.objects.all()
        super_filter = supers.filter(super_type__type=super_type_param)

        heroes = supers.filter(super_type__type='hero')
        villains = supers.filter(super_type__type='villain')

        hero_serializer = SuperSerializer(heroes, many=True)
        villain_serializer = SuperSerializer(villains, many=True)

        if super_type_param:
            super_serializer = SuperSerializer(super_filter, many=True)
            return Response(super_serializer.data, status=status.HTTP_200_OK)
       
        custom_response_dictionary = {
            "Heroes": hero_serializer.data,
            "Villains": villain_serializer.data,
        }
        return Response(custom_response_dictionary, status=status.HTTP_200_OK)

    if request.method =='POST':

        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def supers_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)

    if request.method == 'GET':
        serializer = SuperSerializer(super)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)