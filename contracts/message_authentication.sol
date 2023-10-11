// SPDX-License-Identifier: UNKNOWN 
pragma solidity ^0.8.0;

contract MessageAuthentication {
    mapping(bytes32 => bool) public messageHashes;

    event MessageStored(bytes32 hash);

    function storeMessage(bytes32 hash) public {
        messageHashes[hash] = true;
        emit MessageStored(hash);
    }

    function getMessageHash() public view returns (bytes32) {
        return keccak256(abi.encodePacked(block.timestamp, block.difficulty));
    }
}
