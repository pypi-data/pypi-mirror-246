import plutus.rpc.server.gen_py.xcmrpc.HelloWorld as HelloWorld
from .constants import get_plutus_rpc_server_url


async def use_xcm_rpc():
    from thrift.transport import TSocket, TTransport, THttpClient
    from thrift.protocol import TBinaryProtocol, TJSONProtocol

    class Instrument:
        def _set_client(self, client):
            self.client = client

        def _set_id(self, id):
            self.id = id

        def do_stuff(self):
            return self.client.remote('Instrument', self.id, 'do_stuff')

    transport = THttpClient.THttpClient(get_plutus_rpc_server_url())
    transport.setCustomHeaders({"Content-Type": "application/json"})
    protocol = TJSONProtocol.TJSONProtocol(transport)
    client = HelloWorld.Client(protocol)
    transport.open()

    person = client.getPerson("Alice")
    print(
        f"Received Person: Name - {person.name}, Age - {person.age}, Finger - {person.body.hand.finger}")

    ins = Instrument()
    ins._set_client(client)
    ins._set_id('some_id')
    print(ins.do_stuff())

    transport.close()
