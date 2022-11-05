import os

MODE = "test"
if MODE == "dev":
    NODE_URL = "https://fullnode.devnet.aptoslabs.com/v1"
    FAUCET_URL = os.getenv("APTOS_FAUCET_URL", "https://faucet.devnet.aptoslabs.com")
elif MODE == "test":
    NODE_URL = "https://fullnode.testnet.aptoslabs.com/v1"
    FAUCET_URL = os.getenv("APTOS_FAUCET_URL", "https://faucet.testnet.aptoslabs.com")
else:
    NODE_URL = os.getenv("APTOS_NODE_URL", "https://fullnode.mainnet.aptoslabs.com/v1")
    FAUCET_URL=None

CONTRACT_ADDRESS = "0xb33d04e0873c4f4b3fca881ddb2381658e620ce2cb598e1c60b925feb7d945c2::whitelist"
MKP_ADDRESS = "0xb33d04e0873c4f4b3fca881ddb2381658e620ce2cb598e1c60b925feb7d945c2::marketplace"
RESOURCE_ADDRESS = "0x95fcca7a4228616e228d3a8206003d7e4a15208ff1fbf4f8bc4af533430249e5"
RESOURCE_MKP_ADDRESS = "0xb8e8014fea807205fca0afb35ffa26c677ca3320b90bcdde4dd4f7fbefd89f97"
MAX_GAS = 1500000
GAS_UNIT = 100
BATCH_NUMBER = 200
IPFS_GATEWAY = "https://cloudflare-ipfs.com/ipfs/"
SUPPORTED_IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.webp')
AR_RESOLVER = "https://arweave.net/"

