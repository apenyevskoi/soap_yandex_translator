from suds.client import Client

hello_client = Client('http://127.0.0.1:8080?wsdl')
print(hello_client.service.Insoap("translate this text"))