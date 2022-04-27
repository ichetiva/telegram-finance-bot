from envparse import env

env.read_envfile(".env")

BOT_TOKEN = env.str("BOT_TOKEN")

DATABASE_CREDENTIALS = {
    "user": env.str("POSTGRES_USER"),
    "password": env.str("POSTGRES_PASSWORD"),
    "host": env.str("POSTGRES_HOST"),
    "database": env.str("POSTGRES_DATABASE"),
}

