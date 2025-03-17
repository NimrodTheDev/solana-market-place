import {
	PublicKey,
	Transaction,
	TransactionInstruction,
} from "@solana/web3.js";
import { sendTransaction, connection } from "./solana";
import { Buffer } from "buffer";

const PROGRAM_ID = new PublicKey("YOUR_PROGRAM_ID");

export const buyToken = async (
	wallet: any,
	seller: string,
	tokenMint: string,
	price: number,
	amount: number
) => {
	if (!wallet) return alert("Connect wallet first!");

	const instructionData = Buffer.concat([
		Buffer.from([2]), // Instruction for buying
		Buffer.from(new Uint8Array(new BigUint64Array([BigInt(price)]).buffer)),
		Buffer.from(new Uint8Array(new BigUint64Array([BigInt(amount)]).buffer)),
	]);

	const transaction = new Transaction().add(
		new TransactionInstruction({
			keys: [
				{ pubkey: wallet.publicKey, isSigner: true, isWritable: true },
				{ pubkey: new PublicKey(seller), isSigner: false, isWritable: true },
				{ pubkey: new PublicKey(tokenMint), isSigner: false, isWritable: true },
				{ pubkey: PROGRAM_ID, isSigner: false, isWritable: true },
			],
			programId: PROGRAM_ID,
			data: instructionData,
		})
	);

	const signature = await sendTransaction(transaction, wallet);
	console.log("Token Purchased:", signature);
};
