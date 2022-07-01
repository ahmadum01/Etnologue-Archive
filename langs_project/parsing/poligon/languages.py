import parsing.poligon.config as config
import requests
import json
import csv
from bs4 import BeautifulSoup
from os import path


HOST = "https://www.ethnologue.com"
LANG_LETTERS = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ǀ ǂ ǁ'.replace(" ", '').lower()
ISO_LETTERS = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.replace(" ", '').lower()
RES_PATH = path.join(path.split(__file__)[0], 'res')
CLASSES_FOR_PARSE = {
    'language_of': 'field-name-a-language-of',
    'iso_6393': 'field-name-language-iso-link-to-sil-org',
    'autonym': 'field-name-field-autonym',
    'alternate_names': 'field-name-field-alternate-names',
    'user_population': 'field-name-field-population',
    'location': 'field-name-field-region',
    'language_maps': 'view-display-id-entity_view_1',
    'language_status': 'field-name-language-status',
    'classification': 'field-name-language-classification-link',
    'dialects': 'field-name-field-dialects',
    'typology': 'field-name-field-typology',
    'language_use': 'field-name-field-language-use',
    'language_development': 'field-name-field-language-development',
    'language_resource': 'field-name-language-resources-link',
    'writing': 'field-name-field-writing',
    'other_comments': 'field-name-field-comments',
}


class Parser:
    @staticmethod
    def save_lang_list_json() -> None:
        """
        Parse list of languages and save language names and links for detail in the next format:
            {
                a: [(lang, link), (lang, link), ...],
                b: [(lang, link), (lang, link), ...],
                ...
            }
        """

        result = {}
        for letter in LANG_LETTERS:
            response = requests.get(url=f'{HOST}/browse/names/{letter}', headers={'cookie': config.COOKIE})
            result[letter] = []
            soup = BeautifulSoup(response.content, 'html.parser')
            print(letter)
            for tag_a in soup.findAll('a'):
                if '/language/' in str(tag_a):
                    result[letter].append((tag_a.text, tag_a['href']))

        with open(f'{RES_PATH}/lang_list.json', "w", encoding="utf-8") as file:
            json.dump(result, file)

    @staticmethod
    def save_iso_list_json() -> None:
        """
        Parse list of iso's and save them in the next format
        {
            a: [iso1, iso2, iso3, ...],
            b: [iso1, iso2, iso3, ...],
            ....
        }
        """
        result = {}
        for letter in ISO_LETTERS:
            response = requests.get(url=f'{HOST}/browse/codes/{letter}', headers={'cookie': config.COOKIE})
            result[letter] = []
            soup = BeautifulSoup(response.content, 'html.parser')
            print(letter)
            for tag_a in soup.findAll('a'):
                if '/language/' in str(tag_a):
                    result[letter].append(tag_a.text)

        with open(f'{RES_PATH}/iso_list.json', "w", encoding="utf-8") as file:
            json.dump(result, file)

    @staticmethod
    def parse_lang_detail(language_name: str, link: str) -> dict:
        response = requests.get(url=HOST + link, headers={'cookie': config.COOKIE})
        soup = BeautifulSoup(response.content, 'html.parser')
        lang_detail = {
            'language_name': language_name,
            'language_of': LangDetailParser.language_of(soup),
            'iso': LangDetailParser.iso(soup),
            'alternate_names': LangDetailParser.alternate_names(soup),
            'autonym': LangDetailParser.autonym(soup),
            'user_population': LangDetailParser.user_population(soup),
            'location': LangDetailParser.location(soup),
            'language_maps': LangDetailParser.language_maps(soup),
            'language_status': LangDetailParser.language_status(soup),
            'classification': LangDetailParser.classification(soup),
            'dialects': LangDetailParser.dialects(soup),
            'typology': LangDetailParser.typology(soup),
            'language_use': LangDetailParser.language_use(soup),
            'language_development': LangDetailParser.language_development(soup),
            'language_resource': LangDetailParser.language_resource(soup),
            'writing': LangDetailParser.writing(soup),
            'other_comments': LangDetailParser.other_comments(soup),
        }
        # Parser.save_html_for_test(response.text)
        return lang_detail


    @staticmethod
    def save_html_for_test(response: str):
        with open(f'{RES_PATH}/test.html', 'w', encoding='utf-8') as file:
            file.write(response)


