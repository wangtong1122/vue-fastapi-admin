TORTOISE_ORM: dict = {
    "connections": {
        "mysql": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "192.168.55.10",  # Database host address
                "port": 3306,  # Database port
                "user": "root",  # Database username
                "password": "iopagent",  # Database password
                "database": "aerich_learn",  # Database name
            },
        },
    },
    "apps": {
        "models": {
            # Use an absolute import path that is importable from the repo root.
            # `aerich_demo` lives under `app/db_script/`, so `aerich_demo.models` may not be importable
            # unless you tweak PYTHONPATH / run from that folder.
            "models": ["app.db_script.aerich_demo.models", "aerich.models"],
            "default_connection": "mysql",
        },
    },
    "use_tz": False,  # Whether to use timezone-aware datetimes
    "timezone": "Asia/Shanghai",  # Timezone setting
}