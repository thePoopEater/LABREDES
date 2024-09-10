from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime

key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

with open("private_key.pem", "wb") as f:
    f.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "CL"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Arica"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Arica"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Elpp"),
    x509.NameAttribute(NameOID.COMMON_NAME, "dominio.elpp"),
])

certificado = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName("mywebsite.com")]),
    critical=False,
).sign(key, hashes.SHA256(), default_backend())

with open("certificate.pem", "wb") as f:
    f.write(certificado.public_bytes(serialization.Encoding.PEM))

print("Certificado y clave privada generados exitosamente.")
