import os

def get_plutus_rpc_server_url():
    return os.environ.get('PLUTUSOS_SERVER_ADDRESS') or 'https://orca-app-t2q3p.ondigitalocean.app'