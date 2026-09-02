import hre from "hardhat";

async function main() {
  const { ethers } = await hre.network.connect();

  console.log("Deploying NirnayRegistry to Polygon Amoy...");

  const nirnayRegistry = await ethers.deployContract("NirnayRegistry");

  await nirnayRegistry.waitForDeployment();

  const address = await nirnayRegistry.getAddress();

  console.log("✅ NirnayRegistry deployed to:", address);
  console.log("Copy this address into backend/.env as CONTRACT_ADDRESS");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});