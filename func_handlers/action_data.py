import json
from typing import List, Optional

import pyshorteners
from pathlib import *
from pydantic import BaseModel
from pydantic_core import core_schema


class DataJSON(BaseModel):
    long_url: str
    short_url: str


class DataURLS(BaseModel):
    urls: List[DataJSON] = []


def save_data(long_url: str) -> DataURLS:
    data_base = DataURLS()
    data = DataJSON(long_url=long_url, short_url=make_short_url(long_url))

    if get_path_db().stat().st_size == 0:
        with open(get_path_db(), 'w') as open_file:
            data_base.urls.append(data.__dict__)
            json.dump(data_base.__dict__, open_file, indent=4)
    else:
        with open(get_path_db(), 'r') as read_file:
            data_base.urls = [DataJSON(**elem).__dict__ for elem in json.load(read_file)['urls']]

            if data.__dict__ not in data_base.urls:
                data_base.urls.append(data.__dict__)

                with open(get_path_db(), 'w') as out_file:
                    json.dump(data_base.__dict__, out_file, indent=4)

    return data_base


def delete_data(url: str) -> DataURLS:
    data_base = DataURLS()

    if get_path_db().stat().st_size != 0:
        with open(get_path_db(), 'r') as open_file:
            data_base.urls = [DataJSON(**elem).__dict__ for elem in json.load(open_file)['urls']]

            filtered_value = [*filter(lambda elem: elem['short_url'] == url or elem['long_url'] == url, data_base.urls)]

            if filtered_value:
                data_base.urls.remove(*filtered_value)

            with open(get_path_db(), 'w') as out_file:
                json.dump(data_base.__dict__, out_file, indent=4)

    return data_base


def update_data(new_url: str, old_url: str) -> DataURLS:
    with open(get_path_db(), 'r') as open_file:
        data_base = DataURLS()
        data_base.urls = [DataJSON(**elem).__dict__ for elem in json.load(open_file)['urls']]

        filtered_value = [*filter(lambda elem: elem['long_url'] == old_url, data_base.urls)]

        if filtered_value:
            data_base.urls.remove(filtered_value[0])

            filtered_value[0]['long_url'] = new_url
            filtered_value[0]['short_url'] = make_short_url(new_url)

            data_base.urls.append(filtered_value[0])

        with open(get_path_db(), 'w') as out_file:
            json.dump(data_base.__dict__, out_file, indent=4)

    return data_base


def show_all_urls() -> DataURLS:
    data_base = DataURLS()

    with open(get_path_db(), 'r') as open_file:
        data_base.urls = [DataJSON(**elem).__dict__ for elem in json.load(open_file)['urls']]

    return data_base


def make_short_url(long_url: str) -> str:
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(long_url)
    return short_url


def get_path_db() -> Path:
    data_path = Path.cwd().joinpath('data').joinpath('data_base.json')
    return data_path
