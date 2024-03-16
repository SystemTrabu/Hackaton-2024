import os
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
from django.http import FileResponse
from nltk.metrics import edit_distance
from pyjarowinkler import distance as jwdist

global_text_data=None
global_json_data=None
global_types=None
global_types_low_match=None
global_count=None
global_porcentajetype=None
global_porcentajelow=None
global_porcentajetypeSimi=None
global_types_simi=None
global_total_data=[]
global_totalInputs=None
global_imputsNew=[]

def libreriaarea_code():
     # Diccionario que mapea los códigos de área a los estados correspondientes
    area_codes_states = {
        "201": "New Jersey", "202": "District of Columbia", "203": "Connecticut", 
        "205": "Alabama", "206": "Washington", "207": "Maine", "208": "Idaho", 
        "209": "California", "210": "Texas", "212": "New York",  
   
    }

    # Seleccionar un código de área aleatorio de la lista de claves
    random_area_code = random.choice(list(area_codes_states.keys()))

    # Obtener el estado correspondiente al código de área seleccionado
    state = area_codes_states[random_area_code]

    return random_area_code, state
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
            global global_totalInputs
            global global_imputsNew
            global global_total_data
            registros = []
            registro_nuevo = ""
            global_text_data=uploaded_file.read().decode('utf-8')
            text = uploaded_file.read().decode('utf-8')
            global_text_data = global_text_data.replace('\r', '').replace('\n', '')

            for line in text.split('\n'):
                line = line.strip()
                if 'SEED' in line:
                    # Si hay un registro acumulado, agrégalo a la lista de registros
                    if registro_nuevo:
                        registros.append(registro_nuevo)
                    # Comenzar un nuevo registro
                    registro_nuevo = ""
                registro_nuevo += line + "\n"
                
                global_imputsNew.append(registro_nuevo)
            global_totalInputs=len(registro_nuevo)+1
            global_total_data.append(registro_nuevo)
            global_total_data.append("\n")
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
        global global_types_low_match
        global global_porcentajelow
        global global_porcentajetypeSimi
        global global_types_simi
        global global_totalInputs
        global global_imputsNew
        
        # for x in range(global_totalInputs):
        #     if x>1:
        #         print(global_imputsNew, 'jeje')
            
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
                    
                        for sub_case in case['sub_cases']:
                            
                            family_distributions[sub_case['case_id']] = sub_case['distribution']
                        
                        
                        global_types = family_distributions
                        
                    
                    if case['case_id'] == 'LOW_SIMILARITY':
                        global_porcentajelow=case['distribution']
                        
                        low = {}
                        
                        for sub_case in case['sub_cases']:
                            low[sub_case['case_id']] = sub_case['distribution']
                        
                        global_types_low_match= low
                    if case['case_id']=='SIMILAR':
                        global_porcentajetypeSimi=case['distribution']
                        similar_distributions={}
                        for sub_case in case['sub_cases']:
                            similar_distributions[sub_case['case_id']]=sub_case['distribution']
                        global_types_simi=similar_distributions
       
        
              
                Family.run()
                Low_match.run()
                similares.run()
       
           
        return Response({'message': 'Se recibio correctamente'}, status=status.HTTP_200_OK)



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
        global global_total_data
        for x in range(count):
         
            family_structure = global_text_data.split('|') 
            seed=family_structure
            type = Family.select_structure_type(percentages)
            if type == 'TWINS':
                genero = fake.random_element(['M', 'F'])
                
                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[27] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[27] = 'M'

                ssn = family_structure[10]
                ssn_prefix = ssn[:-4] 
                ssn_suffix = ssn[-4:]  
                modified_suffix = list(ssn_suffix)  
                modified_suffix[random.randint(0, 3)] = str(fake.random_digit_or_empty())  
                new_ssn = ssn_prefix + ''.join(modified_suffix) 
                family_structure[10] = new_ssn  
                family_structure[29] = 'familary-twice'
                if random.randint(0,3)==2:
                    family_structure[24]=str(fake.random_int(7))
                    family_structure[23]=str(fake.randdom_int(4))
                family_structure[11]=fake.street_address()
                if random.randint(0,5)==2:
                    family_structure[12]=fake.secondary_address()
                family_structure[13]=fake.city()
                family_structure[14]=fake.state_abbr()
                family_structure[15]=str( fake.zipcode())
                family_structure[16]=str(fake.random_int(4))

            if type == 'PARENT_CHILD':
                genero = fake.random_element(['M', 'F'])

                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[27] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[27] = 'M'

                fecha_nacimiento_original = datetime.datetime.strptime(family_structure[9], "%Y-%m-%d")
                nueva_fecha_nacimiento = fecha_nacimiento_original + datetime.timedelta(days=20*365)
                nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                family_structure[9] = nueva_fecha_nacimiento_str

                if family_structure[5] == 'Jr':
                    numero = random.randint(0, 5)
                    if numero == 3:
                        family_structure[5] = 'Sr'
                        fecha_nacimiento_original = datetime.datetime.strptime(family_structure[9], "%Y-%m-%d")
                        nueva_fecha_nacimiento = fecha_nacimiento_original + datetime.timedelta(days=20*365)
                        nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                        family_structure[9] = nueva_fecha_nacimiento_str

                if family_structure[5] == 'Sr':
                    numero = random.randint(0, 5)
                    if numero == 3:
                        family_structure[5] = 'Jr'
                        fecha_nacimiento_original = datetime.datetime.strptime(family_structure[9], "%Y-%m-%d")
                        nueva_fecha_nacimiento = fecha_nacimiento_original - datetime.timedelta(days=20*365)
                        nueva_fecha_nacimiento_str = nueva_fecha_nacimiento.strftime("%Y-%m-%d")
                        family_structure[9] = nueva_fecha_nacimiento_str

                family_structure[29] = 'familary-parent-child'

            if type == 'SIBLINGS':
                genero = fake.random_element(['M', 'F'])

                if genero == 'F':
                    family_structure[2] = fake.first_name_female()
                    family_structure[27] = 'F'
                else:
                    family_structure[2] = fake.first_name_male()
                    family_structure[27] = 'M'

                family_structure[29] = 'familary-siblings'
                family_structure[10]= fake.ssn()
                
                if(random.randint(1,5)==3):
                    family_structure[9]=fake.date_of_birth(minimun_age=18,maximun_age=90).strftime('%Y-%m-%d')
            family_change.append('|'.join(family_structure))
        
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
            
            print(percentages, 'olaa')

        # Seleccionar y mostrar las estructuras
        if global_count is not None:
            global global_total_data
            family_count=int(global_count*global_porcentajetype)
            # for key in percentages:
            #     percentages[key]*=100
            print(family_count)
            family_structures = Family.generate_family_structures(family_count, percentages)

            for family in family_structures:
                print (family)
            
            global_total_data.append(family)
            global_total_data.append("\n")
            
            
        else:
            family_structures = Family.generate_family_structures(0, percentages)
        

