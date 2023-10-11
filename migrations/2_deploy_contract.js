const MessageAuthentication = artifacts.require("MessageAuthentication");

module.exports = function (deployer) {
  deployer.deploy(MessageAuthentication, { gas: 2000000 }); // Adjust the gas limit as needed
};
