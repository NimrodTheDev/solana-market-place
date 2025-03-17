import React, { useState } from "react";
import { useWallet } from "../../helper/connect";
import { createToken } from "../../helper/createToken";
import { listToken } from "../../helper/listToken";
import { buyToken } from "../../helper/buyToken";

export default function Home() {
	const { wallet, connectWallet } = useWallet();
	const [tokenMint, setTokenMint] = useState("");
	const [price, setPrice] = useState("");
	const [amount, setAmount] = useState("");

	return (
		<div>
			<h1>Solana Marketplace</h1>
			{wallet ? (
				<p>Connected: {wallet.toString()}</p>
			) : (
				<button onClick={connectWallet}>Connect Wallet</button>
			)}

			<button onClick={() => createToken(wallet)}>Create Token</button>

			<h2>List Token</h2>
			<input
				placeholder='Token Mint Address'
				onChange={(e) => setTokenMint(e.target.value)}
			/>
			<input
				placeholder='Price (SOL)'
				type='number'
				onChange={(e) => setPrice(e.target.value)}
			/>
			<input
				placeholder='Amount'
				type='number'
				onChange={(e) => setAmount(e.target.value)}
			/>
			<button
				onClick={() =>
					listToken(wallet, tokenMint, parseFloat(price), parseInt(amount))
				}
			>
				List Token
			</button>

			<h2>Buy Token</h2>
			<button
				onClick={() =>
					buyToken(
						wallet,
						"SELLER_PUBKEY",
						tokenMint,
						parseFloat(price),
						parseInt(amount)
					)
				}
			>
				Buy Token
			</button>
		</div>
	);
}
