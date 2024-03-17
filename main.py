from fastapi import FastAPI
from pydantic import BaseModel
from func_handlers.action_data import save_data, delete_data, update_data, make_short_url, show_all_urls

app = FastAPI()


class DataJSON(BaseModel):
    long_url: str
    short_url: str


@app.post('/make_short_url')
def make_short_url_handler(long_url: str):
    data = DataJSON

    data.long_url = long_url
    data.short_url = make_short_url(long_url)
    result = {'long_url': data.long_url, 'short_url': data.short_url}
    save_data(result)
    return result, 'Ссылка добавлена!'


@app.post('/delete_url')
def delete_url_handler(short_url: str, long_url: str) -> tuple:
    result = delete_data(short_url=short_url, long_url=long_url)
    return result


@app.put('/update_url')
def update_url_handler(new_url: str, old_url: str) -> tuple:
    result = update_data(new_url=new_url, old_url=old_url)
    return result


@app.get('/show_all_urls')
def show_all_urls_handler():
    result = show_all_urls()
    return result
