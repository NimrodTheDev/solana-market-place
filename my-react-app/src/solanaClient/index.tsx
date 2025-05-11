import { createContext, useContext, ReactNode } from 'react';
// import init, { create_token_mint } from 'wasm';
import * as web3 from '@solana/web3.js';
//import * as token from '@solana/spl-token';
// import * as anchor from "@coral-xyz/anchor";
import {Program} from "@project-serum/anchor";

// import { useConnection } from '@solana/wallet-adapter-react';
import { PhantomWalletAdapter } from '@solana/wallet-adapter-phantom';
// import { Program, Idl } from '@coral-xyz/anchor';
import drc_token_json from "./drc_token.json"
// import { DrcToken } from './drc_token_type';
import { getProvider } from './proveder';
import { Buffer as buffer } from "buffer";

//@ts-ignore
global.Buffer = buffer;

Buffer = buffer;
console.log(Buffer)

const TOKEN_METADATA_PROGRAM_ID = new web3.PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s');

interface SolanaContextType {
  CreateTokenMint?: (tokenName: string, tokenSymbol: string, tokenUri: string) => Promise<string>
}

const SolanaContext = createContext<SolanaContextType>({
});

export const useSolana = () => useContext(SolanaContext);

interface SolanaProviderProps {
  children: ReactNode;
  wallet: PhantomWalletAdapter;
}

export const SolanaProvider = ({ children }: SolanaProviderProps) => {


  // const { connection } = useConnection();
  const programId = new web3.PublicKey("A7sBBSngzEZTsCPCffHDbeXDJ54uJWkwdEsskmn2YBGo");

  const program = new Program(drc_token_json as any, 
    programId, getProvider()
    // {connection}
  )
  



  const CreateTokenMint = async (tokenName: string, tokenSymbol: string, tokenUri: string) => {
    const mintAccount = web3.Keypair.generate();
    const [metadataAddress] = await web3.PublicKey.findProgramAddressSync(
      [
        // new Uint8Array([109, 101, 116, 97, 100, 97, 116, 97]),
        global.Buffer.from("metadata"),
        TOKEN_METADATA_PROGRAM_ID.toBuffer(),
        mintAccount.publicKey.toBuffer(),
      ],
      TOKEN_METADATA_PROGRAM_ID
    );
    const TOKEN_PROGRAM_ID = new web3.PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA');
    //@ts-ignore
    const response = await window.solana.connect();

    if (!response) {
      throw Error("No public key found")
    }

    const transaction = await program.methods.createToken(tokenName = tokenName, tokenSymbol = tokenSymbol, tokenUri = tokenUri).accounts({
      payer: response.publicKey,
      mintAccount: mintAccount.publicKey,
      metadataAccount: metadataAddress,
      tokenProgram: TOKEN_PROGRAM_ID,
      tokenMetadataProgram: TOKEN_METADATA_PROGRAM_ID,
      systemProgram: web3.SystemProgram.programId,
      rent: web3.SYSVAR_RENT_PUBKEY
    })
      .signers([mintAccount])
      .rpc();

      return transaction
  }


  return (
    <SolanaContext.Provider
      value={{
        CreateTokenMint
      }}
    >
      {children}
    </SolanaContext.Provider>
  );
};
