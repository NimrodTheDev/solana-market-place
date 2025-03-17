import {
	PublicKey,
	Transaction,
	TransactionInstruction,
} from "@solana/web3.js";
import { sendTransaction, connection } from "./solana";
import { Buffer } from "buffer";

const PROGRAM_ID = new PublicKey("YOUR_PROGRAM_ID");

export const listToken = async (
	wallet: any,
	tokenMint: string,
	price: number,
	amount: number
) => {
	if (!wallet) return alert("Connect wallet first!");

	const instructionData = Buffer.concat([
		Buffer.from([1]), // Instruction for listing
		new PublicKey(tokenMint).toBuffer(),
		Buffer.from(new Uint8Array(new BigUint64Array([BigInt(price)]).buffer)),
		Buffer.from(new Uint8Array(new BigUint64Array([BigInt(amount)]).buffer)),
	]);

	const transaction = new Transaction().add(
		new TransactionInstruction({
			keys: [
				{ pubkey: wallet.publicKey, isSigner: true, isWritable: true },
				{ pubkey: PROGRAM_ID, isSigner: false, isWritable: true },
			],
			programId: PROGRAM_ID,
			data: instructionData,
		})
	);

	const signature = await sendTransaction(transaction, wallet);
	console.log("Token Listed:", signature);
};
