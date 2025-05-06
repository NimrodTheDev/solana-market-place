import HoldersAnalytics from "../components/coin/coinHolder";
import CoinProfile from "../components/coin/coinProfile";
import CoinComments from "../components/coin/comment";
import CryptoTokenDetails from "../components/coin/cryptoTokenDetail";
import SimilarCoins from "../components/coin/similiarCoin";
import CryptoTradingWidget from "../components/coin/tradingWidget";

const CoinPage = () => {
	return (
		<div className='bg-gray-900 flex flex-col gap-2'>
			<div className='flex gap-2'>
				<div className='flex flex-col gap-2 w-full'>
					<CoinProfile />
					<CryptoTokenDetails />
					<CoinComments />
				</div>
				<div className='flex flex-col gap-2'>
					<CryptoTradingWidget />
					<HoldersAnalytics />
				</div>
			</div>
			<SimilarCoins />
		</div>
	);
};

export default CoinPage;
