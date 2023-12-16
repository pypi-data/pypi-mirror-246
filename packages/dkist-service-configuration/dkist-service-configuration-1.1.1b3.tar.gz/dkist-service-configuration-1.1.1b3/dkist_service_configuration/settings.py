"""
Wrapper for retrieving configurations and safely logging their retrieval
"""
import re

from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import Field

from dkist_service_configuration.logging import logger


class ConfigurationBase(BaseSettings):
    """Settings base which logs configured settings while censoring secrets"""

    log_level: str = Field("INFO", env="LOGURU_LEVEL")
    # env -> validation_alias in pydantic 2.x

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8") in pydantic 2.x

    @staticmethod
    def _is_secret(field_name: str) -> bool:
        for pattern in ("pass", "secret", "token"):
            if re.search(pattern, field_name):
                return True
        return False

    def log_configurations(self):
        for field_name in self.__fields__:  # __fields__ -> model_fields in pydantic 2.x
            if self._is_secret(field_name=field_name):
                logger.info(f"{field_name}: <CENSORED>")
            else:
                logger.info(f"{field_name}: {getattr(self, field_name)}")


class MeshService(BaseModel):
    """Model of the metadata for a node in the service mesh"""

    host: str = Field(..., alias="mesh_address")
    port: int = Field(..., alias="mesh_port")


DEFAULT_MESH_SERVICE = MeshService(mesh_address="127.0.0.1", mesh_port=0)


class MeshServiceConfigurationBase(ConfigurationBase):
    """
    Settings base for services using a mesh configuration to define connections in the form
    {
        "upstream_service_name": {"mesh_address": "localhost", "mesh_port": 6742}
    }
    """

    service_mesh: dict[str, MeshService] = Field(
        default_factory=dict, env="MESH_CONFIG"
    )  # env -> validation_alias when going to pydantic 2.x

    def service_mesh_detail(
        self, service_name: str, default_mesh_service: MeshService = DEFAULT_MESH_SERVICE
    ) -> MeshService:
        mesh_service = self.service_mesh.get(service_name) or default_mesh_service
        return mesh_service
