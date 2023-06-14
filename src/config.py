# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - present Yarlagadda Naga Praveen
"""
import socket


from pydantic import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    secret_key: str = 'S#perS3crEt_9999'
    host_name: str = socket.gethostname()
    server_address: str = socket.gethostbyname(host_name)
    
    stripe_secret_key: str = None
    stripe_publishable_key: str = None
    stripe_is_active: bool = False
    stripe_client_id: str = None
    stripe_oauth_redirect: str = None

    def __init__(self):
        super().__init__()
        self.check_stripe()

    def check_stripe(self):
        if self.stripe_secret_key and self.stripe_publishable_key:
            self.stripe_is_active = True


    class Config:
        env_file = "./..env"


settings = Settings()
