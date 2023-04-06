FROM python:3.8-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENV FLASK_ENV=devlopment
ENV DATABASE_URI=postgresql://postgres:postgres@172.17.0.2/employee_management
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]