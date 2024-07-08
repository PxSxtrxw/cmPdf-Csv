import PyPDF2
import csv
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def parse_text(text):
    lines = text.split('\n')
    parsed_data = []
    current_code = None
    current_description = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Tratar de emparejar líneas con el formato de código seguido de descripción
        match = re.match(r'^(\d{1,4}\s?\d*)\s+(.*)$', line)
        if match:
            if current_code is not None:
                # Guardar el código y descripción actual si hay información previa
                parsed_data.append({'CÓDIGO': current_code, 'DESCRIPCIÓN': ' '.join(current_description).strip()})
            # Establecer nuevo código y descripción
            current_code = match.group(1).replace(' ', '')  # Unificar el código eliminando espacios
            current_description = [match.group(2).strip()]
            
            # Buscar y extraer números de la descripción para unificar con el código
            description_numbers = re.findall(r'(\d+)', current_description[0])
            if description_numbers:
                for number in description_numbers:
                    current_code += number
            
            # Eliminar los números de la descripción
            current_description[0] = re.sub(r'\d+', '', current_description[0]).strip()
            
        else:
            match_general = re.match(r'^([A-Z])\s+(.*)$', line)
            if match_general:
                if current_code is not None:
                    # Guardar el código y descripción actual si hay información previa
                    parsed_data.append({'CÓDIGO': current_code, 'DESCRIPCIÓN': ' '.join(current_description).strip()})
                # Establecer nuevo código y descripción general
                current_code = match_general.group(1)
                current_description = [match_general.group(2).strip()]
            else:
                # Si no hay coincidencia, agregar la línea a la descripción actual
                current_description.append(line.strip())

    # Asegurarse de guardar la última línea procesada
    if current_code is not None:
        parsed_data.append({'CÓDIGO': current_code, 'DESCRIPCIÓN': ' '.join(current_description).strip()})

    return parsed_data

def save_to_csv(data, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['CÓDIGO', 'DESCRIPCIÓN']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    pdf_path = 'pdf.pdf'  # Reemplaza con la ruta de tu archivo PDF
    csv_path = 'salida.csv'  # Reemplaza con la ruta de tu archivo CSV de salida

    text = extract_text_from_pdf(pdf_path)
    parsed_data = parse_text(text)
    save_to_csv(parsed_data, csv_path)
    print(f'Datos extraídos y guardados en {csv_path}')

if __name__ == "__main__":
    main()
