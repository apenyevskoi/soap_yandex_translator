from suds.client import Client

yaTranslClient = Client('http://127.0.0.1:8080?wsdl')
print(yaTranslClient.service.Insoap("translate this text", 'fr'))