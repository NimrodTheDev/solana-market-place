import { Copy, Info } from "lucide-react";
import { useState } from "react";

export default function CryptoTokenDetails() {
	const [copySuccess, setCopySuccess] = useState(false);

	const handleCopyClick = () => {
		navigator.clipboard
			.writeText("9XhQz4yMFBQn2RjkzPt9XbFHEtqT5UvDwpm3LFQZf4rY")
			.then(() => {
				setCopySuccess(true);
				setTimeout(() => setCopySuccess(false), 2000);
			});
	};

	return (
		<div className='bg-gray-900 text-white min-h-screen p-6'>
			<div className='max-w-4xl mx-auto'>
				{/* Creator row */}
				<div className='flex justify-between items-center mb-6'>
					<div className='text-gray-300 text-lg'>Creator</div>
					<div className='flex items-center'>
						<span className='text-yellow-400 mr-2'>👑</span>
						<a href='#' className='text-blue-400 underline text-lg'>
							Specialdev
						</a>
					</div>
				</div>

				{/* Time Launched row */}
				<div className='flex justify-between items-center mb-6'>
					<div className='text-gray-300 text-lg'>Time Launched:</div>
					<div className='text-white text-lg'>3 hours ago</div>
				</div>

				{/* Marketcap row */}
				<div className='flex justify-between items-center mb-6'>
					<div className='text-gray-300 text-lg'>Marketcap:</div>
					<div className='text-white text-lg'>$5,700</div>
				</div>

				{/* DRS row */}
				<div className='flex justify-between items-center mb-6'>
					<div className='text-gray-300 text-lg'>DRS:</div>
					<div className='text-white text-lg'>500</div>
				</div>

				{/* Contract Address row */}
				<div className='flex justify-between items-center mb-6'>
					<div className='text-gray-300 text-lg'>Contract Address</div>
					<div className='flex items-center'>
						<span className='text-white text-lg mr-2 font-mono'>
							9XhQz4yMFBQn2RjkzPt9XbFHEtqT5UvDwpm3LFQZf4rY
						</span>
						<button
							onClick={handleCopyClick}
							className='text-gray-400 hover:text-white transition-colors'
							title='Copy to clipboard'
						>
							<Copy size={20} />
						</button>
						{copySuccess && (
							<span className='text-green-500 ml-2 text-sm'>Copied!</span>
						)}
					</div>
				</div>

				{/* Bonding curve progress */}
				<div className='mb-6'>
					<div className='flex justify-between items-center mb-2'>
						<div className='text-gray-300 text-lg'>Bonding curve progress</div>
						<div className='flex items-center'>
							<span className='text-white text-lg mr-2'>60%</span>
							<Info size={16} className='text-gray-400' />
						</div>
					</div>
					<div className='relative h-4 bg-gray-800 rounded-full'>
						<div
							className='absolute h-full bg-gradient-to-r from-purple-500 to-blue-400 rounded-full'
							style={{ width: "60%" }}
						></div>
					</div>
					<div className='flex justify-between mt-1'>
						<span className='text-gray-400 text-sm'>short note below</span>
						<span className='text-gray-400 text-sm'>link text</span>
					</div>
				</div>

				{/* Total Supply row */}
				<div className='flex justify-between items-center mb-6'>
					<div className='text-gray-300 text-lg'>Total Supply</div>
					<div className='text-white text-lg'>1,000,000 $CC</div>
				</div>

				{/* Website row */}
				<div className='flex justify-between items-center mb-6'>
					<div className='text-gray-300 text-lg'>Website</div>
					<div className='text-lg'>
						<a
							href='https://cybercatcoin.com'
							className='text-blue-400 underline'
						>
							cybercatcoin.com
						</a>
					</div>
				</div>
			</div>
		</div>
	);
}
