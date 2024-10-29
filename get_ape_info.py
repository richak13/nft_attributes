from web3 import Web3
from web3.providers.rpc import HTTPProvider
import requests
import json

# Define the Bored Ape contract address and Infura API URL
bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
api_url = "https://mainnet.infura.io/v3/f474620ee28c4a6185ac4f3facbd6cf6"

# Load ABI from file
with open('/home/codio/workspace/abi.json', 'r') as f:
    abi = json.load(f)

# Connect to the Ethereum provider
provider = HTTPProvider(api_url)
web3 = Web3(provider)
assert web3.is_connected(), "Failed to connect to Ethereum provider."

# Initialize contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Function to get Bored Ape NFT information
def get_ape_info(apeID):
    # Validate input
    assert isinstance(apeID, int), f"{apeID} is not an integer."
    assert apeID >= 1, f"ApeID {apeID} must be at least 1."

    data = {'owner': "", 'image': "", 'eyes': ""}

    try:
        # Get owner of the NFT
        owner = contract.functions.ownerOf(apeID).call()
        data['owner'] = owner

        # Retrieve the token URI and convert IPFS URI
        token_uri = contract.functions.tokenURI(apeID).call()
        ipfs_url = token_uri.replace("ipfs://", "https://ipfs.io/ipfs/")

        # Fetch metadata from IPFS
        metadata_response = requests.get(ipfs_url)
        if metadata_response.status_code == 200:
            metadata = metadata_response.json()
            data['image'] = metadata.get('image')
            data['eyes'] = next(
                (attr['value'] for attr in metadata.get('attributes', []) if attr['trait_type'] == 'Eyes'), None
            )
        else:
            raise Exception(f"Failed to retrieve metadata for ApeID {apeID}. Status code: {metadata_response.status_code}")

    except Exception as e:
        print(f"Error retrieving info for ApeID {apeID}: {e}")

    # Verify data structure
    assert isinstance(data, dict), f"get_ape_info({apeID}) should return a dictionary."
    assert all(key in data for key in ['owner', 'image', 'eyes']), "Return value should include keys 'owner', 'image', and 'eyes'."

    return data

# Example usage
apeID = 1
ape_info = get_ape_info(apeID)
print(ape_info)
