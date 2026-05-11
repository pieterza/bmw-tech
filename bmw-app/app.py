from flask import Flask, jsonify, request
from confluent_kafka import Consumer
import json,os

app = Flask(__name__)

kafka_config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'group.id': 'flask-on-demand-consumer',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': False,
}

@app.route("/")
def home():
    return "<h1>Hello BMW from Flask on EKS!<h1><p>Development mode active.</p>"

@app.route("/health")
def health():
    return {"status": "ok"}

# Optional route to consume in a blocking manner.
@app.route('/consume', methods=['GET'])
def consume_now():
    topic = request.args.get('topic', 'my-topic')
    max_messages = int(request.args.get('max', 10))

    consumer = Consumer(kafka_config)
    consumer.subscribe([topic])

    messages = []
    for _ in range(max_messages):
        msg = consumer.poll(timeout=2.0)
        if msg and not msg.error():
            messages.append(json.loads(msg.value().decode('utf-8')))

    consumer.close()
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
