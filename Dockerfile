FROM python:3.10
COPY /app /app
RUN pip install requests
EXPOSE 8000
CMD python app/weather-checker.py