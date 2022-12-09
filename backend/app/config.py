from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


# By doing the following we will tell pydantic to read the environment variables from the file .env and use them as the values for the variables in the class:
    class Config:
        env_file = ".env"


settings = Settings()



# we are creating an instance of Settings class  and pydantic will read all of the environment variables listed in the Settings class 
                      # and its going to perform validations 

