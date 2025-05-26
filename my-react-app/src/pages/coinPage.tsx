import { useEffect, useState } from "react";
// import HoldersAnalytics from "../components/coin/coinHolder";
import CoinProfile from "../components/coin/coinProfile";
// import CoinComments from "../components/coin/comment";
import CryptoTokenDetails from "../components/coin/cryptoTokenDetail";
// import SimilarCoins from "../components/coin/similiarCoin";
// import CryptoTradingWidget from "../components/coin/tradingWidget";
import { useParams } from "react-router-dom";
import axios from "axios";
// Add the type definition
interface CoinData {
	address: string;
	created_at: string;
	score: number;
	creator: string;
	creator_display_name: string;
	current_price: string;
	description: string | null;
	image_url: string;
	market_cap: number;
	name: string;
	telegram: string | null;
	ticker: string;
	total_held: number;
	total_supply: string;
	twitter: string | null;
	website: string | null;
}

export default function CoinPage() {
	const [coinData, setCoinData] = useState<CoinData | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const { id } = useParams();


	useEffect(() => {
		const fetchCoinData = async () => {
			try {
				setLoading(true);
				const response = await axios.get<CoinData>(`https://solana-market-place-backend.onrender.com/api/coins/${id}`);
				setCoinData(response.data);

				setError(null);
			} catch (e) {
				setError("Failed to fetch coin data");
				console.error("Error fetching coin data:", e);
			} finally {
				setLoading(false);
			}
		};

		fetchCoinData();
	}, [id]);

	if (loading) {
		return <div className="bg-gray-900 text-white min-h-screen p-4">Loading...</div>;
	}

	if (error || !coinData) {
		return <div className="bg-gray-900 text-white min-h-screen p-4">{error || "No data available"}</div>;
	}

	return (

		<div className=" bg-custom-dark-blue items-center ">
			<div className='bg-custom-dark-blue flex flex-col gap-2 w-4/5 mx-auto p-4 text-white'>
				<div className='grid lg:grid-cols-custom-2-1 gap-2'>
					<div className='flex flex-col gap-2 w-full'>
						<CoinProfile coinData={coinData} />
						<CryptoTokenDetails coinData={coinData} />
						{/* <CoinComments coinData={coinData} /> */}
					</div>
					<div className='flex flex-col gap-2'>
						{/* <CryptoTradingWidget coinData={coinData} /> */}
						{/* <HoldersAnalytics coinData={coinData} /> */}
					</div>
				</div>
				{/* <SimilarCoins coinData={coinData} /> */}
			</div>
		</div>

	);
}
