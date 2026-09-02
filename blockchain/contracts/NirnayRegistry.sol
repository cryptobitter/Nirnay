// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Nirnay Registry - AI Policy Decision Auditor
/// @notice Stores tamper-evident hashes of AI-generated policy decisions for public verification.
/// @dev Implements an allowlist to ensure only the official backend wallet can submit records.
contract NirnayRegistry {
    
    struct Record {
        uint256 timestamp;
        address submitter;
    }

    /// @notice The administrator of the contract (the deployer)
    address public owner;

    /// @notice Maps a SHA-256 record hash to its anchoring details
    mapping(bytes32 => Record) private _records;

    /// @notice Tracks which addresses are authorized to submit records to the chain
    mapping(address => bool) public approvedSubmitters;

    /// @notice Emitted when a new assessment hash is anchored to the blockchain
    event RecordSubmitted(bytes32 indexed recordHash, address indexed submitter, uint256 timestamp);
    
    /// @notice Emitted when a new backend wallet is authorized
    event SubmitterAdded(address indexed account);
    
    /// @notice Emitted when a backend wallet is deauthorized
    event SubmitterRemoved(address indexed account);

    modifier onlyOwner() {
        require(msg.sender == owner, "Nirnay: caller is not the owner");
        _;
    }

    modifier onlyApprovedSubmitter() {
        require(approvedSubmitters[msg.sender], "Nirnay: caller is not an approved submitter");
        _;
    }

    /// @notice Sets the deployer as the owner and adds them to the initial allowlist
    constructor() {
        owner = msg.sender;
        approvedSubmitters[msg.sender] = true;
        emit SubmitterAdded(msg.sender);
    }

    /// @notice Authorizes a new address to submit record hashes
    /// @param account The address to authorize
    function addSubmitter(address account) external onlyOwner {
        require(!approvedSubmitters[account], "Nirnay: address already approved");
        approvedSubmitters[account] = true;
        emit SubmitterAdded(account);
    }

    /// @notice Revokes submission authorization from an address
    /// @param account The address to deauthorize
    function removeSubmitter(address account) external onlyOwner {
        require(approvedSubmitters[account], "Nirnay: address not approved");
        require(account != owner, "Nirnay: cannot remove the owner");
        approvedSubmitters[account] = false;
        emit SubmitterRemoved(account);
    }

    /// @notice Anchors a new policy assessment hash to the blockchain
    /// @dev Reverts if the exact hash has already been submitted to prevent overwrites/duplicates
    /// @param recordHash The 32-byte SHA-256 hash of the deterministic assessment JSON
    function submitRecord(bytes32 recordHash) external onlyApprovedSubmitter {
        require(_records[recordHash].timestamp == 0, "Nirnay: record hash already exists");

        _records[recordHash] = Record({
            timestamp: block.timestamp,
            submitter: msg.sender
        });

        emit RecordSubmitted(recordHash, msg.sender, block.timestamp);
    }

    /// @notice Retrieves the anchoring details of a specific policy assessment hash
    /// @dev Returns (0, address(0)) if the hash has never been submitted
    /// @param recordHash The 32-byte SHA-256 hash to query
    /// @return timestamp The block timestamp when the record was anchored
    /// @return submitter The authorized backend wallet address that submitted it
    function getRecord(bytes32 recordHash) external view returns (uint256 timestamp, address submitter) {
        Record memory rec = _records[recordHash];
        return (rec.timestamp, rec.submitter);
    }
}