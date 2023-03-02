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
#SoapUI
#http://localhost:8080?wsdl
class Soap(ServiceBase):
    @rpc(str, str, _returns=Unicode)
    def Insoap(ctx, text, lang):
        print(lxml.etree.tostring(ctx.in_document))
        # return "Response from Server"
        return translate(text, lang)

def translate(tx, lang):
    tr = Translater()
    tr.set_key('')
    tr.set_from_lang('en')
    tr.set_to_lang('ru')
    tr.set_iamtoken('')
    tr.set_folderid('')
    tr.set_target_language(lang)
    tr.set_text(tx)
    return tr.translate()

app = Application([Soap], tns='ya_Translator', in_protocol=Soap11(), out_protocol=Soap11())
application = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8080, application)
    server.serve_forever()