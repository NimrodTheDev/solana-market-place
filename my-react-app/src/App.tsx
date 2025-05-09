import NottyTerminalFooter from "./components/landingPage/footer";
import Header from "./components/landingPage/header";
import CoinPage from "./pages/coinPage";
import LandingPage from "./pages/landingPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CreateCoin from "./pages/CreateCoin";

import {
	ConnectionProvider,
	WalletProvider,
} from "@solana/wallet-adapter-react";
import { WalletModalProvider } from "@solana/wallet-adapter-react-ui";
import { PhantomWalletAdapter } from "@solana/wallet-adapter-phantom";
import { clusterApiUrl } from "@solana/web3.js";
import "@solana/wallet-adapter-react-ui/styles.css";
import { SolanaProvider } from "./solanaClient";
function App() {
	const endpoint = clusterApiUrl("devnet");
	const wallets = [new PhantomWalletAdapter()];
	return (
		<ConnectionProvider endpoint={endpoint}>
			<WalletProvider wallets={wallets} autoConnect={false}>
				<SolanaProvider wallet={wallets[0]}>
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
							</Routes>
							<NottyTerminalFooter />
						</Router>
					</WalletModalProvider>
				</SolanaProvider>
			</WalletProvider>
		</ConnectionProvider>
	);
}

export default App;
