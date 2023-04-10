# SubAPI

Simple FastAPI for Subscriptions

## Usage
1. Clone the project and fill `settings.py` based on your needs.
2. Build the docker image`docker build -t subapi .`
3. Run image: `docker run -d --name subapi -p 80:80 subapi`
4. Checkout `/users` for users **id** and then `/{id}` per user.


