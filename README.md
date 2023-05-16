# SubAPI

Simple FastAPI for Subscriptions

## Usage
1. Create a `custom.py` and fill it as `app/settings/base.py`
2. Run image: `docker run -v $(pwd)/custom.py:/app/settings/custom.py -p 80:80 ghcr.io/itsamirhn/subapi`
3. Checkout `/users` for users **id** and then `/{id}` per user.


