# api/views.py
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class JSONUploadView(APIView):
    
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('json_file')
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Lee el contenido del archivo JSON
            json_data = json.load(uploaded_file)
            datosJson=json_data
            print(json_data)
            # Aquí puedes realizar cualquier operación con los datos JSON, como procesamiento, análisis, etc.
            return Response({'message': 'Archivo JSON subido exitosamente', 'data': json_data}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({'error': 'El archivo subido no es un archivo JSON válido'}, status=status.HTTP_400_BAD_REQUEST)
 