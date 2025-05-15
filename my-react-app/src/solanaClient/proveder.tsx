import { Connection, clusterApiUrl } from "@solana/web3.js";
import { AnchorProvider } from "@project-serum/anchor";
import { Wallet } from "@solana/wallet-adapter-react";
// const programId = new PublicKey("A7sBBSngzEZTsCPCffHDbeXDJ54uJWkwdEsskmn2YBGo");

const network = clusterApiUrl("devnet");
const connection = new Connection(network, "processed");

// Use Phantom or any wallet adapter
export const getProvider = (arg: Wallet | null) => {
  // @ts-ignore
  if (!window.solana) {
    return
    // throw new Error("Wallet not found");
  }

  const provider = new AnchorProvider(
    connection,
    // @ts-ignore
    arg, // this is injected by Phantom
    {
      preflightCommitment: "processed",
    }
  );
  return provider;
};