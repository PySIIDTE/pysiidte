#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
from __future__ import print_function
import base64
import hashlib
import logging
from datetime import datetime

import cchardet
import pytz
from bs4 import BeautifulSoup as bs
from lxml import etree
from signxml import XMLSigner, methods
from suds.client import Client


"""
Módulo auxiliares y para realizar conexión, firma y servicios
relacionados don Documentos Tributarios Electrónicos del SII
(Servicio de Impuestos Internos) de Chile
"""
__author__ = "Daniel Blanco Martín (daniel@blancomartin.cl)"
__copyright__ = "Copyright (C) 2015-2017 Blanco Martín y Asoc. EIRL - BMyA S.A."
__license__ = "AGPL 3.0"


_logger = logging.getLogger(__name__)
retries = 1000
ssl._create_default_https_context = ssl._create_unverified_context

server_url = {
    'SIIHOMO': 'https://maullin.sii.cl/DTEWS/',
    'SII': 'https://palena.sii.cl/DTEWS/', }
BC = '''-----BEGIN CERTIFICATE-----\n'''
EC = '''\n-----END CERTIFICATE-----\n'''

clean1 = ' xmlns:SII="http://www.sii.cl/XMLSchema"'
clean2 = '<?xml version="1.0" encoding="UTF-8"?>'
clean3 = ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'

