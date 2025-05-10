import { Connection, PublicKey, clusterApiUrl } from "@solana/web3.js";
import { AnchorProvider, Program, web3 } from "@project-serum/anchor";
const programId = new PublicKey("A7sBBSngzEZTsCPCffHDbeXDJ54uJWkwdEsskmn2YBGo");

const network = clusterApiUrl("devnet");
const connection = new Connection(network, "processed");

// Use Phantom or any wallet adapter
export const getProvider = () => {
  // @ts-ignore
  if (!window.solana) throw new Error("Wallet not found");

  const provider = new AnchorProvider(
    connection,
    // @ts-ignore
    window.solana, // this is injected by Phantom
    {
      preflightCommitment: "processed",
    }
  );
  return provider;
};