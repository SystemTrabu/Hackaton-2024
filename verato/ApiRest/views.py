from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

# Variable global para almacenar el JSON
global_json_data = None
global_text_data=None

class JSONUploadView(APIView):
    def post(self, request, *args, **kwargs):
        global global_json_data  # Acceder a la variable global
        uploaded_file = request.FILES.get('json_file')
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Lee el contenido del archivo JSON
            global_json_data = json.load(uploaded_file)
            # Aquí puedes realizar cualquier operación con los datos JSON, como procesamiento, análisis, etc.
            return Response({'message': 'Archivo JSON subido exitosamente', 'data': global_json_data}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({'error': 'El archivo subido no es un archivo JSON válido'}, status=status.HTTP_400_BAD_REQUEST)

class TextUploadView(APIView):
    def post(self, request, *args, **kwargs):
        global global_text_data
        global global_json_data  # Acceder a la variable global
        uploaded_file = request.FILES.get('text_file')
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Lee el contenido del archivo de texto
            text_data = uploaded_file.read().decode('utf-8')
            global_text_data= text_data
            
            print(text_data)
            # Aquí puedes realizar cualquier operación con los datos de texto
            generate.print()
            return Response({'message': 'Archivo TXT subido exitosamente', 'data': text_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Error al procesar el archivo de texto: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)


class generate(APIView):
    def print():
        global global_json_data
        distributions_porcentaje=[]
        if global_json_data and 'cases' in global_json_data:
            for case in global_json_data['cases']:
                if 'distribution' in case:
                    distribution = case['distribution']
                    distributions_porcentaje.append(distribution*100)
                    print("Distribution:", distribution)
            else:
                print("Distribution no encontrada en el objeto JSON")
        
        print(distributions_porcentaje, 'jejeje')
