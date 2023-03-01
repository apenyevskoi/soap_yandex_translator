import lxml
from spyne.protocol.soap import Soap11
from yandex.Translater import Translater
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne import Application, rpc, ServiceBase, Unicode

'''
веб-сервис, который будет служить нам переводчиком на английский язык. Наш веб-сервис будет получать запросы, 
обращаться в Yandex-translator, получать перевод и данный перевод отдавать клиенту. Принимаются входящие запросы 
в XML-формате. Ответ также будет уходить в XML-формате
'''
# curl -H "Content-Type: text/xml; charset=utf-8" -H 'SOAPAction:' --data-binary @F:\soap1.xml -X POST 127.0.0.1:8080?wsdl
#curl -X POST 127.0.0.1:8080?wsdl -H 'Content-Type: text/xml' -H 'SOAPAction: blz:getBank' -d '<soapenv:Envelope xmlns:soapenv=«schemas.xmlsoap.org/soap/envelope» xmlns:tran=«Translator»><soapenv:Header/><soapenv:Body><tran:Insoap><tran:words>Тестируем наше приложение</tran:words></tran:Insoap></soapenv:Body></soapenv:Envelope>'
#curl -H "Content-Type: text/xml; charset=utf-8" --data @F:\soap1.xml -X POST 127.0.0.1:8080?wsdl
class Soap(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def Insoap(ctx, text):
        print(lxml.etree.tostring(ctx.in_document))
        # return "Response from Server"
        return translate(text, 'ru')


def translate(tx, lang):
    print('here_translater')
    tr = Translater()
    tr.set_from_lang('en')
    tr.set_to_lang('ru')
    tr.set_iamtoken('t1.9euelZqUyJHJmo6JjpCbz5OdmpaMle3rnpWamZSQj46UkZOWxpCTxonHms_l8_cWRARg-e9DdF97_N3z91ZyAWD570N0X3v8.pC_p5YL6L8aiOUPh70ZIubZLAHGAwIC7UCrOSM9Q4W0A79GhrU73FtnlpqRhGfK1j5sN_C68-sT-VSnusTB-Cg')
    tr.set_folderid('')
    tr.set_target_language(lang)
    tr.set_text(tx)
    return tr.translate()

app = Application([Soap], tns='ya_Translator', in_protocol=Soap11(), out_protocol=Soap11())
application = WsgiApplication(app)

if __name__ == '__main__':
    #print(translate('test text to acquire', 'ru' ))
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8080, application)
    server.serve_forever()
