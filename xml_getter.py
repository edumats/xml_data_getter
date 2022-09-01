import argparse
import csv
import os
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import ParseError


def get_xml_elements(path: str,
                     element: str) -> list[tuple[str, str, str, str]]:
    """
    Receives a path to xml file and element type to retrieve
    Returns a list of tuples, containing:
    product description
    product code
    EAN code
    EAN trib code
    file path
    """
    tree = etree.parse(path)
    all_elements = tree.findall(f'.//{{*}}{element}')
    x_nome = tree.find('.//{*}xNome')

    result = []

    # If no elements were found, return empty list
    if not all_elements:
        return result

    for product in all_elements:
        # They Could return None
        x_prod = product.find('.//{*}xProd')
        c_prod = product.find('.//{*}cProd')
        c_ean = product.find('.//{*}cEAN')

        # Append empty string if None
        result.append((
            "" if c_prod is None else c_prod.text,
            "" if x_prod is None else x_prod.text,
            "" if c_ean is None else c_ean.text,
            "" if x_nome is None else x_nome.text,
            os.path.basename(path),
        ))

    return result


def get_file_paths(path, extension):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)


if __name__ == '__main__':
    # Argparse configuration
    parser = argparse.ArgumentParser(
        description='Extract data from .xml files'
    )
    parser.add_argument('-d', '--directory', type=str, help='target directory')
    parser.add_argument('-f', '--file', type=str, help='name of results file')
    args = parser.parse_args()

    # If target file does not exist, create file with headers
    if not os.path.isfile(args.file):
        with open(args.file, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerow([
                'Código Produto',
                'Descrição Produto',
                'EAN',
                'Nome Fornecedor',
                'Arquivo'
            ])
    # Yields a file path to a .xml file at each iteration
    for path in get_file_paths(args.directory, '.xml'):
        # Get all products data contained in a file
        try:
            products_data = get_xml_elements(path, 'prod')
        except ParseError:
            print(f'Error ocurred when parsing file {path}')
            continue

        # Pass iteration if no products were found on file
        if not products_data:
            continue

        # Appends product data to results file
        with open(args.file, mode='a') as file:
            writer = csv.writer(
                file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_NONNUMERIC
            )
            for product_data in products_data:
                writer.writerow(product_data)
