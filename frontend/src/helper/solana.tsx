import {
	Connection,
	PublicKey,
	Transaction,
	clusterApiUrl,
} from "@solana/web3.js";

export const connection = new Connection(clusterApiUrl("devnet"), "confirmed");

export const sendTransaction = async (
	transaction: Transaction,
	wallet: any
) => {
	try {
		transaction.feePayer = wallet.publicKey;
		transaction.recentBlockhash = (
			await connection.getLatestBlockhash()
		).blockhash;

		const signedTransaction = await wallet.signTransaction(transaction);
		const signature = await connection.sendRawTransaction(
			signedTransaction.serialize()
		);

		await connection.confirmTransaction(signature, "confirmed");
		return signature;
	} catch (error) {
		console.error("Transaction Error:", error);
	}
};
