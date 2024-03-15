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
        
class TextUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('text_file')
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Lee el contenido del archivo de texto
            text_data = uploaded_file.read().decode('utf-8')
            datos_txt = text_data
            print(text_data)
            # Aquí puedes realizar cualquier operación con los datos de texto
            return Response({'message': 'Archivo TXT subido exitosamente', 'data': text_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Error al procesar el archivo de texto: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)