import requests
from typing import Any, Dict, List

from colossus_sdk.colossus_exceptions import ColossusAPIError


class ColossusClient:
    """
    A client for interacting with the Colossus Staking API.

    Attributes:
        api_key (str): The API key used for authenticating with the Colossus
                       API.
        base_url (str): The base URL of the Colossus API.
    """

    def __init__(
        self, api_key: str, base_url: str = "http://57.128.162.54:3001/api/v1/"
    ) -> None:
        """
        Initializes the ColossusClient with an API key and base URL.

        Args:
            api_key (str): The API key for Colossus API.
            base_url (str): The base URL for the Colossus API. Defaults to
            'http://127.0.0.1:5000'.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.user_id = self._check_token_validity()

    def _check_token_validity(self) -> Any:
        """
        Checks if the API key is valid and returns the user's token.

        Returns:
            Any: The user's token if the API key is valid.

        Raises:
            Exception: If the API key is invalid or any other error occurs.
        """
        endpoint = "auth/authorization"
        url = self.base_url + endpoint
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            r = response.json()
            return r["response"]["token"]
        else:
            raise Exception(response.json())
        
    def create_tx_flow(self, flow_request: "FlowRequest") -> "FlowResponse":
        """
        Creates a new flow in the Colossus Staking API.

        Args:
            flow_request (FlowRequest): The flow request data.

        Returns:
            FlowResponse: The response from the API after creating the flow.

        Raises:
            ColossusAPIError: If the API request fails.
        """
        url = self.base_url + "flows"
        headers = {
            "Authorization": f"Bearer {self.user_id}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=flow_request, headers=headers)

        if response.status_code == 201:
            # return FlowResponse.from_dict(response.json()['response'])
            self.flow_id = response.json()["response"]["id"]
            return FlowResponse.from_dict(response.json()["response"])
        else:
            raise ColossusAPIError(response.status_code, response.text)

    def execute_flow_action(
        self, flow_id: str, action_name: str, action_inputs: Dict[str, Any]
    ):
        """
        Executes a flow action for a specified flow.

        Args:
            flow_id (str): The ID of the flow.
            action_name (str): The name of the action to be executed.
            action_inputs (Dict[str, Any]): The inputs for the flow action.

        Returns:
            FlowResponse: The response from the API after executing the flow
            action.

        Raises:
            ColossusAPIError: If the API request fails.
        """
        endpoint = "flows/" + flow_id
        url = self.base_url + endpoint

        data = {"name": action_name, "inputs": action_inputs}
        headers = {"Authorization": "Bearer " + self.user_id}
        response = requests.put(url, json=data, headers=headers)

        if (
            action_name == "broadcast_tx"
        ):  # the output of this endpoint is not ready yet so i return all the response
            return response.json()
        if response.status_code == 200:
            return FlowResponse.from_dict(response.json()["response"])
        else:
            raise ColossusAPIError(response.status_code, response.text)


# Model Classes
class FlowRequest:
    """
    Represents a request to create a new flow in the Colossus Staking API.

    Attributes:
        network (str): Network code of the flow.
        coin_ticker (str): Chain code of the flow.
        operation (str): The operation to be performed in the flow.
    """

    def __init__(self, network: str, coin_ticker: str, operation: str) -> None:
        """
        Initializes a FlowRequest instance.

        Args:
            network (str): testnet or mainnet.
            coin_ticker (str): ticker of coin.
            operation (str): The operation to be performed in the flow.
        """
        self.network = network
        self.coin_ticker = coin_ticker
        self.operation = operation

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the FlowRequest instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the FlowRequest
            instance.
        """
        return {
            "flow": {
                "network": self.network,
                "coin_ticker": self.coin_ticker,
                "operation": self.operation,
            }
        }


