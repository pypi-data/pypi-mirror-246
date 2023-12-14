from plutus.classmodel.xcm_engine import XcmEngine
from thrift.transport import TSocket, TTransport, THttpClient
from thrift.protocol import TBinaryProtocol, TJSONProtocol

from plutus.rpc.server.gen_py.xcmrpc.ttypes import *
from plutus.classmodel.xxcm import *

from .constants import get_plutus_rpc_server_url

import plutus.rpc.server.gen_py.xcmrpc.RpcXcm as RpcXcm




def commit_instrument(ins: XInstrument):
    transport = THttpClient.THttpClient(get_plutus_rpc_server_url())
    transport.setCustomHeaders({"Content-Type": "application/json"})
    protocol = TJSONProtocol.TJSONProtocol(transport)
    client = RpcXcm.Client(protocol)
    instrument = RpcXInstrument()
    # instrument.id =  ins.Id()
    instrument.name = ins.Name()
    transport.open()
    ret = client.commit(instrument)
    transport.close()
    return ret

def query_instrument(name):
    transport = THttpClient.THttpClient(get_plutus_rpc_server_url())
    transport.setCustomHeaders({"Content-Type": "application/json"})
    protocol = TJSONProtocol.TJSONProtocol(transport)
    client = RpcXcm.Client(protocol)
    transport.open()
    ins: RpcXInstrument = client.query(name)
    transport.close()
    ret = XInstrument()
    ret.Name(ins.name)
    # ret.Id(ins.id)
    return ret



class XcmEngineRpc(XcmEngine):
    def commit(self, obj):
        print('XcmEngineOrm:commit')
        return commit_instrument(obj)

    def query(self, name):
        print('XcmEngineOrm:query')
        return query_instrument(name)
    
