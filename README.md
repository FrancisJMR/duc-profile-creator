# DUC Profile Creator App
A Streamlit app that lets users create a Digital User Conditions (DUC) profile JSON file.

For more information about DUC please visit: https://github.com/Digital-Use-Conditions/

## Development
On local host:
> docker build -t duc-streamlit-app:latest .

> docker run -p 8501:8501 duc-streamlit-app:latest


## Deploy on Azure via CLI
Guide: https://towardsdatascience.com/deploying-a-streamlit-web-app-with-azure-app-service-1f09a2159743

Create Azure Contrainer Registry (ACR)
> az acr create --name MyAppRegistry --resource-group My-Apps-Resource-Group --sku basic --admin-enabled true

Build container image on ACR
> az acr build --registry MyAppRegistry --image duc-profile-creator-app .

Create Azure App Service Plan
> az appservice plan create -g My-Apps-Resource-Group -n MyAppServicePlan -l canadacentral --is-linux --sku F1

Deploy to Azure App Service
> az webapp create -p MyAppServicePlan -n duc-profile-creator-app duc-profile-creator-app:latest