normalize_tags = collections.OrderedDict()
normalize_tags['RutEmisor'] = [10]
normalize_tags['RznSoc'] = [100]
normalize_tags['GiroEmis'] = [80]
normalize_tags['Telefono'] = [20]
normalize_tags['CorreoEmisor'] = [80, u'variable correo del emisor']
normalize_tags['Actecos'] = collections.OrderedDict()
normalize_tags['Actecos']['Acteco'] = [6]
normalize_tags['CdgTraslado'] = [1]
normalize_tags['FolioAut'] = [5]
normalize_tags['FchAut'] = [10]
normalize_tags['Sucursal'] = [20]
normalize_tags['CdgSIISucur'] = [9]
normalize_tags['CodAdicSucur'] = [20]
normalize_tags['DirOrigen'] = [60, u'dirección de la compañía']
normalize_tags['CmnaOrigen'] = [20, u'comuna de la compañía']
normalize_tags['CiudadOrigen'] = [20, u'ciudad de la compañía']
normalize_tags['CdgVendedor'] = [60]
normalize_tags['IdAdicEmisor'] = [20]
normalize_tags['IdAdicEmisor'] = [20]
normalize_tags['RUTRecep'] = [10, u'RUT del receptor']
normalize_tags['CdgIntRecep'] = [20]
normalize_tags['RznSocRecep'] = [100, u'Razón social o nombre receptor']
normalize_tags['NumId'] = [20]
normalize_tags['Nacionalidad'] = [3]
normalize_tags['IdAdicRecep'] = [20]
normalize_tags['GiroRecep'] = [40, u'giro del receptor']
normalize_tags['Contacto'] = [80]
normalize_tags['CorreoRecep'] = [80, u'variable correo del receptor']
normalize_tags['DirRecep'] = [70, u'dirección del receptor']
normalize_tags['CmnaRecep'] = [20, u'comuna del receptor']
normalize_tags['CiudadRecep'] = [20, u'ciudad del receptor']
normalize_tags['DirPostal'] = [70]
normalize_tags['CmnaPostal'] = [20]
normalize_tags['CiudadPostal'] = [20]
normalize_tags['Patente'] = [8]
normalize_tags['RUTTrans'] = [10]
normalize_tags['RUTChofer'] = [10]
normalize_tags['NombreChofer'] = [30]
normalize_tags['DirDest'] = [70]
normalize_tags['CmnaDest'] = [20]
normalize_tags['CiudadDest'] = [20]
normalize_tags['CiudadDest'] = [20]
normalize_tags['MntNeto'] = [18]
normalize_tags['MntExe'] = [18]
normalize_tags['MntBase'] = [18]
normalize_tags['MntMargenCom'] = [18]
normalize_tags['TasaIVA'] = [5]
normalize_tags['IVA'] = [18]
normalize_tags['IVAProp'] = [18]
normalize_tags['IVATerc'] = [18]
normalize_tags['TipoImp'] = [3]
normalize_tags['TasaImp'] = [5]
normalize_tags['MontoImp'] = [18]
normalize_tags['IVANoRet'] = [18]
normalize_tags['CredEC'] = [18]
normalize_tags['GmtDep'] = [18]
normalize_tags['ValComNeto'] = [18]
normalize_tags['ValComExe'] = [18]
normalize_tags['ValComIVA'] = [18]
normalize_tags['MntTotal'] = [18]
normalize_tags['MontoNF'] = [18]
normalize_tags['MontoPeriodo'] = [18]
normalize_tags['SaldoAnterior'] = [18]
normalize_tags['VlrPagar'] = [18]
normalize_tags['TpoMoneda'] = [15]
normalize_tags['TpoCambio'] = [10]
normalize_tags['MntNetoOtrMnda'] = [18]
normalize_tags['MntExeOtrMnda'] = [18]
normalize_tags['MntFaeCarneOtrMnda'] = [18]
normalize_tags['MntMargComOtrMnda'] = [18]
normalize_tags['IVAOtrMnda'] = [18]
# pluralizado deliberadamente 'Detalles' en lugar de ImptoReten
# se usó 'Detalles' (plural) para diferenciar del tag real 'Detalle'
# el cual va aplicado a cada elemento de la lista o tabla.
# según el tipo de comunicación, se elimina el tag Detalles o se le quita el
# plural en la conversion a xml
normalize_tags['NroLinDet'] = [4]
# ojo qu este que sigue es tabla tambien
normalize_tags['TpoCodigo'] = [10]
normalize_tags['VlrCodigo'] = [35]
normalize_tags['TpoDocLiq'] = [3]
normalize_tags['IndExe'] = [3]
# todo: falta retenedor
normalize_tags['NmbItem'] = [80]
normalize_tags['DscItem'] = [1000]
normalize_tags['QtyRef'] = [18]
normalize_tags['UnmdRef'] = [4]
normalize_tags['PrcRef'] = [18]
normalize_tags['QtyItem'] = [18]
# todo: falta tabla subcantidad
normalize_tags['FchElabor'] = [10]
normalize_tags['FchVencim'] = [10]
normalize_tags['UnmdItem'] = [10]
normalize_tags['PrcItem'] = [18]
# todo: falta tabla OtrMnda
normalize_tags['DescuentoOct'] = [5]
normalize_tags['DescuentoMonto'] = [18]
# todo: falta tabla distrib dcto
# todo: falta tabla distrib recargo
# todo: falta tabla cod imp adicional y retenciones
normalize_tags['MontoItem'] = [18]
# todo: falta subtotales informativos
# ojo que estos descuentos podrían ser globales más de uno,
# pero la implementación soporta uno solo
normalize_tags['NroLinDR'] = [2]
normalize_tags['TpoMov'] = [1]
normalize_tags['GlosaDR'] = [45]
normalize_tags['TpoValor'] = [1]
normalize_tags['ValorDR'] = [18]
normalize_tags['ValorDROtrMnda'] = [18]
normalize_tags['IndExeDR'] = [1]
# pluralizado deliberadamente
normalize_tags['NroLinRef'] = [2]
normalize_tags['TpoDocRef'] = [3]
normalize_tags['IndGlobal'] = [3]
normalize_tags['FolioRef'] = [18]
normalize_tags['RUTOtr'] = [10]
normalize_tags['IdAdicOtr'] = [20]
normalize_tags['FchRef'] = [10]
normalize_tags['CodRef'] = [1]
normalize_tags['RazonRef'] = [1]
# todo: faltan comisiones y otros cargos
pluralizeds = [
    'Actecos', 'Detalles', 'Referencias', 'DscRcgGlobals', 'ImptoRetens']
stamp = """<TED version="1.0"><DD><RE/><TD/><F/>\
<FE/><RR/><RSR/><MNT/><IT1/><CAF version="1.0"><DA><RE/><RS/>\
<TD/><RNG><D/><H/></RNG><FA/><RSAPK><M/><E/></RSAPK>\
<IDK/></DA><FRMA algoritmo="SHA1withRSA"/></CAF><TSTED/></DD>\
<FRMT algoritmo="SHA1withRSA"/></TED>"""
connection_status = {
    '0': 'Upload OK',
    '1': 'El remitente no tiene permiso para enviar',
    '2': 'Error en tamaño del archivo (muy grande o muy chico)',
    '3': 'Archivo cortado (tamaño <> al parámetro size)',
    '5': 'No está autenticado',
    '6': 'Empresa no autorizada a enviar archivos',
    '7': 'Esquema Invalido',
    '8': 'Firma del Documento',
    '9': 'Sistema Bloqueado',
    'Otro': 'Error Interno.', }
