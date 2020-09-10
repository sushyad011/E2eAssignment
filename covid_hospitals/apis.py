from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BedStatusSerializers, GetPatientsListSerializer, GetBedListSerializer

from .models import Bed, Patient


class NewPatient(APIView):
    """
    New Patient get admitted if the requested bed is available.
    params: name, requested bed type
    """

    def post(self,request):

        name = request.data.get('name')
        bed_type = request.data.get('bed_type')

        if not name or not bed_type:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error_msg': 'Please provide name annd bed_type',
                },status=status.HTTP_400_BAD_REQUEST
            )

        bed = Bed.objects.filter(status='empty', type=bed_type).order_by('bed_id').first()
        if bed:
            patient = Patient.objects.create(name=name, assigned_bed=bed)
            bed.status = 'full'
            bed.save()

            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'New patient admitted successfully. Assigned bed no.' + str(bed.bed_id)
                },status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': status.HTTP_204_NO_CONTENT,
                    'message': 'No bed available of this type.'
                }
            )


class BedStatusBasedOnId(APIView):
    """
    Return Bed status with patient name if occupied
    params: bed id
    """

    def get(self,request,pk):

        try:
            queryset = Bed.objects.get(bed_id=pk)
            serializers = BedStatusSerializers(queryset)

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Status fetched',
                    'data': serializers.data,
                },status=status.HTTP_200_OK
            )
        except Bed.DoesNotExist:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Invalid id'
                },status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error_message': str(e),
                },status=status.HTTP_400_BAD_REQUEST
            )

class PatientCheckout(APIView):
    """
    Patient checkout
    params: patient id
    """

    def post(self,request,pk):

        try:
            patient = Patient.objects.get(id=pk)
            if not patient.active:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Already checked out'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            bed = Bed.objects.get(bed_id = patient.assigned_bed.bed_id)
            bed.status = 'empty'
            patient.active = False
            patient.save()
            bed.save()

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Checkout successfully'
                },status=status.HTTP_200_OK
            )

        except Patient.DoesNotExist:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Patient not found'
                },status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': str(e),
                },status=status.HTTP_400_BAD_REQUEST
            )


class GetPatientsListBasedOnBedType(APIView):
    """
    Return patient list based on bed type specified in the query params.
    """

    def get(self,request):
        bed_type = request.GET.get('bed_type')

        queryset = Patient.objects.filter(assigned_bed__type=bed_type,active=True)
        serializer = GetPatientsListSerializer(queryset,many=True)

        return Response(
            {
                'status': status.HTTP_200_OK,
                'data': serializer.data,
            },status=status.HTTP_200_OK
        )

class BedListBasedOnBedType(APIView):
    """
    Return bed list details based on bed type specified in the query params.
    """

    def get(self,request):
        bed_type = request.GET.get('bed_type')
        queryset = Bed.objects.filter(type=bed_type)
        serializer = GetBedListSerializer(queryset,many=True)

        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Bed details fetched successfully',
                'data': serializer.data
            },status=status.HTTP_200_OK
        )


class GetBedListBasedOnStatus(APIView):
    """
    Return bed list based on bed status specified in the query params
    """

    def get(self,request):
        bed_status = request.GET.get('status')

        queryset = Bed.objects.filter(status=bed_status)
        serializer = GetBedListSerializer(queryset,many=True)

        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Bed list fetched successfully',
                'data': serializer.data,
            },status=status.HTTP_200_OK
        )