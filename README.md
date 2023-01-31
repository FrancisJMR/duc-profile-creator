# DUC Profile Creator App
A Streamlit app that lets users create a Digital Use Conditions (DUC) profile JSON file.

For more information about DUC please visit: https://github.com/Digital-Use-Conditions/

## Demo

A demo of the app is available here: https://duc-profile-creator.azurewebsites.net/ (please wait several minutes for this free web service to boot)

## Development
On local host:
> docker build -t duc-streamlit:latest .

> docker run -p 8501:8501 duc-streamlit:latest


## Deploy on Azure via CLI
Guide: https://towardsdatascience.com/deploying-a-streamlit-web-app-with-azure-app-service-1f09a2159743

### Create Azure Registry and App Service Plan
1. Create Azure Contrainer Registry (ACR)
> az acr create --name MyContainerRegistry --resource-group Data-Analytics-Resource-Group --sku basic --admin-enabled true

2. Create Azure App Service Plan
> az appservice plan create -g Data-Analytics-Resource-Group -n MyAppServicePlan -l canadacentral --is-linux --sku F1


### Build container image on registry and deploy app on service plan
1. Build container image on registry
> az acr build --registry MyContainerRegistry --image duc-streamlit .

2. Deploy to Azure Service Apps

> az webapp create -p MyAppServicePlan -g Data-Analytics-Resource-Group -n duc-streamlit -i MyContainerRegistry.azurecr.io/duc-streamlit:latest
