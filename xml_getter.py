import xml.etree.ElementTree as etree
import re
import csv

def get_name_space(tag: str) -> str:
    match = re.search(r'{(.*)}', tag)
    return match.group()

def get_xml_elements(path: str, element: str) -> list[tuple[str, str, str, str]]:
    tree = etree.parse(path)
    root = tree.getroot()
    namespace = get_name_space(root.tag)
    all_products = tree.findall(f'.//{namespace}{element}')

    result = []

    for product in all_products:
        # They Could return None
        x_prod = product.find(f'.//{namespace}xProd').text
        c_prod = product.find(f'.//{namespace}cProd').text
        c_ean = product.find(f'.//{namespace}cEAN').text
        c_ean_trib = product.find(f'.//{namespace}cEANTrib').text
        result.append((
            "" if x_prod is None else x_prod, 
            "" if c_prod is None else c_prod,
            "" if c_ean is None else c_ean, 
            "" if c_ean_trib is None else c_ean_trib,
        ))
    
    return result



if __name__ == '__main__':
    products_data = get_xml_elements('biape.xml', 'prod')
    
    with open('results.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')
        for product_data in products_data:
            writer.writerow(product_data)
        