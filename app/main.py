from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from .worker import predict_async
from .config import REDIS_URL, MAX_QUEUE_SIZE

app = Flask(__name__)
redis_conn = Redis.from_url(REDIS_URL)
queue = Queue('ml_predictions', connection=redis_conn)

@app.route('/predict', methods=['POST'])
def predict():
    if not request.json or 'data' not in request.json:
        return jsonify({'error': 'No data provided'}), 400
        
    job = queue.enqueue(
        predict_async,
        request.json['data'],
        job_timeout='5m'
    )
    
    return jsonify({
        'job_id': job.id,
        'status': 'queued'
    })

@app.route('/status/<job_id>')
def get_status(job_id):
    job = queue.fetch_job(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
        
    status = {
        'job_id': job.id,
        'status': job.get_status(),
        'result': job.result if job.result else None
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run()
