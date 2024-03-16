from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import datetime
from faker import Faker
import random
import datetime
import random
from faker import Faker

global_text_data=None
global_json_data=None
global_types=None
global_count=None
global_porcentajetype=None
global_porcentajetypeSimi=None
global_types_simi=None
global_total_data=[]
class JSONUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('json_file')
        global global_text_data
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            global global_json_data  # Acceder a la variable global
            # Lee el contenido del archivo JSON
            global_json_data = json.load(uploaded_file)
            print(global_text_data, 'probandoo')
            # Aquí puedes realizar cualquier operación con los datos JSON, como procesamiento, análisis, etc.
            return Response({'message': 'Archivo JSON subido exitosamente', 'data': global_json_data}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({'error': 'El archivo subido no es un archivo JSON válido'}, status=status.HTTP_400_BAD_REQUEST)

class TextUploadView(APIView):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('text_file')
        if not uploaded_file:
            return Response({'error': 'No se ha proporcionado ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            global global_text_data
            # Lee el contenido del archivo de texto
            text = uploaded_file.read().decode('utf-8')
            global_text_data=text.rstrip()
            # Aquí puedes realizar cualquier operación con los datos de texto
            
            
            return Response({'message': 'Archivo TXT subido exitosamente', 'data': global_text_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Error al procesar el archivo de texto: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)


class Generate(APIView):
    def get(self, request, *args, **kwargs):
        global global_json_data
        global global_types
        global global_count
        global global_porcentajetype
        global global_porcentajetypeSimi
        global global_types_simi
        # Verificar si global_json_data no es nulo y si contiene la clave "cases"
        if global_json_data and 'cases' in global_json_data:
            global_count = global_json_data['records_per_arc']
            # Iterar sobre los casos en global_json_data
            for case in global_json_data['cases']:
                
                # Verificar si el caso es de tipo "FAMILY"
                if case['case_id'] == 'FAMILY':
                    # Obtener el valor de "distribution" y guardarlo en global_count
                    global_porcentajetype=case['distribution']
                    
                    # Inicializar un diccionario para almacenar los subcasos y sus distribuciones
                    family_distributions = {}
                    
                    # Iterar sobre los subcasos en el caso "FAMILY"
                    for sub_case in case['sub_cases']:
                        # Guardar el subcaso y su distribución en el diccionario
                        family_distributions[sub_case['case_id']] = sub_case['distribution']
                    
                    # Asignar el diccionario a global_types
                    global_types = family_distributions
                    print(global_types)  # Mostrar global_types en la consola
                      # Salir del bucle una vez que se haya encontrado el caso "FAMILY"
                
                if case['case_id']=='SIMILAR':
                    global_porcentajetypeSimi=case['distribution']
                    similar_distributions={}
                    for sub_case in case['sub_cases']:
                        similar_distributions[sub_case['case_id']]=sub_case['distribution']
                    global_types_simi=similar_distributions
                    
        print('ola')     
        Family.run()
        similares.run()
        return Response({'message': 'Subcasos de FAMILY y sus distribuciones', 'data': family_distributions}, status=status.HTTP_200_OK)



class Family:
    estructura = 'ID|Prefix|FirstName|MiddleName|LastName|Suffix|Name Alias-1|Name Alias-2|Name Alias-3|DOB|SSN|Address-1 Line 1|Address-1 Line 2|Address-1 City|Address-1 State|Address-1 Zip|Address-1 Zip4|Address-2 Line 1|Address-2 Line 2|Address-2 City|Address-2 State|Address-2 Zip|Address-2 Zip4|Phone-1 Area Code|Phone-1 Base Number|Phone-2 Area Code|Phone-2 Base Number|Gender|SimilarityScore|CASE Type'

    # Semilla original
    #seed = "123ABC||STANFORD||SMITH||MD|SMITH,STANFORD|S,F,SMOTH||1965-01-09|343679845|123 MAIN ST||MOSCOW|ID|83844||456 ELM RD||MOSCOW|ID|83844||208|3450998|208|4569845|M||1.0|SEED"

    # Función para generar estructuras familiares
    @staticmethod
    def generate_family_structures(count, percentages):
        fake = Faker()
        family_change = []
        global global_text_data

        for x in range(count):
            family_structure = global_text_data.split('|')  # Divide la semilla en partes
            type = Family.select_structure_type(percentages)
            global global_total_data
            if x<1:
                global_total_data.append(global_text_data.split('|'))

            if type == 'TWINS':
                genero = fake.random_element(['M', 'F'])
                
                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[28] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[28] = 'M'

                ssn = family_structure[11]
                ssn_prefix = ssn[:-4] 
                ssn_suffix = ssn[-4:]  
                modified_suffix = list(ssn_suffix)  
                modified_suffix[random.randint(0, 3)] = str(fake.random_digit_or_empty())  
                new_ssn = ssn_prefix + ''.join(modified_suffix) 
                family_structure[11] = new_ssn  
                family_structure[31] = 'familary-twice'

            if type == 'PARENT_CHILD':
                genero = fake.random_element(['M', 'F'])

                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[28] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[28] = 'M'

                fecha_nacimiento_original = datetime.datetime.strptime(family_structure[10], "%Y-%m-%d")
                nueva_fecha_nacimiento = fecha_nacimiento_original + datetime.timedelta(days=20*365)
                nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                family_structure[10] = nueva_fecha_nacimiento_str

                if family_structure[6] == 'Jr':
                    numero = random.randint(0, 5)
                    if numero == 3:
                        family_structure[6] = 'Sr'
                        fecha_nacimiento_original = datetime.datetime.strptime(family_structure[10], "%Y-%m-%d")
                        nueva_fecha_nacimiento = fecha_nacimiento_original + datetime.timedelta(days=20*365)
                        nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                        family_structure[10] = nueva_fecha_nacimiento_str

                if family_structure[6] == 'Sr':
                    numero = random.randint(0, 5)
                    if numero == 3:
                        family_structure[6] = 'Jr'
                        fecha_nacimiento_original = datetime.datetime.strptime(family_structure[10], "%Y-%m-%d")
                        nueva_fecha_nacimiento = fecha_nacimiento_original - datetime.timedelta(days=20*365)
                        nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                        family_structure[10] = nueva_fecha_nacimiento_str

                family_structure[31] = 'familary-parent-child'

            if type == 'SIBLINGS':
                genero = fake.random_element(['M', 'F'])

                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[28] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[28] = 'M'

                family_structure[31] = 'familary-siblings'

            family_change.append('|'.join(family_structure))      
            global_total_data.append(family_change)
            

        return family_change

    # Función para seleccionar el tipo de estructura según los porcentajes
    @staticmethod
    def select_structure_type(percentages):
        rand_num = random.uniform(0, 100)
        cumulative_prob = 0

        for type, percentage in percentages.items():
            cumulative_prob += percentage
            if rand_num <= cumulative_prob:
                return type

    @staticmethod
    def run():
        global global_types
        global global_count
        global global_porcentajetype
        # Parámetros para la cantidad de estructuras a generar
        

        # Porcentajes de cada tipo de estructura
        if global_types is not None:
            percentages = global_types
            for key in percentages:
                percentages[key]*=100

        # Seleccionar y mostrar las estructuras
        if global_count is not None:
            print(global_count, 'ola')
            print(global_porcentajetype, 'ola')
            print(percentages)

            family_count=int(global_count*global_porcentajetype)
            # for key in percentages:
            #     percentages[key]*=100
            print(percentages, 'new')
            print(family_count)
            family_structures = Family.generate_family_structures(family_count, percentages)

            for family in family_structures:
                print (family)
                
            
            
        else:
            family_structures = Family.generate_family_structures(0, percentages)
        



class Low_match():
    structure = 'ID|Prefix|FirstName|MiddleName|LastName|Suffix|Name Alias-1|Name Alias-2|Name Alias-3|DOB|SSN|Address-1 Line 1|Address-1 Line 2|Address-1 City|Address-1 State|Address-1 Zip|Address-1 Zip4|Address-2 Line 1|Address-2 Line 2|Address-2 City|Address-2 State|Address-2 Zip|Address-2 Zip4|Phone-1 Area Code|Phone-1 Base Number|Phone-2 Area Code|Phone-2 Base Number|Gender|SimilarityScore|CASE Type'

class similares:
    @staticmethod
    def generate_similares_estructure(count, percentages):
        fake = Faker()
        family_change = []
        global global_text_data
        

        for x in range(count):
            global global_total_data
            family_structure = global_text_data.split('|')  # Divide la semilla en partes
            if x<1 :
                global_total_data=global_text_data.split('|')

            type = similares.select_structure_type(percentages)
            if type == 'SAME':
                print(global_text_data)
                family_structure[31]='Same'
                print('ola')

            if type == 'TYPO':
                r = random.randint(1, 5)
                family_structure[31]='Typo'
                if(r==1):
                    firtsname=family_structure[3]
                    family_structure[3]=family_structure[3] +firtsname[1]
                elif(r==2):
                    alias2=family_structure[8] 
                    family_structure[8]=family_structure[3] + alias2[1]
                elif(r==3):
                    lastname=family_structure[5]
                    family_structure[5]=family_structure[5]+lastname[1]
                elif(r==4):
                    SSN=family_structure[11]
                    SSN[:-1]
                    family_structure[11]=SSN[:-1]+ str(random.randint(1,9))
                else:
                    dato=family_structure[25]
                    dato[:-1]
                    family_structure[25]=dato+str(random.randint(1,9))


                numberR = random.randint(1,4)
                nombre=family_structure[3]
                if (numberR==1):
                    def introduce_typo(word, typo_probability=1):
                        if random.random() < typo_probability:
                            # Selecciona una posición aleatoria en la palabra
                            index = random.randint(0, len(word) - 1)
                            # Si la letra en la posición seleccionada es una vocal, reemplázala por otra vocal aleatoria
                            vowels = "aeiou"
                            if word[index] in vowels:
                                new_vowel = random.choice(vowels.replace(word[index], ""))  # Excluye la vocal original
                                new_word = word[:index] + new_vowel + word[index + 1:]
                                family_structure[3]=new_word
                                family_structure[31]='Typo'
                            else:
                                # Si no es una vocal, reemplaza la letra por otra aleatoria
                                new_letter = chr(random.randint(97, 122))  # Genera una letra minúscula aleatoria
                                new_word = word[:index] + new_letter + word[index + 1:]
                                family_structure[3]=new_word
                                family_structure[31]='Typo'
                        
                    original_word = dato
                    # Introduce un error de dedo
                    typo_word = introduce_typo(original_word)
                    
                elif (numberR==2):
                    def introduce_typo(word, typo_probability=1):
                        if random.random() < typo_probability:
                            # Elige una posición aleatoria en la palabra
                            position = random.randint(0, len(word) - 1)
                            # Obtiene la letra en la posición elegida
                            letter_to_copy = word[position]
                            # Crea la nueva palabra agregando la letra en una posición aleatoria
                            new_word = word[:position] + letter_to_copy + word[position:]
                            family_structure[3]=new_word
                            family_structure[31]='Typo'
                        

                    original_word = nombre
                    typo_word = introduce_typo(original_word)
                elif(numberR==3):
                    def introduce_typo(word, typo_probability=1):
                        if random.random() < typo_probability:
                            # Elige una posición aleatoria en la palabra
                            position = random.randint(0, len(word))
                            # Genera un número aleatorio
                            random_number = str(random.randint(0, 9))
                            # Inserta el número aleatorio en la posición elegida
                            new_word = word[:position] + random_number + word[position:]
                            family_structure[3]=new_word
                            family_structure[31]='Typo'
                       

                    # Palabra original
                    original_word = nombre
                    # Introduce un error de dedo
                    typo_word = introduce_typo(original_word)
                    
                    
                else:
                    def replace_letter_with_number(word):
                        if not word:
                            return word
                        # Selecciona una posición aleatoria en la palabra
                        random_index = random.randint(0, len(word) - 1)
                        # Genera un dígito aleatorio entre 0 y 9
                        random_digit = random.randint(0, 9)
                        # Reemplaza la letra en la posición aleatoria por el dígito aleatorio
                        word_with_number = word[:random_index] + str(random_digit) + word[random_index + 1:]
                        family_structure[3]=word_with_number

                    # Ejemplo de uso
                    word = nombre
                    word_with_number = replace_letter_with_number(word)
                    family_structure[31]='Typo'
            family_change.append('|'.join(family_structure))
            global_total_data.append(family_change)
            

        return family_change

    def select_structure_type(percentages):
        rand_num = random.uniform(0, 100)
        cumulative_prob = 0

        for type, percentage in percentages.items():
            cumulative_prob += percentage
            if rand_num <= cumulative_prob:
                return type

    def run():
        global global_types_simi
        global global_count
        global global_porcentajetypeSimi

        #este es de prueba
        global global_total_data
        print('Aqui inicia el global',global_total_data)
        # Parámetros para la cantidad de estructuras a generar
        

        # Porcentajes de cada tipo de estructura
        if global_types_simi is not None:
            percentages = global_types_simi
            for key in percentages:
                percentages[key]*=100

        # Seleccionar y mostrar las estructuras
        if global_count is not None:
            print(global_count, 'ola')
            print(global_porcentajetypeSimi, 'ola')
            print(percentages)

            family_count=int(global_count*global_porcentajetypeSimi)
            # for key in percentages:
            #     percentages[key]*=100
            print(percentages, 'new')
            print(family_count)
            family_structures = similares.generate_similares_estructure(family_count, percentages)

            for family in family_structures:
                print (family) 
        else:
            family_structures = similares.generate_family_structures(0, percentages)