class similares:
    @staticmethod
    def generate_similares_estructure(count, percentages):
        fake = Faker()
        family_change = []




class Low_match():
    structure = 'ID|Prefix|FirstName|MiddleName|LastName|Suffix|Name Alias-1|Name Alias-2|Name Alias-3|DOB|SSN|Address-1 Line 1|Address-1 Line 2|Address-1 City|Address-1 State|Address-1 Zip|Address-1 Zip4|Address-2 Line 1|Address-2 Line 2|Address-2 City|Address-2 State|Address-2 Zip|Address-2 Zip4|Phone-1 Area Code|Phone-1 Base Number|Phone-2 Area Code|Phone-2 Base Number|Gender|SimilarityScore|CASE Type'
     # Semilla original
    #seed = "123ABC||STANFORD||SMITH||MD|SMITH,STANFORD|S,F,SMOTH||1965-01-09|343679845|123 MAIN ST||MOSCOW|ID|83844||456 ELM RD||MOSCOW|ID|83844||208|3450998|208|4569845|M||1.0|SEED"

    # Función para generar estructuras familiares
    @staticmethod
    def generate_lowmatch_structures(count, percentages):
        fake = Faker()
        Low_match_change = []
        global global_text_data
        global global_total_data

        for x in range(count):
            Low_match_structure = global_text_data.split('|')
            seed=Low_match_change
           
            type = Low_match.select_structure_type(percentages)
            if type == 'NOMATCH_FN_DOB':
                area, estado=libreriaarea_code()
                Low_match_structure [1] = str (fake.prefix()) if random.choice([True,False]) else ''
                Low_match_structure [2] = fake.first_name()
                Low_match_structure [3] = fake.first_name() #middle name
                Low_match_structure [4] = fake.last_name()
                Low_match_structure [5] = str(fake.suffix() ) if random.choice([True,False]) else ''
                Low_match_structure [9] = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
                Low_match_structure [11] = fake.street_address()
                Low_match_structure [13] = fake.city()
                Low_match_structure [14] = fake.state_abbr()
                Low_match_structure [15] = str(fake.zipcode())
                Low_match_structure [16] = str(fake.random_int(4))
                Low_match_structure [17] = fake.street_address()
                Low_match_structure [19] = fake.city()
                Low_match_structure [20] = estado
                Low_match_structure [21] = str(fake.zipcode())
                Low_match_structure [22] = str(fake.random_int(4))
                Low_match_structure [23] = str(area)
                area, estado=libreriaarea_code()
                Low_match_structure [24] = str(fake.random_int(7))
                Low_match_structure [25] = str(area)
                Low_match_structure [26] = str(fake.random_int(7))
                Low_match_structure [27] = fake.random_element(['F', 'M'])
                Low_match_structure [29] = 'NOMATCH_FN_DOB'


                

            if type == 'NOMATCH_LN_DOB':
                Low_match_structure [1] = fake.prefix() if random.choice([True,False]) else ''
                Low_match_structure [2] = fake.first_name()
                Low_match_structure [3] = fake.first_name()
                Low_match_structure [5] = fake.suffix() if random.choice([True,False]) else ''
                Low_match_structure [10] = fake.ssn()
                Low_match_structure [11] = fake.street_address()
                Low_match_structure [13] = fake.city()
                Low_match_structure [14] = fake.state_abbr()
                Low_match_structure [15] = str(fake.zipcode())
                Low_match_structure [16] = str(fake.random_int(4))
                Low_match_structure [17] = fake.street_address()
                Low_match_structure [19] = fake.city()
                area, estado=libreriaarea_code()
                Low_match_structure [20] = estado
                Low_match_structure [21] = str(fake.zipcode())
                Low_match_structure [22] = str(fake.random_int(4))
                Low_match_structure [23] = str(area)
                Low_match_structure [24] = str(fake.random_int(7))
                Low_match_structure [25] = str(area)
                Low_match_structure [26] = str(fake.random_int(7))
                Low_match_structure [27] = str(fake.random_element(['F', 'M']))
                Low_match_structure [29] = 'NOMATCH_LN_DOB'
            
            if type == 'NOMATCH_SSN':
                Low_match_structure [1] = str(fake.prefix()) if random.choice([True,False]) else ''
                Low_match_structure [2] = fake.first_name()
                Low_match_structure [3] = fake.first_name()
                Low_match_structure [4] = fake.last_name()
                Low_match_structure [5] = fake.suffix()  if random.choice([True,False]) else ''
                Low_match_structure [11] = fake.street_address()
                Low_match_structure [13] = fake.city()
                Low_match_structure [14] = fake.state_abbr()
                Low_match_structure [15] = str(fake.zipcode())
                Low_match_structure [16] = str(fake.random_int(4))
                Low_match_structure [17] = fake.street_address()
                Low_match_structure [19] = fake.city()
                area, estado=libreriaarea_code()
                Low_match_structure [20] = estado
                Low_match_structure [21] = str(fake.zipcode())
                Low_match_structure [22] = str(fake.random_int(4))
                
                Low_match_structure [23] = area
                Low_match_structure [24] = str(fake.random_int(7))
                area, estado=libreriaarea_code()
                Low_match_structure [25] = area
                Low_match_structure [26] = str(fake.random_int(7))
                Low_match_structure [27] = fake.random_element(['F', 'M'])
                Low_match_structure [29] = 'NOMATCH_SSN'
            
            if type == 'NOMATCH_DOB_ZIP':
                Low_match_structure [1] = fake.prefix() if random.choice([True,False]) else ''
                Low_match_structure [2] = fake.first_name()
                Low_match_structure [3] = fake.first_name()
                Low_match_structure [4] = fake.last_name()
                Low_match_structure [5] = fake.suffix() if random.choice([True,False]) else ''
                Low_match_structure [10] = fake.ssn()
                Low_match_structure [11] = fake.street_address()
                Low_match_structure [13] = fake.city()
                Low_match_structure [14] = fake.state_abbr()
                Low_match_structure [16] = str(fake.random_number(4))
                Low_match_structure [17] = fake.street_address()
                Low_match_structure [19] = fake.city()
                area, estado=libreriaarea_code()
                Low_match_structure [20] = estado
                Low_match_structure [21] = str(fake.zipcode())
                Low_match_structure [22] = str(fake.random_number(4))
                Low_match_structure [23] = area
                Low_match_structure [24] = str(fake.random_number(7))
                area, estado=libreriaarea_code()
                Low_match_structure [25] = area
                Low_match_structure [26] = str(fake.random_number(7))
                Low_match_structure [27] = fake.random_element(['F', 'M'])
                Low_match_structure [29] = 'NOMATCH_DOB_ZIP'
    
                # similares.similitudes(global_text_data,Low_match_structure)

            Low_match_change.append('|'.join(Low_match_structure))
        
        return Low_match_change

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
        global global_types_low_match
        global global_count
        global global_porcentajelow
        # Parámetros para la cantidad de estructuras a generar
        

        # Porcentajes de cada tipo de estructura
        if global_types_low_match is not None:
            percentages = global_types_low_match
            for key in percentages:
                percentages[key]*=100

        # Seleccionar y mostrar las estructuras
        if global_count is not None:
           
            low_match_count=int(global_count*global_porcentajelow)
            # for key in percentages:
            #     percentages[key]*=100
           
            low_match_structures = Low_match.generate_lowmatch_structures(low_match_count, percentages)
            global global_total_data
            for low in low_match_structures:
                print (low)  
            global_total_data.append(low)
            global_total_data.append("\n")
        

