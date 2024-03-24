from fastapi import FastAPI

from func_handlers.action_data import (save_data, delete_data, update_data, show_all_urls, DataJSON, DataURLS)

app = FastAPI()


@app.post('/')
def make_short_url_handler(long_url: str) -> DataURLS:
    return save_data(long_url)


@app.delete('/')
def delete_url_handler(url: str) -> DataURLS:
    return delete_data(url=url)


@app.put('/')
def update_url_handler(new_url: str, old_url: str) -> DataURLS:
    return update_data(new_url=new_url, old_url=old_url)


@app.get('/')
def show_all_urls_handler() -> DataURLS:
    return show_all_urls()
