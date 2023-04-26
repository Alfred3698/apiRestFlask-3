FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
