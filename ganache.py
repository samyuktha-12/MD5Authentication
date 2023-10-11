import requests

GANACHE_URL = "http://localhost:7545"  # Replace with your Ganache URL
BLOCK_DATA = {}  # Global dictionary to store block data

def get_latest_block():
    try:
        response = requests.post(GANACHE_URL, json={
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": ["latest", False],
            "id": 1,
        })

        if response.status_code == 200:
            return response.json()["result"]
        else:
            print("Failed to get the latest block.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    while True:
        input_string = input("Enter a string (or 'q' to quit): ")
        if input_string == 'q':
            break

        # Mine a new block
        response = requests.post(GANACHE_URL, json={
            "jsonrpc": "2.0",
            "method": "evm_mine",
            "params": [],
            "id": 1,
        })

        if response.status_code == 200:
            latest_block = get_latest_block()
            if latest_block:
                block_hash = latest_block["hash"]
                BLOCK_DATA[block_hash] = input_string
                print(f"Block mined. Hash: {block_hash}, Data: {input_string}")
        else:
            print("Failed to mine a new block.")

    # Display the global dictionary when done
    print("Block Data:")
    for block_hash, data in BLOCK_DATA.items():
        print(f"Block Hash: {block_hash}, Data: {data}")