xsdpath = os.path.dirname(os.path.realpath(__file__))+'/xsd/'


def set_headers(token, referer):
    headers = {
        'Accept': 'image/gif, image/x-xbitmap, image/jpeg, \
image/pjpeg, application/vnd.ms-powerpoint, application/ms-excel, \
application/msword, */*',
        'Accept-Language': 'es-cl',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; PROG 1.0; Windows NT 5.0; \
YComp 5.0.2.4)',
        'Referer': '{}'.format(referer),
        'Connection': 'Keep-Alive',
        'Cache-Control': 'no-cache',
        'Cookie': 'TOKEN={}'.format(token), }
    return headers


def time_stamp(format='%Y-%m-%dT%H:%M:%S'):
    tz = pytz.timezone('America/Santiago')
    return datetime.now(tz).strftime(format)


def xml_validator(some_xml_string, validacion='doc'):
    """
    Funcion para validar los xml generados contra el esquema que le
    corresponda segun el tipo de documento.
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2016-06-01. Se agregó validación para boletas
    Modificada por Daniel Santibañez 2016-08-01
    """
    if validacion == 'bol':
        return True
    validacion_type = {
        'doc': 'DTE_v10.xsd',
        'env': 'EnvioDTE_v10.xsd',
        'env_boleta': 'EnvioBOLETA_v11.xsd',
        'recep': 'Recibos_v10.xsd',
        'env_recep': 'EnvioRecibos_v10.xsd',
        'env_resp': 'RespuestaEnvioDTE_v10.xsd',
        'sig': 'xmldsignature_v10.xsd',
        'book': 'LibroCV_v10.xsd', }
    xsd_file = xsdpath + validacion_type[validacion]
    try:
        xmlschema_doc = etree.parse(xsd_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        xml_doc = etree.fromstring(some_xml_string)
        result = xmlschema.validate(xml_doc)
        if not result:
            xmlschema.assert_(xml_doc)
        return {'result': 'OK', 'msg': result}
    except AssertionError as e:
        _logger.info(etree.tostring(xml_doc))
        return {'result': e.args, 'msg': validacion}


def convert_encoding(data, new_coding='UTF-8'):
    """
    Funcion auxiliar para conversion de codificacion de strings
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2014-12-01 - actualizada 2017-08-20
    """
    try:
        encoding = cchardet.detect(data)['encoding']
        _logger.info('Encoding:')
        _logger.info(encoding)
    except:
        encoding = 'ascii'
    if new_coding.upper() != encoding.upper():
        try:
            data = data.decode(encoding=encoding, errors='ignore')
        except:
            try:
                data = data.decode(encoding='UTF-8', errors='ignore')
            except:
                try:
                    data = data.decode(
                        encoding='ISO-8859-9', errors='replace')
                except:
                    pass
        data = data.encode(encoding=new_coding, errors='ignore')
    return data


def soup_text(xml, type_tag):
    """
    :param xml: xml obtenido
    :param type: TOKEN o SEMILLA
    :return:
    """
    try:
        soup = bs(xml, 'xml')
        tag = soup.find(type_tag).text
        return tag
    except:
        _logger.info(u'Error de conexión al servidor')
        raise ValueError(u'''Hay un problema de conectividad al servidor \
del SII. Por favor, intente conectarse en unos minutos.
(No se pudo obtener el %s)''' % type_tag)


def char_replace(text):
    """
    Funcion para reemplazar caracteres especiales
    Esta funcion sirve para salvar bug en libreDTE con los recortes de
    giros que están codificados en utf8 (cuando trunca, trunca la
    codificacion)
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2016-07-31
    """
    special_chars = [
        [u'á', 'a'],
        [u'é', 'e'],
        [u'í', 'i'],
        [u'ó', 'o'],
        [u'ú', 'u'],
        [u'ñ', 'n'],
        [u'Á', 'A'],
        [u'É', 'E'],
        [u'Í', 'I'],
        [u'Ó', 'O'],
        [u'Ú', 'U'],
        [u'Ñ', 'N']]
    for char in special_chars:
        try:
            text = text.replace(char[0], char[1])
        except:
            pass
    return text


def digest(data):
    """
    Funcion para obtener digest en la firma
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2015-03-01
    """
    sha1 = hashlib.new('sha1', data)
    return sha1.digest()


def search_digest(xml, tag):
    """
    Busca el digest de un xml (primero que encuentra?)
    :param xml:
    :param tag:
    :return:
    """
    pass


def get_tag_digest(xml, coding='iso-8859-1'):
    """
    Función para obtener el digest del tag EnvioDTE
    :param xml: el documento a extraer el tag
    :param tag: nro de tag (en el documento)
    :param coding: codificacion (default iso-8859-1)
    :return: digest remoto del documento
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2017-08-07
    """
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding=coding)
    root = etree.fromstring(xml, parser=parser)
    if root.tag == '{http://www.sii.cl/SiiDte}EnvioDTE':
        setdte = etree.tostring(root[0])
        xmlm = etree.tostring(etree.fromstring(setdte), method='c14n')
    elif root.tag == '{http://www.sii.cl/SiiDte}DTE':
        doc = etree.tostring(
            root.find("{http://www.sii.cl/SiiDte}Documento"))
        xmlm = etree.tostring(
            etree.fromstring(doc), method="c14n").replace(clean3, '')
    return base64.b64encode(digest(xmlm))


