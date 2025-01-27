# import logging
# from logging.config import dictConfig
# from pydantic import BaseSettings

# # Classe de configuration (paramètres)
# class Settings(BaseSettings):
#     LOG_LEVEL: str = "INFO"
#     LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# settings = Settings()

# def setup_app_logging(config: Settings):
#     """Configure le système de journalisation avec des paramètres personnalisés."""
#     log_config = {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "default": {
#                 "format": config.LOG_FORMAT
#             },
#         },
#         "handlers": {
#             "console": {
#                 "class": "logging.StreamHandler",
#                 "formatter": "default",
#             },
#         },
#         "root": {
#             "level": config.LOG_LEVEL,
#             "handlers": ["console"],
#         },
#     }
#     dictConfig(log_config)
