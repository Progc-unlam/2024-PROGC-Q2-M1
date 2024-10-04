import os
import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()

# URL de inicio de sesion y de la pagina de contenidos
login_url = 'https://miel.unlam.edu.ar/principal/event/login/'
contents_url = 'https://miel.unlam.edu.ar/principal/interno/'
base_directory = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(base_directory, "pdfs")
credentials = {
    'usuario': '111222333444',
    'clave': '111222333444'
}
absolute_path = os.path.abspath(base_path)
print(f"Los archivos se guardarán en: {absolute_path}")

if not os.path.exists(base_path):
    os.makedirs(base_path)

# inicio sesion
login_response = session.post(login_url, data=credentials)

if login_response.status_code != 200:
    print("Error al iniciar sesion")
    exit()

login_response_json = login_response.json()

if login_response_json.get("estado") != 0:
    print(
        f"Error al hacer la solicitud de inicio de sesión: {login_response.status_code}")
    exit()


# Accedo a la pagina de contenidos
contents_response = session.get(contents_url)

if contents_response.status_code != 200:
    print(
        f"Error al acceder a la pagina de contenidos: {contents_response.status_code}")
    exit()


contents_soup = BeautifulSoup(
    contents_response.content, 'html.parser')

print("Acceso a la pagina de contenidos exitoso")

subject_links = contents_soup.find_all('div', class_="materia-bloque")

# accedo a cada bloque de materia               //// TODO: hilos o procesos por cada uno, todo lo de abajo a una funcion y le mandamos los hilos a ejecutar
for subject in subject_links:  # archivos de principal/interno

    subject_title = subject.find(
        'div', class_="materia-titulo").get_text(strip=True)
    # creo la carpeta por cada materia
    subject_path = os.path.join(base_path, subject_title)
    if not os.path.exists(subject_path):
        os.makedirs(subject_path)

    subject_link = subject.find(
        'a', href=True, class_="w3-col w3-padding-8 w3-center w3-hover-green w3-hover-text-white")

    href = subject_link['href']

    # accedo a los modulos de la materia
    subject_response = session.get(href)
    subject_soup = BeautifulSoup(
        subject_response.content, 'html.parser')

    modules = subject_soup.find_all('div', class_="desplegarModulo")

    for module in modules:
        module_tittle = module.find('span').get_text(strip=True)

        module_path = os.path.join(subject_path, module_tittle)
        if not os.path.exists(module_path):
            os.makedirs(module_path)

        unit_container = module.find_next_sibling(
            'div', class_='w3-accordion-content')
        unit_table = unit_container.find_all('table', class_='w3-table')

        # accedo a las unidades de cada modulo
        for table in unit_table:
            unit_tittle = table.find(
                'th', colspan="2").contents[0].get_text(strip=True)  # contents[0] porque no hay un span en el encabezado, y el get_text te trae todo incluyendo lo que idce en el <o> y <div> interno
            # le saco los caracteres basura para crear la carpeta
            unit_tittle = re.sub(r'[<>:"/\\|?*]', '_', unit_tittle)

            unit_path = os.path.join(
                module_path, unit_tittle.replace(' ', '_'))

            if not os.path.exists(unit_path):
                os.makedirs(unit_path)

            pdf_links = table.find_all('a', href=True)
            for link in pdf_links:  # busco los .pdf de contenido // posiblemente hago lo mismo que arriba y obtengo el div para sacar el titulo y crear la carpeta
                href = link['href']

                if "descargarElemento" in href:
                    print(f"Descargando {href}...")

                    pdf_response = session.get(href)  # descargo pdf
                    if pdf_response.status_code == 200:
                        # usan 5C como prefijo
                        file_name = os.path.basename(
                            href.split('/')[-3])

                        # TODO: hay otros caracteres raros aparte del 5C_
                        file_name = file_name.split('5C_', 1)[-1]

                        file_path = os.path.join(unit_path, file_name)
                        with open(file_path, 'wb') as pdf_file:
                            pdf_file.write(pdf_response.content)
                            print(
                                f"Archivo {file_name} descargado en {file_path}.")
                    else:
                        print(
                            f"Error al descargar el archivo")
