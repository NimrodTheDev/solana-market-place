import { useState, useEffect } from "react";
import { PublicKey } from "@solana/web3.js";

declare global {
	interface Window {
		solana?: any;
	}
}

export const useWallet = () => {
	const [wallet, setWallet] = useState<PublicKey | null>(null);

	useEffect(() => {
		if (window.solana && window.solana.isPhantom) {
			window.solana.connect({ onlyIfTrusted: true }).then((res: any) => {
				setWallet(res.publicKey);
			});
		}
	}, []);

	const connectWallet = async () => {
		if (window.solana) {
			const response = await window.solana.connect();
			setWallet(response.publicKey);
		} else {
			alert("Please install Phantom Wallet!");
		}
	};

	return { wallet, connectWallet };
};
