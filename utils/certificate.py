# -*- coding: utf-8 -*-
"""
Certificate generation module.
"""

from OpenSSL import crypto
import time
import base64
from flask import url_for
from .crypt import Md5Utils
from rds import rds


class Certificate(object):
    ca = tuple()

    def __init__(self, ca_key, ca_cert):
        self.ca = self.get_ca_certificate(ca_key, ca_cert)

    @staticmethod
    def create_key_pair(key_type, bits):
        """
        Create a public/private key pair.
        Arguments: key_type - Key type, must be one of TYPE_RSA and TYPE_DSA
                   bits - Number of bits to use in the key
        Returns:   The public/private key pair in a PKey object
        """
        pkey = crypto.PKey()
        pkey.generate_key(key_type, bits)
        return pkey

    @staticmethod
    def create_cert_request(pkey, digest="sha1", **name):
        """
        Create a certificate request.
        Arguments: pkey   - The key to associate with the request
                   digest - Digestion method to use for signing, default is md5
                   **name - The name of the subject of the request, possible
                            arguments are:
                              C     - Country name
                              ST    - State or province name
                              L     - Locality name
                              O     - Organization name
                              OU    - Organizational unit name
                              CN    - Common name
                              emailAddress - E-mail address
        Returns:   The certificate request in an X509Req object
        """
        req = crypto.X509Req()
        subj = req.get_subject()

        for (key, value) in name.items():
            setattr(subj, key, value)

        req.set_pubkey(pkey)
        req.sign(pkey, digest)
        return req

    @classmethod
    def create_certificate(cls, req, (issuer_key, issuer_cert), serial, (not_before, not_after), digest="sha1",
                           extension_type=None):
        """
        Generate a certificate given a certificate request.
        Arguments: req        - Certificate reqeust to use
                   issuer_cert - The certificate of the issuer
                   issuer_key  - The private key of the issuer
                   serial     - Serial number for the certificate
                   notBefore  - Timestamp (relative to now) when the certificate
                                starts being valid
                   notAfter   - Timestamp (relative to now) when the certificate
                                stops being valid
                   digest     - Digest method to use for signing, default is sha1
                   extension_type - extension type
        Returns:   The signed certificate in an X509 object
        """
        cert = crypto.X509()

        cert.set_version(2)
        cert.set_serial_number(serial)
        cert.gmtime_adj_notBefore(not_before)
        cert.gmtime_adj_notAfter(not_after)
        cert.set_issuer(issuer_cert.get_subject())
        cert.set_subject(req.get_subject())
        cert.set_pubkey(req.get_pubkey())
        if extension_type == 'client':
            cert.add_extensions(cls.get_client_extensions(cert, issuer_cert))
        elif extension_type == 'server':
            cert.add_extensions(cls.get_server_extension(cert, issuer_cert))

        cert.sign(issuer_key, digest)
        return cert

    @staticmethod
    def get_client_extensions(client_cert, ca_cert):
        return [crypto.X509Extension('basicConstraints', False, 'CA:false'),
                crypto.X509Extension('subjectKeyIdentifier', False, 'hash', subject=client_cert),
                crypto.X509Extension('authorityKeyIdentifier', False, 'keyid:always', issuer=ca_cert),
                crypto.X509Extension('keyUsage', False, 'digitalSignature,keyEncipherment'),
                crypto.X509Extension('extendedKeyUsage', False, 'clientAuth'),
                crypto.X509Extension('crlDistributionPoints', False, 'URI:http://path.to.crl/myca.crl')]

    @staticmethod
    def get_server_extension(server_cert, ca_cert):
        return [crypto.X509Extension('basicConstraints', False, 'CA:false'),
                crypto.X509Extension('subjectKeyIdentifier', False, 'hash', subject=server_cert),
                crypto.X509Extension('authorityKeyIdentifier', False, 'keyid:always', issuer=ca_cert),
                crypto.X509Extension('keyUsage', False, 'digitalSignature,keyEncipherment'),
                crypto.X509Extension('subjectAltName', False, 'IP:127.0.0.1'),
                crypto.X509Extension('extendedKeyUsage', False, 'serverAuth'),
                crypto.X509Extension('crlDistributionPoints', False, 'URI:http://path.to.crl/myca.crl')]

    @staticmethod
    def get_ca_certificate(key, cer):

        with open(key, 'r') as k:
            t = k.read()
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, t)

        with open(cer, 'r') as c:
            t = c.read()
            ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, t)

        return ca_key, ca_cert

    @staticmethod
    def get_serial_id():
        key = 'certificate_id'
        return rds.incr(key)

    def create_client_certificate(self, client_id):
        """

        :param client_id:
        :type client_id: str
        :return:
        :rtype:
        """
        pkey = self.create_key_pair(crypto.TYPE_RSA, 2048)
        req = self.create_cert_request(pkey, C="CN", CN=str(client_id))

        cert = self.create_certificate(req, self.ca, self.get_serial_id(), (0, 60 * 60 * 24 * 365 * 1),
                                       extension_type="client")
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey), crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

    def create_server_certificate(self, cn="push server"):
        pkey = self.create_key_pair(crypto.TYPE_RSA, 2048)
        req = self.create_cert_request(pkey, C="CN", CN=cn)

        cert = self.create_certificate(req, self.ca, self.get_serial_id(), (0, 60 * 60 * 24 * 365 * 1),
                                       extension_type="server")
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey), crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

    @classmethod
    def create_ca_certificate(cls):
        ca_key = cls.create_key_pair(crypto.TYPE_RSA, 2048)
        ca_req = cls.create_cert_request(ca_key, O='New Game', OU='New Game Developer',
                                         CN='New Game Developer Authority',
                                         C='CN')
        ca_cert = cls.create_certificate(ca_req, (ca_req, ca_key), cls.get_serial_id(),
                                         (0, 60 * 60 * 24 * 365 * 10))  # ten years
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key), crypto.dump_certificate(crypto.FILETYPE_PEM,
                                                                                            ca_cert)

    @staticmethod
    def create_download_url(client_id, cer_type, secret):
        data = str(client_id) + "," + str(cer_type) + "," + str(int(time.time()))

        sign = Md5Utils.sign(data, str(secret))
        path = base64.b64encode(data + "," + sign)
        return url_for('.download',
                       path=path,
                       _external=True)

    @staticmethod
    def get_download_data(path):
        data = base64.b64decode(path)
        return data.split(',')