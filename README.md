### Running Locally

First, clone the repo, create a Python virtual environment and install dependencies:

```bash
git clone https://github.com/gokhansengun/gitpod-flask-redis.git
cd gitpod-flask-redis
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

If you're using Docker to run Redis Stack, start the container using docker compose or just create a redis running locally at port 6379

```bash
docker compose up -d # or docker-compose up -d when using old cli
```

Then start the app:

```bash
export OTEL_SERVICE_NAME="sample-flask-app"
export OTEL_EXPORTER_OTLP_ENDPOINT=http://192.168.25.103:32209

opentelemetry-instrument python app.py
```

Now, open tabs in your browser for each of the following URLs:

* Application: `http://127.0.0.1:5000`
* Error endpoint: `http://127.0.0.1:5000/emit-error?reason=some-reason`
* Create traffic with: `while true; do curl http://127.0.0.1:5001/incr ; sleep 0.1; done`
