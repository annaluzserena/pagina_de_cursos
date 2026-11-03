"""Canonicalización conservadora de URLs (TRD TD-009, BackendSchema §4).

Solo reglas seguras: esquema/host en minúsculas, sin fragmento, sin puerto por
defecto y sin slash final. NO se tocan los parámetros de query.
"""
import ipaddress
import re
from urllib.parse import urlsplit, urlunsplit

MAX_LEN = 2048
_DEFAULT_PORTS = {"http": 80, "https": 443}


def canonicalize(raw: str) -> tuple[str, str]:
    """Devuelve (url_canónica, host). Lanza ValueError con mensaje apto para el usuario."""
    raw = raw.strip()
    if not raw or len(raw) > MAX_LEN:
        raise ValueError("La URL es obligatoria y debe tener como máximo 2048 caracteres.")
    if re.search(r"[\s\x00-\x1f]", raw):
        raise ValueError("La URL no puede contener espacios ni caracteres de control.")

    try:
        parts = urlsplit(raw)
        port = parts.port
    except ValueError:
        raise ValueError("La URL no es válida.") from None

    scheme = parts.scheme.lower()
    if scheme not in _DEFAULT_PORTS:
        raise ValueError("La URL debe comenzar con http:// o https://.")
    if parts.username or parts.password:
        raise ValueError("La URL no puede incluir usuario ni contraseña.")

    host = (parts.hostname or "").lower().rstrip(".")
    if not host:
        raise ValueError("La URL debe incluir un dominio.")
    try:
        ipaddress.ip_address(host)
        is_ip = True
    except ValueError:
        is_ip = False
    if is_ip:
        raise ValueError("Usá la URL con dominio del curso, no una dirección IP.")
    if "." not in host:
        raise ValueError("La URL debe incluir un dominio público válido.")
    try:
        host = host.encode("idna").decode("ascii")
    except UnicodeError:
        raise ValueError("El dominio de la URL no es válido.") from None

    netloc = host if port in (None, _DEFAULT_PORTS[scheme]) else f"{host}:{port}"
    path = parts.path or "/"
    if len(path) > 1:
        path = path.rstrip("/") or "/"
    canonical = urlunsplit((scheme, netloc, path, parts.query, ""))
    if len(canonical) > MAX_LEN:
        raise ValueError("La URL es demasiado larga.")
    return canonical, host.removeprefix("www.")
