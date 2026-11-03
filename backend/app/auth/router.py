from fastapi import APIRouter, BackgroundTasks, Response

from app.auth import service
from app.auth.schemas import ForgotIn, LoginIn, MessageOut, RegisterIn, ResetIn, UserOut
from app.core.config import get_settings
from app.core.deps import ClientIp, CurrentSession, CurrentUser, DbSession

router = APIRouter(prefix="/auth", tags=["auth"])

FORGOT_MESSAGE = "Si el email está registrado, te enviamos un enlace para restablecer la contraseña."


def _set_cookie(response: Response, token: str) -> None:
    s = get_settings()
    response.set_cookie(
        key=s.cookie_name,
        value=token,
        max_age=s.session_ttl_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=s.cookie_secure,
        path="/",
    )


def _clear_cookie(response: Response) -> None:
    s = get_settings()
    response.delete_cookie(key=s.cookie_name, path="/", httponly=True, samesite="lax", secure=s.cookie_secure)


@router.post("/register", response_model=UserOut, status_code=201)
def register(body: RegisterIn, response: Response, db: DbSession, ip: ClientIp) -> UserOut:
    user, token = service.register(db, body.email, body.password, ip)
    _set_cookie(response, token)
    return UserOut.model_validate(user)


@router.post("/login", response_model=UserOut)
def login(body: LoginIn, response: Response, db: DbSession, ip: ClientIp) -> UserOut:
    user, token = service.login(db, body.email, body.password, ip)
    _set_cookie(response, token)
    return UserOut.model_validate(user)


@router.post("/logout", status_code=204)
def logout(db: DbSession, session: CurrentSession) -> Response:
    service.logout(db, session)
    response = Response(status_code=204)
    _clear_cookie(response)
    return response


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> UserOut:
    return UserOut.model_validate(user)


@router.post("/password/forgot", response_model=MessageOut, status_code=202)
def forgot_password(
    body: ForgotIn, background: BackgroundTasks, db: DbSession, ip: ClientIp
) -> MessageOut:
    result = service.request_password_reset(db, body.email, ip)
    if result:
        # En segundo plano: el tiempo de respuesta no delata si la cuenta existe.
        background.add_task(service.send_reset_email, *result)
    return MessageOut(message=FORGOT_MESSAGE)


@router.post("/password/reset", status_code=204)
def reset_password(body: ResetIn, db: DbSession, ip: ClientIp) -> Response:
    service.reset_password(db, body.token, body.new_password, ip)
    return Response(status_code=204)
