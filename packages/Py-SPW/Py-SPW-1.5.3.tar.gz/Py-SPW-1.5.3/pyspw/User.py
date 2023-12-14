from enum import Enum
from typing import Optional

import requests as rq
from mojang import API as MAPI
from mojang._types import UserProfile

from . import errors as err
from .errors import MojangAccountNotFound

mapi = MAPI()

headers = {
    'User-Agent': f'Py-SPW'
}


class SkinVariant(Enum):
    """
    Варианты скинов.
    """
    SLIM = 'slim'
    CLASSIC = 'classic'


class _SkinPart:
    def __init__(self, url: str):
        self.__skin_part_url = url

    def __str__(self):
        return self.get_url()

    def __bytes__(self):
        return self.get_image()

    def get_url(self) -> str:
        """
        Получения ссылки на изображение части скина.

        :return: Ссылка на изображение части скина.
        """
        return self.__skin_part_url

    def get_image(self) -> bytes:
        """
        Получения изображения части скина.

        :return: Изображения части скина.
        """

        try:
            visage_surgeplay_response = rq.get(self.__skin_part_url, headers=headers)
            if visage_surgeplay_response.status_code != 200:
                raise err.SurgeplayApiError(f'HTTP status: {visage_surgeplay_response.status_code}')
            return visage_surgeplay_response.content

        except rq.exceptions.ConnectionError as error:
            raise err.SurgeplayApiError(error)


class Skin:
    __visage_surgeplay_url = 'https://visage.surgeplay.com/'

    def __init__(self, profile: UserProfile):
        self._profile = profile
        self._variant = SkinVariant(profile.skin_variant)

    @property
    def variant(self) -> SkinVariant:
        return self._variant

    def get_face(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/face/{image_size}/{self._profile.id}')

    def get_front(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/front/{image_size}/{self._profile.id}')

    def get_front_full(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/frontfull/{image_size}/{self._profile.id}')

    def get_head(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/head/{image_size}/{self._profile.id}')

    def get_bust(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/bust/{image_size}/{self._profile.id}')

    def get_full(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/full/{image_size}/{self._profile.id}')

    def get_skin(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/skin/{image_size}/{self._profile.id}')

    def get_cape(self) -> Optional[_SkinPart]:
        if self._profile.cape_url is None:
            return None
        return _SkinPart(self._profile.cape_url)


class User:
    def __init__(self, nickname: str):
        self._nickname = nickname
        self._uuid = mapi.get_uuid(nickname)
        if self._uuid is None:
            raise MojangAccountNotFound(self._nickname)
        self._profile = mapi.get_profile(self._uuid)

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def profile(self) -> UserProfile:
        return self._profile

    def get_skin(self) -> Skin:
        """
        Получения объекта скина пользователя.
        """
        return Skin(self._profile)
