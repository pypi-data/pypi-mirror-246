from colossus_sdk.colossus_client import (ColossusClient,
                                            FlowRequest,
                                            FlowResponse,
                                            DelegateDataRequest,
                                            ColossusAPIError)
import requests
import json

token = 'V1T2MA-O7XLFU-AJ01TU-NU015U-2X2L87'
base_url = "http://57.128.162.54:3001/api/v1/"

cl = ColossusClient(token, base_url)

signature = '4eab69fa61c13d0d101d07bc3692d1c793bb7c938a84e4917490a7cd482b26733bba96bc41a8a30f92b3129bdceb2aa9b0b5e4cc9d40b3ea58b1831e81ed09d4'
broadcast_input = {'signature': signature}
flow_id = 'ab19ce20-046b-4483-9ab6-2fb07a93bb77'

endpoint = 'flows/' + flow_id
url = cl.base_url + endpoint

tx = cl.execute_flow_action(flow_id, 'broadcast_tx', broadcast_input)
print(tx)
