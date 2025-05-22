import { Connection, clusterApiUrl } from "@solana/web3.js";
import { AnchorProvider } from "@project-serum/anchor";
import {WalletContextState } from "@solana/wallet-adapter-react";
// const programId = new PublicKey("A7sBBSngzEZTsCPCffHDbeXDJ54uJWkwdEsskmn2YBGo");

const network = clusterApiUrl("devnet");
const connection = new Connection(network, "processed");

// Use Phantom or any wallet adapter
export const getProvider = (arg: WalletContextState | null) => {
  
  let arg2 = arg
console.log(arg2)
  
  // @ts-ignore
  if (!window.solana) {
    return
    // throw new Error("Wallet not found");
  }

  const provider = new AnchorProvider(
    connection,

    // @ts-ignore
    window.solana,
    // {...arg, signTransaction: arg?.signTransaction}, 
    //  this is injected by Phantom
    {
      preflightCommitment: "processed",
    }
  );
  return provider;
};