class LangDetailParser:
    @staticmethod
    def language_of(soup: BeautifulSoup) -> str:
        try:
            return soup.find('div', {'class': CLASSES_FOR_PARSE['language_of']}).h2.a.text
            # tag_h2.a['href'] = HOST + tag_h2.a['href']
            # return "".join([str(tag) for tag in tag_h2])
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def iso(soup: BeautifulSoup) -> str:
        try:
            return soup.find('div', {'class': CLASSES_FOR_PARSE['iso_6393']}).a.text
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def alternate_names(soup: BeautifulSoup) -> str:
        try:
            return soup.find('div', {'class': CLASSES_FOR_PARSE['alternate_names']})\
                       .find('div', {'class': 'even'})\
                       .text
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def autonym(soup: BeautifulSoup) -> str:
        try:
            return soup.find('div', {'class': CLASSES_FOR_PARSE['autonym']})\
                       .find('div', {'class': 'even'})\
                       .text\
                       .strip()
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def user_population(soup: BeautifulSoup) -> str:
        try:
            tag_p = soup.find('div', {'class': CLASSES_FOR_PARSE['user_population']})\
                        .find('div', {'class': 'even'})\
                        .find('p')
            return ''.join([str(tag) for tag in tag_p.contents])
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def location(soup: BeautifulSoup) -> str:
        try:
            return soup.find('div', {'class': CLASSES_FOR_PARSE['location']})\
                       .find('div', {'class': 'even'})\
                       .text\
                       .strip()
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def language_maps(soup: BeautifulSoup) -> str:
        try:
            tags_a = soup.find('div', {'class': CLASSES_FOR_PARSE['language_maps']})\
                         .find_all('a')
            for tag_a in tags_a:
                tag_a['href'] = HOST + tag_a['href']
            return "\n".join([str(tag_a) for tag_a in tags_a])
        except (AttributeError, TypeError) as e:
            return ''

    @staticmethod
    def language_status(soup: BeautifulSoup) -> str:
        try:
            return soup.find('div', {'class': CLASSES_FOR_PARSE['language_status']})\
                       .find('div', {'class': 'even'})\
                       .text\
                       .strip()
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def classification(soup: BeautifulSoup) -> str:
        try:
            tag_a = soup.find('div', {'class': CLASSES_FOR_PARSE['classification']}).a
            tag_a['href'] = HOST + tag_a['href']
            return str(tag_a)
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def dialects(soup: BeautifulSoup) -> str:
        try:
            tag_p = soup.find('div', {'class': CLASSES_FOR_PARSE['dialects']})\
                        .find('div', {'class': 'even'})\
                        .find('p')
            return ''.join([str(tag) for tag in tag_p.contents])
        except (AttributeError, TypeError):
            return ''


    @staticmethod
    def typology(soup: BeautifulSoup) -> str:
        try:
            return soup.find('div', {'class': CLASSES_FOR_PARSE['typology']})\
                       .find('p')\
                       .text
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def language_use(soup: BeautifulSoup) -> str:
        try:
            tag_p = soup.find('div', {'class': CLASSES_FOR_PARSE['language_use']})\
                        .find('div', {'class': 'even'})\
                        .find('p')
            return ''.join([str(tag) for tag in tag_p.contents])
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def language_development(soup: BeautifulSoup) -> str:
        try:
            tag_p = soup.find('div', {'class': CLASSES_FOR_PARSE['language_development']})\
                        .find('div', {'class': 'even'})\
                        .find('p')
            return ''.join([str(tag) for tag in tag_p.contents])
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def language_resource(soup: BeautifulSoup) -> str:
        try:
            return str(soup.find('div', {'class': CLASSES_FOR_PARSE['language_resource']}).a)
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def writing(soup: BeautifulSoup) -> str:
        try:
            tag_p = soup.find('div', {'class': CLASSES_FOR_PARSE['writing']}) \
                .find('div', {'class': 'even'}) \
                .find('p')
            return ''.join([str(tag) for tag in tag_p.contents])
        except (AttributeError, TypeError):
            return ''

    @staticmethod
    def other_comments(soup: BeautifulSoup) -> str:
        try:
            tag_p = soup.find('div', {'class': CLASSES_FOR_PARSE['other_comments']}) \
                .find('div', {'class': 'even'}) \
                .find('p')
            return ''.join([str(tag) for tag in tag_p.contents])
        except (AttributeError, TypeError):
            return ''


def get_langs() -> dict:
    with open(f'{RES_PATH}/lang_list.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def get_iso() -> dict:
    with open(f'{RES_PATH}/iso_list.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def get_map_points() -> list:
    with open(f'{RES_PATH}/map_points.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        result = []
        for row in csv_reader:
            if row[2] not in {'wrd', 'lno', 'aga', 'wya', 'lak', 'snb', 'pii', 'smd', 'cug', 'ajt', 'uun'}:
                result.append(
                    {
                        "iso": row[2],
                        "north": row[3],
                        "south": row[4],
                        "east": row[5],
                        "west": row[6],
                    }
                )
        return result[1:]


if __name__ == '__main__':
    print(Parser.parse_lang_detail('asdf', '/language/eng'))
