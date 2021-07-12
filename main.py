from masstransitpython import RabbitMQSender
from json import loads
from pika import PlainCredentials
from masstransitpython import RabbitMQConfiguration
from json import JSONEncoder

class SampleMessage:
    def __init__(self, name):
        self.name = name

class MessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

RABBITMQ_USERNAME = 'secret'
RABBITMQ_PASSWORD = 'secret'
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_VIRTUAL_HOST = '/'

credentials = PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
conf = RabbitMQConfiguration(credentials,
                             queue='ApplicationBroker',
                             host=RABBITMQ_HOST,
                             port=RABBITMQ_PORT,
                             virtual_host=RABBITMQ_VIRTUAL_HOST,)

def send_message(body):
    """
    :param body: Message received from MassTransit client
    :return: None
    """
    with RabbitMQSender(conf) as sender:
        #sender.set_exchange('ApplicationMasterService.Messages:SampleMessage')
        sender.set_exchange('Aeb.ApplicationMasterService.Web.Consumer:ApplicationBrokerEventModel')
        encoded_msg = MessageEncoder().encode(SampleMessage("Hello World!"))
        response = sender.create_masstransit_response(loads(encoded_msg), body)
        sender.publish(message=response)

if __name__ == '__main__':
    from uuid import uuid4
    massTransitBody = {
        'messageId': str(uuid4()),
        'conversationId' : str(uuid4()),
        'sourceAddress' : '/',
        'destinationAddress' : '/',
        'message': 'test'
    }
    send_message(massTransitBody)

