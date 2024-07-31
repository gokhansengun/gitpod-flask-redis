from flask import Flask, request, render_template
import redis
import random
import time

from opentelemetry import trace

# Acquire a tracer
tracer = trace.get_tracer("sampleapp.tracer")

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True
)

# Redis key name that we will store our counter in.
COUNTER_KEY_NAME = "mycounter"

@app.route("/incr")
def incr():
    with tracer.start_as_current_span("outer-job") as outerspan:
        count = r.incrby(COUNTER_KEY_NAME, 1)
        outerspan.set_attribute("counter.value", count)

        # add a random delay between 20 to 80 ms to simulate a slow request
        time.sleep(random.uniform(0.02, 0.08))

        with tracer.start_as_current_span("inner-job") as innerspan:
            # add a random delay between 10 to 30 ms to simulate a slow request
            time.sleep(random.uniform(0.01, 0.03))

        return { "count": count }

@app.route("/reset")
def reset():
    with tracer.start_as_current_span("reset") as samplespan:
        # Reset by just deleting the key from Redis.
        count = r.get(COUNTER_KEY_NAME)
        samplespan.set_attribute("reset.atvalue", count)
        r.delete(COUNTER_KEY_NAME)

        # add a random delay between 20 to 80 ms to simulate a slow request
        time.sleep(random.uniform(0.02, 0.08))

        return { "count": 0 }
    
@app.route("/emit-error")
def emit_error():
    reason = request.args.get('reason', 'unknown')

    with tracer.start_as_current_span("emit-error") as samplespan:
        # Simulate an error by dividing by zero.
        count = r.get(COUNTER_KEY_NAME)
        samplespan.set_attribute("error.atvalue", count)

        raise Exception(f"Error: {reason}")

@app.route("/")
def home():
    with tracer.start_as_current_span("home") as samplespan:
        # Get the current counter value.
        count = r.get(COUNTER_KEY_NAME)
        if count is None:
            count = 0

        # Render the home page with the current counter value.
        return render_template('homepage.html', count = count)

if __name__ == "__main__":
    app.run(port=5000)