class similares:
    @staticmethod
    def generate_similares_estructure(count, percentages):
        fake = Faker()
        family_change = []
        global global_text_data
        global global_total_data

        for x in range(count):
            family_structure = global_text_data.split('|')  # Divide la semilla en partes
            seed=family_structure

            type = similares.select_structure_type(percentages)
            if type == 'SAME':
                
                family_structure[29]='Same'
                #similitudes(family_structure)

            if type == 'TYPO':
                r = random.randint(1, 5)
                family_structure[29]='Typo'
                if(r==1):
                    firtsname=family_structure[2]
                    if(firtsname!=''):
                        family_structure[2]=family_structure[2] +firtsname[1]
                elif(r==2):
                    alias2=family_structure[7] 
                    if(alias2!=''):
                        family_structure[7]=family_structure[7] + alias2[1]
                elif(r==3):
                    lastname=family_structure[4]
                    if(lastname!=''):
                        family_structure[4]=family_structure[4]+lastname[1]
                elif(r==4):
                    SSN=family_structure[10]
                    SSN[:-1]
                    family_structure[10]=SSN[:-1]+ str(random.randint(1,9))
                else:
                    dato=family_structure[24]
                    dato[:-1]
                    family_structure[24]=dato+str(random.randint(1,9))


                numberR = random.randint(1,4)
                nombre=family_structure[2]
                if (numberR==1):
                    def introduce_typo(word, typo_probability=1):
                        if random.random() < typo_probability:
                            # Selecciona una posición aleatoria en la palabra


                            # Si la letra en la posición seleccionada es una vocal, reemplázala por otra vocal aleatoria
                            vowels = "aeiou"
                            try:
                                if word[3] in vowels:
                                    new_vowel = random.choice(vowels.replace(word[3], ""))  # Excluye la vocal original
                                    new_word = word[-1] + new_vowel + word[1 - 2:]
                                    family_structure[2]=new_word
                                    family_structure[29]='Typo'
                                else:
                                    # Si no es una vocal, reemplaza la letra por otra aleatoria
                                    new_letter = chr(random.randint(97, 122))  # Genera una letra minúscula aleatoria
                                    new_word = word[:3] + new_letter + word[3 + 1:]
                                    family_structure[2]=new_word
                                    family_structure[29]='Typo'
                            except:
                                print('algo malo')
                    original_word = nombre
                    # Introduce un error de dedo
                    introduce_typo(original_word)
                    
                elif (numberR==2):
                    def introduce_typo(word, typo_probability=1):
                        if random.random() < typo_probability:
                            # Elige una posición aleatoria en la palabra
                            position = random.randint(1,2)
                            # Obtiene la letra en la posición elegida
                            letter_to_copy = word[3] if word!='' else None
                            # Crea la nueva palabra agregando la letra en una posición aleatoria
                            new_word = word[3] + letter_to_copy + word[3] if word!='' else ''
                            family_structure[3]=new_word 
                            family_structure[29]='Typo' 
                        

                    original_word = nombre
                    introduce_typo(original_word)
                elif(numberR==3):
                    def introduce_typo(word, typo_probability=1):
                        if random.random() < typo_probability:
                            # Elige una posición aleatoria en la palabra
                            position = random.randint(0, len(word))
                            # Genera un número aleatorio
                            random_number = str(random.randint(0, 9))
                            # Inserta el número aleatorio en la posición elegida
                            new_word = word[:position] + random_number + word[position:]
                            family_structure[2]=new_word
                            family_structure[29]='Typo'
                       

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
                        family_structure[2]=word_with_number

                    # Ejemplo de uso
                    word = nombre
                    word_with_number = replace_letter_with_number(word)
                    family_structure[28]='Typo'
            family_change.append('|'.join(family_structure))
        
        
        #similitudes(seed,family_change)
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
       
        

        # Porcentajes de cada tipo de estructura
        if global_types_simi is not None:
            percentages = global_types_simi
            for key in percentages:
                percentages[key]*=100

        # Seleccionar y mostrar las estructuras
        if global_count is not None:
           

            family_count=int(global_count*global_porcentajetypeSimi)
            # for key in percentages:
            #     percentages[key]*=100
            
            family_structures = similares.generate_similares_estructure(family_count, percentages)
            global global_total_data

            for family in family_structures:
                print (family) 
            global_total_data.append(family)
            global_total_data.append("\n")
        else:
            family_structures = similares.generate_family_structures(0, percentages)
    # def similitudes(similar_structure, arco_structure):
    #     ndatos = len(similar_structure) - 2
    #     for i in range (ndatos):
    #         if(similar_structure[i]==''):
    #             similar_structure[i]="0"
    #         if(arco_structure[i]==''):
    #             arco_structure[i]="0"
                    
    #         seeds = [(similar_structure[i], arco_structure[i])]

    #                     # Calculamos las metricas de distancia pasando cada tupla como argumentos a levdist() y get_jaro_distance()
    #         for x,y in (seeds):
    #             print(f"'{x}' vs '{y}':")
    #             print("Distancia Levenshtein ->", edit_distance(x,y))
    #             print("Similitud Jaro Winkler ->",jwdist.get_jaro_distance(x,y))
    #             print("-"*40)
    #             similitud=jwdist.get_jaro_distance(x,y)
    #             print("la similitud es ",similitud)
    #             total += similitud
    #     print("pasada ",i+1)
    #     total=total/28
    #     print(total)
    #     return total







class createtxt(APIView):
    def get(self, request):
        global global_total_data
        try:
            with open('archivo.txt', 'w') as f:
                x=0
                for data in global_total_data:
                    cadena=str(data)
                    f.write(cadena)
                    print('olaaaaaa',cadena)
                    
                     
                    
            file_path = os.path.join(os.getcwd(), 'archivo.txt')
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='results.txt')
        except Exception as e:
            return Response({'error': str(e)})
