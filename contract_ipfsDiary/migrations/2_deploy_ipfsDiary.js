require('dotenv').config({path: `../.env`});
const {MY_ID} = process.env;
const IpfsDiaryContract = artifacts.require("IpfsDiary");

module.exports = function(deployer) {
  
  deployer.deploy(IpfsDiaryContract, MY_ID);
}