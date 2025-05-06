import NottyTerminalFooter from "./components/landingPage/footer";
import Header from "./components/landingPage/header";
import CoinPage from "./pages/coinPage";
import LandingPage from "./pages/landingPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useAnchorWallet, useConnection } from "@solana/wallet-adapter-react";
import {
	ConnectionProvider,
	WalletProvider,
} from "@solana/wallet-adapter-react";
import {
	WalletModalProvider,
	WalletMultiButton,
} from "@solana/wallet-adapter-react-ui";
import { PhantomWalletAdapter } from "@solana/wallet-adapter-phantom";
import { clusterApiUrl } from "@solana/web3.js";
import "@solana/wallet-adapter-react-ui/styles.css";
function App() {
	const endpoint = clusterApiUrl("devnet");
	const wallets = [new PhantomWalletAdapter()];
	return (
		<ConnectionProvider endpoint={endpoint}>
			<WalletProvider wallets={wallets} autoConnect={false}>
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
						</Routes>
						<NottyTerminalFooter />
					</Router>
				</WalletModalProvider>
			</WalletProvider>
		</ConnectionProvider>
	);
}

export default App;
