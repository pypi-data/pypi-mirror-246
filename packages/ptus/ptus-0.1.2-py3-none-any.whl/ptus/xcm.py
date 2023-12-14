from plutus.classmodel.xcm import *
from .xcm_engine_rpc import XcmEngineRpc

XcmConfig().engine = XcmEngineRpc()
print('XcmEngineRpc initialized: %s' % XcmConfig().engine)