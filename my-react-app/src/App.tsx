import NottyTerminalFooter from "./components/landingPage/footer";
import Header from "./components/landingPage/header";
import CoinPage from "./pages/coinPage";
import LandingPage from "./pages/landingPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CreateCoin from "./pages/CreateCoin";
import 
{
	ConnectionProvider,
	WalletProvider,
} from "@solana/wallet-adapter-react";
import { WalletModalProvider } from "@solana/wallet-adapter-react-ui";
import { PhantomWalletAdapter } from "@solana/wallet-adapter-phantom";
import { clusterApiUrl } from "@solana/web3.js";
import "@solana/wallet-adapter-react-ui/styles.css";
import Loginconnect from "./solanaClient/Loginconnect";
// import { SolanaProvider } from "./solanaClient";
//import { SolanaProvider } from "./solanaClient";
// import { SolanaProvider } from "./solanaClient";
import { useEffect } from "react";
import axios from "axios";
// import { uploadFile } from "./solanaClient/usePinta";
function App() {
	const endpoint = clusterApiUrl("devnet");
	const wallets = [new PhantomWalletAdapter()];
	// uploadFile()
	useEffect(()=>{
		const connectWallet = async () => {
			//@ts-ignore
			const response = await window.solana.connect();

		if (!response) {
		  throw Error("No public key found")
		}
		console.log(response.publicKey?.toBase58())
		axios.post(`https://solana-market-place-backend.onrender.com/api/connect_wallet/`, {
			wallet_address: response.publicKey?.toBase58() || ""
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
		<ConnectionProvider endpoint={endpoint}>
			<WalletProvider wallets={wallets} autoConnect={false}>
				{/* <SolanaProvider wallet={wallets[0]}> */}
				<WalletModalProvider>
					<Router>
						<Header />
						<Routes>
							<Route
								path='/'
								element={
									<div>
										<LandingPage />
									</div>
								}
							/>
							<Route path='/coin/:id' element={<CoinPage />} />
							<Route path='*' element={<div>Not found</div>} />
							<Route path='/coin/create' element={< CreateCoin />} />
							<Route path="/login" element={<Loginconnect/>} />
						</Routes>
						<NottyTerminalFooter />
					</Router>
				</WalletModalProvider>
				{/* </SolanaProvider> */}
			</WalletProvider>
		</ConnectionProvider>
	);
}

export default App;
