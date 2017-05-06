#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# Nuevo pysiidte probando a llevarme todas las funciones esenciales          #
# 2017-05-06                                                                 #
##############################################################################
import ssl
from lxml import etree
from signxml import XMLSigner, XMLVerifier, methods
import logging
import collections

_logger = logging.getLogger(__name__)

ssl._create_default_https_context = ssl._create_unverified_context

server_url = {
    'SIIHOMO': 'https://maullin.sii.cl/DTEWS/',
    'SII': 'https://palena.sii.cl/DTEWS/', }
BC = '''-----BEGIN CERTIFICATE-----\n'''
EC = '''\n-----END CERTIFICATE-----\n'''


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
normalize_tags['GiroRecep'] = [40, u'variable con giro del receptor']
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