def check_digest(xml):
    """
    Funcion para comparar los digest
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2017-08-07
    :param xml:
    :return:
    """
    rdig = str(bs(xml, 'xml').find_all('DigestValue')[-1].text)
    _logger.info('Remote Digest: {}'.format(rdig))
    ldig = get_tag_digest(xml)
    _logger.info('Local Digest: {}'.format(ldig))
    return rdig == ldig


def sign_rsa(self, MESSAGE, KEY, digst=''):
    """
    Decorador para firmar RSA
    :return:
    """
    def real_signer(method):
        def call(*args, **kwargs):
            rsa = M2Crypto.EVP.load_key_string(KEY)
            rsa.reset_context(md='sha1')
            rsa_m = rsa.get_rsa()
            rsa.sign_init()
            rsa.sign_update(MESSAGE)
            FRMT = base64.b64encode(rsa.sign_final())
            if digst == '':
                return {
                    'firma': FRMT, 'modulus': base64.b64encode(rsa_m.n),
                    'exponent': base64.b64eDigesncode(rsa_m.e), }
            else:
                return {
                    'firma': FRMT, 'modulus': base64.b64encode(rsa_m.n),
                    'exponent': base64.b64encode(rsa_m.e),
                    'digest': base64.b64encode(self.digest(MESSAGE)), }
        return call
    return real_signer


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


def get_token(seed, mode):
    """
    Funcion usada en autenticacion en SII
    Obtencion del token a partir del envio de la semilla firmada
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2017-05-10
    """
    url = server_url[mode] + 'GetTokenFromSeed.jws?WSDL'
    client = Client(url)
    tree = etree.fromstring(seed)
    ss = etree.tostring(tree, pretty_print=True, encoding='iso-8859-1')
    aa, i = None, retries
    while aa is None and i > 0:
        _logger.info('getToken: Intento {}'.format(retries + 1 - i))
        try:
            aa = client.service.getToken(ss)
        except:
            continue
        finally:
            i -= 1
    return soup_text(aa, 'TOKEN')


@sign_rsa()
def signrsa(self, MESSAGE, KEY, digst=''):
    """
    Funcion usada en SII
    para firma del timbre (dio errores de firma para el resto de los doc)
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2015-03-01
    """
    return KEY.encode('ascii')


@sign_rsa()
def signmessage(self, MESSAGE, KEY, pubk='', digst=''):
    """
    Funcion usada en SII
    para firma del timbre (dio errores de firma para el resto de los doc)
     @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
     @version: 2015-03-01
    """
    return KEY


def sii_token(mode, privkey, cert):
    @sign_seed(privkey, cert)
    @create_template_seed
    def get_seed(mode):
        """
        Funcion usada en autenticacion en SII, obtención de la semilla
        se discontinúa el método usado con SOAPPy por poco eficiente y
        con existencia de muchos errores (2015-04-01)
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2017-05-10
        """
        url = server_url[mode] + 'CrSeed.jws?WSDL'
        seed_xml, i = None, retries
        client = Client(url)
        while seed_xml is None and i > 0:
            _logger.info('getSeed: Intento {}'.format(retries + 1 - i))
            try:
                seed_xml = client.service.getSeed()
            except:
                continue
            finally:
                i -= 1
        return soup_text(seed_xml, 'SEMILLA')
    return get_token(get_seed(mode), mode)


def split_cert(cert):
    certf, j = '', 0
    for i in range(0, 29):
        certf += cert[76 * i:76 * (i + 1)] + '\n'
    return certf


