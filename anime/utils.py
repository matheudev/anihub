import xml.etree.ElementTree as ET

def parse_anime_ids_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    anime_data = []

    for anime in root.findall('anime'):
        anime_id = int(anime.find('series_animedb_id').text)
        status = anime.find('my_status').text

        if status not in ('', 'On Hold'):
            anime_data.append({'anime_id': anime_id, 'status': status.lower()})

    return anime_data
