FROM python:3.7
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp credentials.toml ~/.streamlit/credentials.toml

EXPOSE 80
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
