from flask import Flask, jsonify, request
from confluent_kafka import Consumer
import json
import os
from typing import Dict

app = Flask(__name__)


def get_kafka_config(profile: str = "default") -> Dict:
    """
    Return different Kafka configurations based on profile.
    All values come from environment variables with sensible defaults.
    """
    profiles = {
        "default": {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'group.id': os.getenv('KAFKA_GROUP_ID', 'flask-on-demand-consumer'),
            'auto.offset.reset': os.getenv('KAFKA_AUTO_OFFSET_RESET', 'latest'),
            'enable.auto.commit': False,
            'client.id': os.getenv('KAFKA_CLIENT_ID', 'flask-consumer-default'),
        },

        "events": {
            'bootstrap.servers': os.getenv('KAFKA_EVENTS_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'group.id': os.getenv('KAFKA_EVENTS_GROUP_ID', 'flask-events-consumer'),
            'auto.offset.reset': os.getenv('KAFKA_AUTO_OFFSET_RESET', 'latest'),
            'enable.auto.commit': False,
            'client.id': 'flask-events-consumer',
        },

        "audit": {
            'bootstrap.servers': os.getenv('KAFKA_AUDIT_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'group.id': os.getenv('KAFKA_AUDIT_GROUP_ID', 'flask-audit-consumer'),
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'client.id': 'flask-audit-consumer',
        },
    }

    if profile not in profiles:
        raise ValueError(f"Unknown Kafka profile: {profile}. Available: {list(profiles.keys())}")

    config = profiles[profile]

    # Security settings (if needed)
    if os.getenv('KAFKA_SECURITY_PROTOCOL'):
        config['security.protocol'] = os.getenv('KAFKA_SECURITY_PROTOCOL')
        config['sasl.mechanism'] = os.getenv('KAFKA_SASL_MECHANISM')
        config['sasl.username'] = os.getenv('KAFKA_SASL_USERNAME')
        config['sasl.password'] = os.getenv('KAFKA_SASL_PASSWORD')

    return config


@app.route("/")
def home():
    return "<h1>Hello BMW from Flask on EKS!</h1><p>Development mode active.</p>"


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route('/consume', methods=['GET'])
def consume_now():
    """
    Consume messages on-demand.

    Query parameters:
    - topic (default: my-topic)
    - max (default: 10)
    - profile (default: default) → Choose which Kafka cluster/config to use
    """
    topic = request.args.get('topic', 'my-topic')
    max_messages = int(request.args.get('max', 10))
    profile = request.args.get('profile', 'default')   # ← New: select config

    try:
        kafka_config = get_kafka_config(profile)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    consumer = Consumer(kafka_config)
    consumer.subscribe([topic])

    messages = []
    try:
        for _ in range(max_messages):
            msg = consumer.poll(timeout=2.0)
            if msg is None:
                continue
            if msg.error():
                return jsonify({"error": str(msg.error())}), 500

            try:
                data = json.loads(msg.value().decode('utf-8'))
                messages.append(data)
            except json.JSONDecodeError:
                messages.append({"raw": msg.value().decode('utf-8')})
    finally:
        consumer.close()

    return jsonify({
        "profile": profile,
        "topic": topic,
        "message_count": len(messages),
        "messages": messages
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
