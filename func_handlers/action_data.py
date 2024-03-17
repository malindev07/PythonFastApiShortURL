import json
import pyshorteners


def save_data(data_url: dict) -> str:
    with open('data/data_base.json', 'r') as open_file:
        data_base = json.load(open_file)
        if data_url in data_base['urls']:
            return ('Ccылка уже сущестсвует!')
        data_base['urls'].append(data_url)
        with open('data/data_base.json', 'w') as out_file:
            json.dump(data_base, out_file, indent=4)
            return 'Ссылка добавлена!'


def delete_data(short_url: str = '', long_url: str = ''):
    with open('data/data_base.json', 'r') as open_file:
        data_base = json.load(open_file)
        filtered_value = [
            *filter(lambda elem: elem['short_url'] == short_url or elem['long_url'] == long_url,
                    data_base['urls'])]

        if filtered_value:
            data_base['urls'].remove(filtered_value[0])
            with open('data/data_base.json', 'w') as out_file:
                json.dump(data_base, out_file, indent=4)
            return 'Ссылка удалена!', filtered_value[0]
        else:
            return 'Ссылка не найдена!', filtered_value


def update_data(new_url: str, old_url: str):
    with open('data/data_base.json', 'r') as open_file:
        data_base = json.load(open_file)

        if [*filter(lambda elem: elem['long_url'] == old_url, data_base['urls'])]:
            filtered_value = [*filter(lambda elem: elem['long_url'] == old_url, data_base['urls'])]

            data_base['urls'].remove(filtered_value[0])

            filtered_value[0]['long_url'] = new_url
            filtered_value[0]['short_url'] = make_short_url(new_url)

            data_base['urls'].append(filtered_value[0])

            with open('data/data_base.json', 'w') as out_file:
                json.dump(data_base, out_file, indent=4)
                return 'Ссылка обновлена!', filtered_value

        else:
            return 'Ссылка не найдена'


def show_all_urls():
    with open('data/data_base.json', 'r') as open_file:
        data_base = json.load(open_file)
        return data_base


def make_short_url(long_url: str) -> str:
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(long_url)
    return short_url
