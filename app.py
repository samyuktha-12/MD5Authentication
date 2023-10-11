from flask import Flask, render_template, request, redirect, url_for
import requests
import hashlib
import random

app = Flask(__name__)

# Global dictionary to store block data
BLOCK_DATA = {}
# Global dictionary to store output for display
OUTPUT_DATA = {}

# Ganache URL (replace with your Ganache URL)
GANACHE_URL = "http://localhost:7545"

def mine_block(message):
    try:
        # Compute the MD5 hash of the message
        md5_digest = hashlib.md5(message.encode()).hexdigest()
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

                # Store block hash, message, and MD5 in BLOCK_DATA
                BLOCK_DATA[block_hash] = {
                    "message": message,
                    "md5_digest": md5_digest,
                }

                # Store output data for display
                OUTPUT_DATA[block_hash] = {
                    "message": message,
                    "md5_digest": md5_digest,
                    "correct": None,  # Initialize correctness to None
                }
                return block_hash
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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

def sender(message):
    try:
        # Mine a new block with the generated message
        block_hash = mine_block(message)

        # Generate a random message (either the same message or with 'a' appended)
        message = message if random.choice([True, False]) else message+"a"

        block_hash=receiver(message,block_hash)
        return block_hash
    except Exception as e:
        print(f"Sender: An error occurred: {e}")
        return None

def receiver(sender_message,block_hash):
    try:
        # Get the last block hash from the global dictionary
        last_md5=BLOCK_DATA[block_hash]["md5_digest"]
        OUTPUT_DATA[block_hash]["receiver_message"] = sender_message

        if last_md5:

            # Compute the MD5 hash of the sender's message
            md5_digest = hashlib.md5(sender_message.encode()).hexdigest()
            OUTPUT_DATA[block_hash]["receiver_digest"] = md5_digest
            # Compare the received digest with the last block's data digest
            is_correct = md5_digest == last_md5

            # Store correctness in OUTPUT_DATA
            OUTPUT_DATA[block_hash]["correct"] = is_correct

            return block_hash
        else:
            return None, False
    except Exception as e:
        print(f"Receiver: An error occurred: {e}")
        return None, False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        block_hash=sender(message)
        print(OUTPUT_DATA[block_hash])
        return redirect(url_for("index"))

    # Display the block data, message, MD5 digest, and correctness
    block_data_list = [{"hash": key, **OUTPUT_DATA[key]} for key in OUTPUT_DATA.keys()]
    print(block_data_list)
    return render_template("index.html", block_data_list=block_data_list)

if __name__ == "__main__":
    app.run(debug=True)
