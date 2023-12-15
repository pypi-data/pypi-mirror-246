import logging
from abc import abstractmethod
from typing import Union
from urllib.parse import unquote

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ImproperlyConfigured
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import Resolver404, reverse
from django.views import View
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

LOGGER = logging.getLogger(__name__)

SETTINGS = (
    "AWS_REGION_NAME",
    "COLA_COGNITO_USER_POOL_ID",
    "COLA_COOKIE_NAME",
    "LOGIN_REDIRECT_URL",
    "LOGIN_URL",
    "LOGIN_FAILURE_TEMPLATE_PATH",
    "CONTACT_EMAIL",
)
for setting_key in SETTINGS:
    if not getattr(settings, setting_key):
        raise ImproperlyConfigured(f"{setting_key} must be set")

try:
    get_template(settings.LOGIN_FAILURE_TEMPLATE_PATH)
except Resolver404:
    LOGGER.error("If you intend to use COLA, please create the `post-login-errors` view")
    raise TemplateDoesNotExist("If you intend to use COLA, please create the `post-login-errors` view")

COLA_COOKIE_DOMAIN = getattr(settings, "COLA_COOKIE_DOMAIN", ".cabinetoffice.gov.uk")

COLA_ISSUER = f"https://cognito-idp.{settings.AWS_REGION_NAME}.amazonaws.com/{settings.COLA_COGNITO_USER_POOL_ID}"

COLA_JWK_URL = f"{COLA_ISSUER}/.well-known/jwks.json"


def flush_cola_cookie(response: HttpResponse) -> HttpResponse:
    """delete COLA cookie from response"""
    response.delete_cookie(settings.COLA_COOKIE_NAME, domain=COLA_COOKIE_DOMAIN)
    return response


def show_error_template(request: HttpRequest, message: str, logger_message: str) -> HttpResponse:
    error_response = render(
        request,
        settings.LOGIN_FAILURE_TEMPLATE_PATH,
        {"errors": message, "contact_email": settings.CONTACT_EMAIL},
    )
    flush_cola_cookie(error_response)
    LOGGER.error(logger_message)
    return error_response


class ColaLogout(View):
    @abstractmethod
    def post_logout(self):
        """
        A method that is invoked post logout of a user
        """
        pass

    @abstractmethod
    def pre_logout(self):
        """
        A method that is invoked pre logout of a user
        """
        pass

    def get(self, request: HttpRequest, **kwargs: dict) -> HttpResponse:
        """
        Logs a user out of the system and removes the COLA JWT from their browser cookies
        :param request: The HTTP request
        :return: A HTTP response without the JWT token cookie
        """

        response = redirect(reverse(settings.LOGIN_URL))
        response_without_cookie = flush_cola_cookie(response)
        logout(request)
        return response_without_cookie


class ColaLogin(View):
    @abstractmethod
    def pre_login(self):
        """
        A method that is invoked after checking if a user is already logged in,
        but before performing any actions on the request
        """
        pass

    @abstractmethod
    def post_login(self):
        """
        A method that is invoked after `handle_claims` and logging/authenticating a user,
        but before returning an HTTP response
        """
        pass

    @abstractmethod
    def handle_user_jwt_details(self, user: AbstractBaseUser, token_payload: dict) -> None:
        """
        A method that is invoked after logging/authenticating a user and before `post_login`,
        but before returning an HTTP response.
        Email is already taken from the token and saved to the user object before this
        :param user: The user that is logged in and authenticated
        :param token_payload: The token payload that includes information from COLA
        """
        pass

    def get(
        self, request: HttpRequest, **kwargs: dict
    ) -> Union[HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect]:
        if request.user and request.user.is_authenticated:
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))

        self.pre_login()

        if not (cola_cookie := request.COOKIES.get(settings.COLA_COOKIE_NAME, None)):
            return show_error_template(request, "No cookie found", "No cookie found")

        response = requests.get(COLA_JWK_URL, timeout=5)
        if response.status_code != 200:
            return show_error_template(request, "Failed to login", "Failed to get expected response from COLA")

        cola_cognito_user_pool_jwk = response.json()

        token = unquote(cola_cookie)

        if token.startswith("s:") and token.count(".") == 3:
            token = ".".join(token[2:].split(".")[:3])

        header = jwt.get_unverified_header(token)
        public_key = next(key for key in cola_cognito_user_pool_jwk["keys"] if key["kid"] == header["kid"])

        try:
            payload = jwt.decode(
                token=token,
                audience=settings.COLA_COGNITO_CLIENT_ID,
                issuer=COLA_ISSUER,
                algorithms=["RS256"],
                key=public_key,
                options={
                    "require_iat": True,
                    "require_aud": True,
                    "require_exp": True,
                    "require_iss": True,
                    "require_sub": True,
                },
            )
        except (ExpiredSignatureError, JWTClaimsError, JWTError) as error:
            return show_error_template(request, "Failed to login", f"cookie error: {error}")

        authenticated_user = {
            "email": payload["email"],
        }

        if user := authenticate(request=request, user_response=authenticated_user):
            LOGGER.info(f"Attempting to log user {user.pk} in")
            user.save()
            self.handle_user_jwt_details(user, payload)
            login(request, user)
            self.post_login()
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))

        return show_error_template(request, "Failed to login", "No user found")
