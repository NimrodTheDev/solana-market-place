import { useState } from "react";
import { Repeat } from "lucide-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";

export default function CryptoTradingWidget({}: {coinData: any}) {
	const [amount, setAmount] = useState("0.00");
	const [activeTab, setActiveTab] = useState("buy");

	return (
		<div className='bg-gray-900 p-6 rounded-lg max-w-md mx-auto'>
			{/* Buy/Sell Tabs */}
			<div className='flex gap-4 mb-6'>
				<button
					className={`py-3 px-8 rounded-lg text-white font-medium ${
						activeTab === "buy"
							? "bg-purple-500 hover:bg-purple-600"
							: "bg-gray-800 hover:bg-gray-700"
					}`}
					onClick={() => setActiveTab("buy")}
				>
					Buy
				</button>
				<button
					className={`py-3 px-8 rounded-lg text-white font-medium ${
						activeTab === "sell"
							? "bg-purple-500 hover:bg-purple-600"
							: "bg-gray-800 hover:bg-gray-700"
					}`}
					onClick={() => setActiveTab("sell")}
				>
					Sell
				</button>
			</div>

			{/* Amount Input */}
			<div className='relative mb-3'>
				<input
					type='text'
					value={amount}
					onChange={(e) => setAmount(e.target.value)}
					className='w-full bg-gray-800 border border-gray-700 rounded-lg p-4 text-white text-xl focus:outline-none focus:ring-2 focus:ring-purple-500'
				/>
				<div className='absolute right-4 top-1/2 -translate-y-1/2'>
					<Repeat size={20} className='text-purple-400' />
				</div>
			</div>

			{/* Currency Switch */}
			<div className='text-right mb-6'>
				<button className='text-gray-300 hover:text-white text-sm'>
					Switch to $CPC
				</button>
			</div>

			{/* Connect Wallet Button */}
			{/* <button className='w-full bg-purple-500 hover:bg-purple-600 text-white py-4 px-6 rounded-lg font-medium transition-colors'>
				Connect Wallet to trade
			</button> */}
			<WalletMultiButton />
		</div>
	);
}
