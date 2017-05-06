#!/home/daniel/odoo-ve/bin/python
# -*- coding: utf-8 -*-
##############################################################################
# Nuevo pysiidte probando a llevarme todas las funciones esenciales          #
# 2017-05-06                                                                 #
##############################################################################
import ssl
from SOAPpy import SOAPProxy
from lxml import etree
from signxml import XMLSigner, XMLVerifier, methods
import logging

_logger = logging.getLogger(__name__)

ssl._create_default_https_context = ssl._create_unverified_context

server_url = {
    'SIIHOMO': 'https://maullin.sii.cl/DTEWS/',
    'SII': 'https://palena.sii.cl/DTEWS/', }
BC = '''-----BEGIN CERTIFICATE-----\n'''
EC = '''\n-----END CERTIFICATE-----\n'''


def sign_seed(privkey, cert):
    """
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2016-06-01
    """
    def real_signer(method):
        def call(*args, **kwargs):
            doc = etree.fromstring(method(*args, **kwargs))
            signed_node = XMLSigner(
                method=methods.enveloped, signature_algorithm=u'rsa-sha1',
                digest_algorithm=u'sha1').sign(
                doc, key=privkey.encode('ascii'), passphrase=None, cert=cert,
                key_name=None, key_info=None, id_attribute=None)
            msg = etree.tostring(
                signed_node, pretty_print=True).replace('ds:', '')
            _logger.info('message: {}'.format(msg))
            return msg
        return call
    return real_signer


def create_template_seed(method):
    """
    Funcion usada en autenticacion en SII
    Creacion de plantilla xml para realizar el envio del token
    Previo a realizar su firma
     @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
     @version: 2016-06-01
    """
    def call(mode):
        xml = u'''<getToken>
<item>
<Semilla>{}</Semilla>
</item>
</getToken>
'''.format(method(mode))
        return xml
    return call


# @sign_seed(privkey, cert)
# @create_template_seed
# def get_seed(mode):
#     """
#     Funcion usada en autenticacion en SII
#     Obtencion de la semilla desde el SII.
#     Basada en función de ejemplo mostrada en el sitio edreams.cl
#      @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
#      @version: 2015-04-01
#     """
#     url = server_url[mode] + 'CrSeed.jws?WSDL'
#     ns = 'urn:' + server_url[mode] + 'CrSeed.jws'
#     _server = SOAPProxy(url, ns)
#     root = etree.fromstring(_server.getSeed())
#     seed = root[0][0].text
#     return seed
