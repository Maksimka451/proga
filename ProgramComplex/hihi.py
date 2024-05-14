import pickle
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request



# Загрузка модели из файла
def load_model(model_file):
    with open(model_file, 'rb') as file:
        model = pickle.load(file)
    return model

# Предсказание класса для данных из файла CSV
def predict_traffic(model, csv_file):
    data = pd.read_csv(csv_file)
    all_frs = data[data.columns.difference(['Label', 'Original_label', 'Timestamp'])]
    X_scaled = preprocessing.scale(all_frs)
    label = data.Label
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, label, test_size=0.3)
    predictions = model.predict(X_test)
    return predictions[:20]

# Создание экземпляра FastAPI
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загрузка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Загрузка обученной модели
model_file = "bagging.pkl"  # Укажите путь к файлу с обученной моделью
model = load_model(model_file)

# Определение маршрута для отображения веб-интерфейса
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Определение маршрута для обработки загрузки файла и предсказания
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Чтение данных из файла CSV и предсказание с использованием модели
    predictions = predict_traffic(model, file.file)
    return {"predictions": predictions.toList()}  # Преобразование массива в список


# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