class FlowResponse:
    """
    Represents a response from the Colossus Staking API for a flow creation
    request.
    """

    def __init__(
        self,
        id: int,
        coin: str,
        operation: str,
        state: str,
        signature_status: str,
        actions: List[str],
        hex_to_sign_compressed: str,
        hex_to_sign_extended: str,
        raw_data: Any,
    ) -> None:
        """
        Initializes a FlowResponse instance with response data from the
        Colossus API.

        Args:
            id (int): The ID of the flow.
            coin (str): The coin of the operation/flow.
            operation (str): The operation to be performed in the flow.
            state (str): The current state of the flow.
            signature_status (str): The signature status of the flow.
            actions (List[str]): The actions that can be performed in the flow.
            hex_to_sign_compressed (str): The compressed hex string to sign.
            hex_to_sign_extended (str): The extended hex string to sign.
            raw_data (Any): The complete flow response data.
        """
        self.id = id
        self.coin = coin
        self.operation = operation
        self.state = state
        self.signature_status = signature_status
        self.actions = actions
        self.hex_to_sign_compressed = hex_to_sign_compressed
        self.hex_to_sign_extended = hex_to_sign_extended
        self.raw_data = raw_data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FlowResponse":
        """
        Constructs a FlowResponse object from a dictionary
        Args:
            data (Dict[str, Any]): A dictionary containing flow response data.
        Returns:
            FlowResponse: An instance of FlowResponse constructed from the
                          provided data.
        """
        if "data_to_sign_compressed" in list(data["outputs"].keys()):
            hex_to_sign_compressed = data["outputs"]["data_to_sign_compressed"]
            hex_to_sign_extended = data["outputs"]["data_to_sign_extended"]
        else:
            hex_to_sign_compressed = None
            hex_to_sign_extended = None

        return FlowResponse(
            id=data.get("id"),
            coin=data.get("coin_ticker"),
            operation=data.get("operation"),
            state=data.get("state"),
            signature_status=data.get("signature_status"),
            actions=data.get("actions"),
            hex_to_sign_compressed=hex_to_sign_compressed,
            hex_to_sign_extended=hex_to_sign_extended,
            raw_data=data,
        )


class DelegateDataRequest:
    """
    Represents a request for delegate data in the context of the Colossus API.

    Attributes:
        name (str): The name of the delegate operation.
        inputs (Dict[str, Any]): The input parameters for the delegate
        operation.
    """

    def __init__(self, name: str, inputs: Dict[str, Any]) -> None:
        """
        Initializes a new instance of DelegateDataRequest.

        Args:
            name (str): The name of the delegate operation.
            inputs (Dict[str, Any]): A dictionary of input parameters for the
            delegate operation.
        """
        self.name = name
        self.inputs = inputs

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the DelegateDataRequest instance to a dictionary.
        Returns:
            Dict[str, Any]: The dictionary representation of the request.
        """
        return self.inputs


class SubmitTransactionRequest:
    """
    Represents a request for submitting a signed transaction in the context of
    the Colossus API.

    Attributes:
        name (str): The name of the transaction operation, defaulting to
        "sign_delegate_tx".
        inputs (Dict[str, str]): Input parameters for the transaction,
        including the transaction payload.
        signatures (List[Dict[str, str]]): A list of signatures associated
        with the transaction.
    """

    def __init__(self, transaction_payload: str, signature_data: str) -> None:
        """
        Initializes a new instance of SubmitTransactionRequest.

        Args:
            transaction_payload (str): The payload of the signed transaction.
            signature_data (str): The signature data associated with the
            transaction.
        """
        self.name = "sign_delegate_tx"
        self.inputs = {"transaction_payload": transaction_payload}
        self.signatures = [{"signature_data": signature_data}]

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the SubmitTransactionRequest instance to a dictionary.

        Returns:
            Dict[str, Any]: The dictionary representation of the request,
            including name, inputs, and signatures.
        """
        return {
            "name": self.name,
            "inputs": self.inputs,
            "signatures": self.signatures,
        }
