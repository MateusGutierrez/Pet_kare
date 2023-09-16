from rest_framework.views import Request, Response, status, APIView
from rest_framework.pagination import PageNumberPagination
from pets.models import Pet
from pets.serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from django.shortcuts import get_object_or_404


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request) -> Response:
        trait_param = req.query_params.get("trait", None)
        print(trait_param)
        if trait_param:
            pets = Pet.objects.filter(traits__name=trait_param)
        else:
            pets = Pet.objects.all()
        result = self.paginate_queryset(pets, req)
        serializer = PetSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        group_data = serializer.validated_data.pop("group")
        try:
            validate_group = Group.objects.get(
                scientific_name__iexact=group_data["scientific_name"]
            )

        except Group.DoesNotExist:
            validate_group = Group.objects.create(**group_data)

        trait_data = serializer.validated_data.pop("traits")

        created_pet = Pet.objects.create(
            **serializer.validated_data, group=validate_group
        )
        for trait in trait_data:
            try:
                validate_trait = Trait.objects.get(name__iexact=trait["name"])
            except Trait.DoesNotExist:
                validate_trait = Trait.objects.create(**trait)
            created_pet.traits.add(validate_trait)

        serializer = PetSerializer(created_pet)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def patch(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=req.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        trait_data = serializer.validated_data.pop("traits", None)
        group_data = serializer.validated_data.pop("group", None)
        if group_data:
            group, _ = Group.objects.get_or_create(
                scientific_name__iexact=group_data["scientific_name"],
                defaults=group_data,
            )
            pet.group = group
        if trait_data:
            traits_to_add = []
            for current_trait in trait_data:
                trait = Trait.objects.filter(name__iexact=current_trait["name"]).first()
                if not current_trait:
                    trait = Trait.objects.create(**current_trait)
                traits_to_add.append(trait)
        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)
        pet.save()
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def delete(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
