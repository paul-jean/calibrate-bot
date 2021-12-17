from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask
from flask import request
import celery
import os
import redis

app = Flask(__name__)
cel = celery.Celery('canna-track-bot')

cel.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

r = redis.from_url(os.environ.get("REDIS_URL"))


@cel.task
def schedule_response(resp):
    return str(resp)


@app.route('/bot', methods=['POST'])
def bot():
    # add webhook logic here and return a response
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    schedule_response.apply_async(
        args=('... and 5 second delayed response!'), countdown=5)
    return str(resp)


if __name__ == '__main__':
    app.run()
