from datetime import datetime, timedelta,timezone

from cryptography import x509
from cryptography.hazmat._oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes


class CertificateAuthority:
    """
     The certificate authority implement layer of abstraction between cryptography lib and application
    """

    def sign(self):
        pass

    
    def convert_to_file(self):
        return self.cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')


    def create(self, key):
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Mato Grosso do Sul"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Mato Grosso do Sul"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"TI"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"My CA")
        ])
        self.cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.now(timezone.utc)
        ).not_valid_after(
            datetime.now(timezone.utc) + timedelta(days=3650)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).add_extension(
            x509.KeyUsage(digital_signature=True, key_encipherment=False, key_cert_sign=True, crl_sign=True,
                          content_commitment=False, data_encipherment=False, key_agreement=False,
                          encipher_only=False,
                          decipher_only=False), critical=True
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False
        ).sign(key, hashes.SHA256(), default_backend())

        return self.cert, serialization.Encoding.PEM