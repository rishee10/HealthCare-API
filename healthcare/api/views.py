# healthcare/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PatientView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        patient = Patient.objects.create(name=data['name'], email=data['email'], created_by=request.user)
        return Response({'message': 'Patient created successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            if patient.created_by == request.user:
                serializer = PatientSerializer(patient)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'You do not have permission to access this patient'}, status=status.HTTP_403_FORBIDDEN)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            if patient.created_by == request.user:
                data = request.data
                patient.name = data['name']
                patient.email = data['email']
                patient.save()
                return Response({'message': 'Patient updated successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'You do not have permission to update this patient'}, status=status.HTTP_403_FORBIDDEN)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            if patient.created_by == request.user:
                patient.delete()
                return Response({'message': 'Patient deleted successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'You do not have permission to delete this patient'}, status=status.HTTP_403_FORBIDDEN)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

class DoctorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        doctor = Doctor.objects.create(name=data['name'], email=data['email'])
        return Response({'message': 'Doctor created successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            data = request.data
            doctor.name = data['name']
            doctor.email = data['email']
            doctor.save()
            return Response({'message': 'Doctor updated successfully'}, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            doctor.delete()
            return Response({'message': 'Doctor deleted successfully'}, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

class PatientDoctorMappingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        patient = Patient.objects.get(pk=data['patient_id'])
        doctor = Doctor.objects.get(pk=data['doctor_id'])
        if patient.created_by == request.user:
            mapping = PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
            return Response({'message': 'Patient-Doctor mapping created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'You do not have permission to create this mapping'}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        mappings = PatientDoctorMapping.objects.all()
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientDoctorMappingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(pk=pk)
            serializer = PatientDoctorMappingSerializer(mapping)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PatientDoctorMapping.DoesNotExist:
            return Response({'error': 'Mapping not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(pk=pk)
            if mapping.patient.created_by == request.user:
                mapping.delete()
                return Response({'message': 'Mapping deleted successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'You do not have permission to delete this mapping'}, status=status.HTTP_403_FORBIDDEN)
        except PatientDoctorMapping.DoesNotExist:
            return Response({'error': 'Mapping not found'}, status=status.HTTP_404_NOT_FOUND)

class PatientDoctorMappingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
            if patient.created_by == request.user:
                mappings = PatientDoctorMapping.objects.filter(patient=patient)
                serializer = PatientDoctorMappingSerializer(mappings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'You do not have permission to access these mappings'}, status=status.HTTP_403_FORBIDDEN)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
