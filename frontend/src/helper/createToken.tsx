import { PublicKey, Transaction, SystemProgram } from "@solana/web3.js";
import { sendTransaction, connection } from "./solana";

const PROGRAM_ID = new PublicKey("YOUR_PROGRAM_ID");

export const createToken = async (wallet: any) => {
	if (!wallet) return alert("Connect wallet first!");

	const transaction = new Transaction().add(
		SystemProgram.createAccount({
			fromPubkey: wallet.publicKey,
			newAccountPubkey: PROGRAM_ID,
			lamports: await connection.getMinimumBalanceForRentExemption(165),
			space: 165,
			programId: PROGRAM_ID,
		})
	);

	const signature = await sendTransaction(transaction, wallet);
	console.log("Token Created:", signature);
};
