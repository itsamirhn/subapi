from configs import *

# These settings are just examples, you can change them as you like

REDIRECT = 'https://google.com'

USERS = (
    ("FirstUser", "c8fed114-79d9-4f89-8ef2-d4c40a057810"),
)

ADMIN = (b'admin', b'adminpassword')

CONFIGS: list[Config] = [
    VLESSConfig('name', 'server', 1080)
]