#def sign_seed(message, privkey, cert):
#    """
#    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
#    @version: 2016-06-01
#    """
#    _logger.info('SIGNING WITH SIGN_SEED ##### ------ #####')
#    doc = etree.fromstring(message)
#    # signed_node = Signer.sign(
#    #    doc, key=privkey.encode('ascii'), cert=cert, key_info=None)
#    signed_node = XMLSigner(
#        method=methods.enveloped, signature_algorithm=u'rsa-sha1',
#        digest_algorithm=u'sha1').sign(
#        doc, key=privkey.encode('ascii'), passphrase=None, cert=cert,
#        key_name=None, key_info=None, id_attribute=None)
#    msg = etree.tostring(
#        signed_node, pretty_print=True).replace('ds:', '')
#    _logger.info('message: {}'.format(msg))
#    return msg


def pdf417bc(ted):
    """
    Funcion creacion de imagen pdf417 basada en biblioteca elaphe
     @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
     @version: 2016-05-01
    """
    bc = barcode(
        'pdf417',
        ted,
        options=dict(
            compact=False,
            eclevel=5,
            columns=13,
            rowmult=2,
            rows=3
        ),
        margin=20,
        scale=1
    )
    return bc


def analyze_sii_result(sii_result, sii_message, sii_receipt):
    _logger.info('pysiidte.analyze_sii_result. sii_result: %s' % sii_result)
    _logger.info('pysiidte.analyze_sii_result. sii_receipt: %s' % sii_receipt)
    result_dict = {
        'Proceso': ['SOK', 'CRT', 'PDR', 'FOK', '-11'],
        'Rechazado': ['RCH', 'RFR', 'RSC', 'RCT'],
        'Reparo': ['RLV'],
        'check_receipt': ['EPR', 'DNK'],
        'check_glosa': ['2'], }
    status = False
    try:
        soup_message = bs(sii_message, 'xml')
        _logger.info(soup_message)
        for key, values in result_dict.iteritems():
            if soup_message.ESTADO.text in values:
                status = key
                break
        if status == 'check_receipt':
            if True:
                soup_receipt = bs(sii_receipt, 'xml')
                _logger.info(soup_receipt)
                if soup_receipt.ACEPTADOS.text == soup_receipt.INFORMADOS.text:
                    return 'Aceptado'
                if soup_receipt.REPAROS.text >= '1':
                    return 'Reparo'
                if soup_receipt.RECHAZADOS.text >= '1':
                    return 'Rechazado'
            else:  # except:
                pass
        elif status == 'check_glosa':
            raise ValueError(
                'Error code: 2: {}'.format(soup_message.GLOSA_ERR.text))
        return sii_result
    except TypeError:
        _logger.info(
            'pysiidte.analyze_sii_result: \
            sii_message Retornando Valor Original')
        return sii_result


def remove_plurals_xml(xml):
    for k in pluralizeds:
        print(k)
        xml = xml.replace('<%s>' % k, '').replace('</%s>' % k, '')
    return xml


def create_template_doc(doc):
    """
    Creacion de plantilla xml para envolver el DTE
    Previo a realizar su firma (1)
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2016-06-01
    """
    xml = '''<DTE xmlns="http://www.sii.cl/SiiDte" version="1.0">
    {}</DTE>'''.format(doc)
    return xml


tag_replace01 = ['TotOpExe', 'TotOpIVARec', 'CodIVANoRec',
                 'TotOpIVARetTotal', 'TotIVARetTotal',
                 'TotOpIVARetParcial', 'TotIVARetParcial',
                 'TotOpIVANoRetenido', 'TotIVANoRetenido',
                 'TotOpIVANoRec', 'TotMntIVANoRec',
                 'TotOpIVAUsoComun', 'TotCredIVAUsoComun',
                 'TotIVAUsoComun', 'TotImpSinCredito', 'CodImp', 'TotMntImp',
                 'TpoImp', 'TasaImp']
tag_replace_1 = ['TpoImp', 'TotOpIVARec', 'TotIVANoRec', 'TotOtrosImp']
tag_replace02 = ['CodIVANoRec', 'MntIVANoRec', 'IVANoRetenido', 'IVARetTotal',
                 'IVARetParcial', 'OtrosImp', 'CodImp', 'MntImp', 'TasaImp',
                 'TpoImp', 'uTasaImp', 'MntIVA']
tag_replace_2 = ['TpoDocRef', 'FolioDocRef', 'TpoImp', 'TasaImp',
                 'IVANoRec', 'OtrosImp']
tag_round = ['MntExe', 'MntNeto', 'MntIva', 'MntImp']
