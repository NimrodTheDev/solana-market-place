import { useWallet } from "@solana/wallet-adapter-react";
import NFTCollection from "../components/landingPage/collection";
import FeaturesSection from "../components/landingPage/features";
import Hero from "../components/landingPage/hero";
import HowItWorks from "../components/landingPage/howItWorks";
import OnboardingCard from "../components/landingPage/onboardingCard";
import { useEffect } from "react";
import axios from "axios";

const LandingPage = () => {
	const wallet = useWallet()
	// uploadFile()
	useEffect(()=>{
		const connectWallet = async () => {
			//@ts-ignore
			// const response = await window?.solana?.connect();

		// if (!response) {
		// //   throw Error("No public key found")
		// return
		// }
		console.log(wallet.publicKey?.toBase58())
		axios.post(`https://solana-market-place-backend.onrender.com/api/connect_wallet/`, {
			wallet_address: wallet.publicKey?.toBase58() || ""
		},{
			headers: {
				"Content-Type": "application/json",
			}
		})
		.then((res)=>{
			console.log(res.data)
		})
		.catch((err)=>{
			console.log(err)
		})
		}
		connectWallet()
	}, [])
	return (
		<div>
			<Hero />
			<NFTCollection />
			<FeaturesSection />
			<HowItWorks />
			<OnboardingCard />
		</div>
	);
};

export default LandingPage;
