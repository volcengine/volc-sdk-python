import os
import base64
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)


def aes_gcm_encrypt_bytes(key, iv, plain_bytes, associated_data=b""):
    # aes_gcm_encrypt_bytes encrypt message using AES-GCM
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
    ).encryptor()
    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)
    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plain_bytes) + encryptor.finalize()
    return ciphertext + encryptor.tag


def aes_gcm_encrypt_base64_string(key, nonce, plaintext):
    """aes_gcm_encrypt_base64_string Encrypt message from base64 string to string using AES-GCM
    """
    plain_bytes = plaintext.encode()
    # Encrypt message to string using AES-GCM
    c = aes_gcm_encrypt_bytes(key, nonce, plain_bytes)
    return base64.b64encode(c).decode()


def aes_gcm_decrypt_bytes(key, iv, cipher_bytes, associated_data=b""):
    """aes_gcm_decrypt_bytes Decrypt message from bytes to bytes using AES-GCM
    """
    tag_length = 16  # default aes gcm tag length
    cipher = cipher_bytes[:-tag_length]
    tag = cipher_bytes[-tag_length:]
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
    ).decryptor()
    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)
    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(cipher) + decryptor.finalize()


def aes_gcm_decrypt_base64_string(key, nonce, ciphertext):
    # Decrypt message(base64.std.string) using AES-GCM
    cipher_bytes = base64.decodebytes(ciphertext.encode())
    return aes_gcm_decrypt_bytes(key, nonce, cipher_bytes).decode()


def marshal_cryptography_pub_key(key):
    # python version of crypto/elliptic/elliptic.go Marshal
    # without point on curve check
    return bytes([4]) + key.x.to_bytes(32, 'big') + key.y.to_bytes(32, 'big')


class key_agreement_client():
    def __init__(self, pem_path_or_string):
        """ Load cert and extract public key
        """
        if os.path.exists(pem_path_or_string):
            with open(pem_path_or_string, 'rb') as f:
                pem_data = f.read()
        else:
            pem_data = pem_path_or_string.encode()
        self._cert = x509.load_pem_x509_certificate(pem_data)
        cert_pub = self._cert.public_key().public_numbers()
        self._curve = ec._CURVE_TYPES[self._cert.public_key().curve.name]()
        self._public_key = ec.EllipticCurvePublicNumbers(
            cert_pub.x, cert_pub.y, self._curve).public_key()

    def generate_ecies_key_pair(self):
        """generate_ecies_key_pair generate ECIES key pair
        """
        # Generate an ephemeral elliptic curve scalar and point
        peer_private_key = ec.generate_private_key(self._curve)
        dh = peer_private_key.exchange(ec.ECDH(), self._public_key)
        R = peer_private_key.public_key().public_numbers()

        # Derive symmetric key and nonce via HKDF
        length = 32 + 12
        buf = HKDF(
            algorithm=hashes.SHA256(),
            length=length,
            salt=None,
            info=None,
        ).derive(dh)
        key = buf[:32]
        nonce = buf[32:length]

        token = marshal_cryptography_pub_key(R)
        return key, nonce, base64.b64encode(token).decode()
