from colossus_sdk.colossus_client import (ColossusClient,
                                            FlowRequest,
                                            FlowResponse,
                                            DelegateDataRequest,
                                            ColossusAPIError)
import json

token = 'V1T2MA-O7XLFU-AJ01TU-NU015U-2X2L87'
base_url = "http://57.128.162.54:3001/api/v1/"

cl = ColossusClient(token, base_url)
print('USER ID:', cl.user_id)

coin = 'atom'
network = 'testnet'
operation = 'delegate'

fr = FlowRequest(network, coin, operation)
#print('\nFLOW REQUEST INPUT:', fr.to_dict())

#print('\nRunning create_flow...')
r = cl.create_tx_flow(fr.to_dict())
print('\nFLOW ID:', r.id)
#print('\nSTATE:', r.state)
#print('\nSignature Status:', r.signature_status)
#print('\n Hex to sign compressed:', r.hex_to_sign_compressed)
#print('\n Hex to sign extended:', r.hex_to_sign_extended)
#print('\nACTIONS:', r.actions)
#print('\nCreate flow output:', r.raw_data)


delegation_inputs = {'sender_pub_key': '03c6ea326c0e5e9198287ddada31d542e3051e5339746fb28b914b1e746bdc11b8',
                     'validator_address': 'cosmosvaloper10jt73m3mlkmsqsys7jl7aktzj9nsdrgxxvy4j5',
                     'amount': 15}

#print('\nRunning execute_flow_action...')
tx = cl.execute_flow_action(r.id, 'create_delegate_tx', delegation_inputs)
#print('\nSTATE:', tx.state)
#print('\nSignature Status:', tx.signature_status)
print('\n Hex to sign compressed:', tx.hex_to_sign_compressed)
#print('\n Hex to sign extended:', tx.hex_to_sign_extended)
#print('\nexecute action output:', tx.raw_data)


'''
for i in r.actions:
    print('\n', i['name'])
    for j in i['inputs']:
        print(j['name'], 'required:',  j['required'], 'type:', j['type'])
'''

