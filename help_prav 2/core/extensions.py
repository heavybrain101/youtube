from rest_framework import viewsets, generics

from core.response import CustomResponse


class CustomResponseViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return CustomResponse(response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return CustomResponse(response.data, status=response.status_code)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return CustomResponse(response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return CustomResponse(response.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return CustomResponse(status=response.status_code)


class CustomRetrieveViewSet(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return CustomResponse(response.data)


class CustomRetrieveUpdateViewSet(generics.RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return CustomResponse(response.data)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return CustomResponse(response.data)

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return CustomResponse(response.data)
