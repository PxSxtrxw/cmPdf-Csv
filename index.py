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
    current_codes = []
    current_descriptions = []

    for line in lines:
        # Tratar de emparejar líneas con el formato de código seguido de descripción
        match = re.match(r'^(\d{1,4}\s?\d*)\s+(.*)$', line)
        if match:
            if current_codes and current_descriptions:
                # Guardar los códigos y descripciones actuales si hay información previa
                for code in current_codes:
                    parsed_data.append({'CÓDIGO': code, 'DESCRIPCIÓN': ' '.join(current_descriptions).strip()})
                current_codes = []
                current_descriptions = []
            
            # Establecer nuevo código y descripción
            current_code = match.group(1).replace(' ', '')  # Unificar el código eliminando espacios
            current_description = match.group(2).strip()
            
            # Dividir la línea en partes usando coma como separador y limpiar los espacios
            parts = [part.strip() for part in re.split(r'(?<=\d)\s+(?=\D)', current_description)]
            
            if len(parts) > 1:
                current_code = current_code[:4] + parts[0]
                current_description = parts[1]
            
            # Guardar el código y descripción
            parsed_data.append({'CÓDIGO': current_code, 'DESCRIPCIÓN': current_description})
            
        else:
            match_general = re.match(r'^([A-Z])\s+(.*)$', line)
            if match_general:
                if current_codes and current_descriptions:
                    # Guardar los códigos y descripciones actuales si hay información previa
                    for code in current_codes:
                        parsed_data.append({'CÓDIGO': code, 'DESCRIPCIÓN': ' '.join(current_descriptions).strip()})
                    current_codes = []
                    current_descriptions = []
                
                # Establecer nuevo código y descripción general
                current_code = match_general.group(1)
                current_description = match_general.group(2).strip()
                parsed_data.append({'CÓDIGO': current_code, 'DESCRIPCIÓN': current_description})
                
            else:
                # Agregar la línea a la descripción actual
                current_descriptions.append(line.strip())

    # Asegurarse de guardar la última línea procesada si hay códigos y descripciones restantes
    if current_codes and current_descriptions:
        for code in current_codes:
            parsed_data.append({'CÓDIGO': code, 'DESCRIPCIÓN': ' '.join(current_descriptions).strip()})

    return parsed_data

def save_to_csv(data, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
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
