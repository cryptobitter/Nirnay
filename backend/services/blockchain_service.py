import os
import json
import time
from web3 import Web3
from config import settings

# Module-level dictionary simulating on-chain storage for local testing without real credentials
_mock_chain_store = {}

class BlockchainService:
    """
    Service interfacing with Polygon Amoy testnet via Web3.py.
    """
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.POLYGON_AMOY_RPC_URL))
        self.contract_address = settings.CONTRACT_ADDRESS
        self.private_key = settings.PRIVATE_KEY
        self.abi = self._load_abi()

    def _load_abi(self):
        if os.path.exists(settings.CONTRACT_ABI_PATH):
            with open(settings.CONTRACT_ABI_PATH, 'r') as f:
                return json.load(f)
        # Default ABI matching submitRecord / getRecord specification
        return [
            {
                "inputs": [{"name": "recordHash", "type": "bytes32"}],
                "name": "submitRecord",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "recordHash", "type": "bytes32"}],
                "name": "getRecord",
                "outputs": [
                    {"name": "timestamp", "type": "uint256"},
                    {"name": "submitter", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]

    def record_hash_to_bytes32(self, hex_hash: str) -> bytes:
        if hex_hash.startswith("0x"):
            hex_hash = hex_hash[2:]
            
        if len(hex_hash) != 64:
            raise ValueError(f"Invalid hash length: expected 64 hex characters, got {len(hex_hash)}")
            
        return bytes.fromhex(hex_hash)

    def submit_record_hash(self, hex_hash: str) -> str:
        """
        Sends audit record hash to smart contract on Polygon Amoy.
        Returns transaction hash.
        """
        if not self.private_key or self.contract_address == "0x0000000000000000000000000000000000000000":
            # Realistic mock persistence for quick testing without testnet gas setup
            _mock_chain_store[hex_hash] = {"timestamp": int(time.time()), "submitter": "0xMockAddress"}
            return "0x" + "0" * 64  # clearly fake but valid-length placeholder tx hash

        try:
            account = self.w3.eth.account.from_key(self.private_key)
            contract = self.w3.eth.contract(address=self.w3.to_checksum_address(self.contract_address), abi=self.abi)

            bytes32_hash = self.record_hash_to_bytes32(hex_hash)
            nonce = self.w3.eth.get_transaction_count(account.address)

            tx = contract.functions.submitRecord(bytes32_hash).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            print(f"Blockchain submission error: {e}")
            raise RuntimeError(f"Failed to submit record hash to blockchain: {e}")

    def verify_record_on_chain(self, hex_hash: str) -> dict:
        """
        Queries smart contract mapping for verification details.
        """
        if not self.contract_address or self.contract_address == "0x0000000000000000000000000000000000000000":
            # Check the in-memory mock store
            if hex_hash in _mock_chain_store:
                record = _mock_chain_store[hex_hash]
                return {"exists": True, "timestamp": record["timestamp"], "submitter": record["submitter"]}
            else:
                return {"exists": False, "timestamp": 0, "submitter": None}

        try:
            contract = self.w3.eth.contract(address=self.w3.to_checksum_address(self.contract_address), abi=self.abi)
            bytes32_hash = self.record_hash_to_bytes32(hex_hash)
            result = contract.functions.getRecord(bytes32_hash).call()
            timestamp, submitter = result[0], result[1]

            return {
                "exists": timestamp > 0,
                "timestamp": timestamp,
                "submitter": submitter
            }
        except Exception as e:
            print(f"Blockchain verification error: {e}")
            return {"exists": False, "timestamp": 0, "submitter": None, "error": str(e)}

blockchain_service = BlockchainService()