// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract IpfsDiary is Ownable{

    constructor(address initialOwner) Ownable(initialOwner) {
    }

    struct Diary {
        string cid;
        string timestamp_title;
    }

    uint256 private _diaryIdCounter;
    mapping(uint256 => Diary) private _idToDiary;

    function currentId() public view returns(uint256){
        return _diaryIdCounter;
    }

    function addNewDiary(string calldata _cid, string calldata _timestamp_title)  external onlyOwner(){
        // _diaryIdCounterをインクリメントする．
        unchecked {
            _diaryIdCounter++;
        }
        Diary memory newDiary = Diary(_cid, _timestamp_title);
        _idToDiary[_diaryIdCounter] = newDiary;
    }

    function showDiaryCid(uint256 _id) external view onlyOwner returns(string memory){
        Diary memory targetDiary = _idToDiary[_id];
        return targetDiary.cid;
    }

    function reset_diaryIdCounter() external onlyOwner{
        _diaryIdCounter = 0;
    }
}
