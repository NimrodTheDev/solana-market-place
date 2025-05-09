import { Twitter, Globe } from "lucide-react";
import { useState } from "react";
import { useSolana } from "../../solanaClient";

export default function CoinProfile() {
	const [fireCount, setFireCount] = useState(500);

	const handleFireClick = () => {
		setFireCount((prevCount) => prevCount + 1);
	};

	const {CreateTokenMint} = useSolana()
	return (
		<div className='bg-gray-900 text-white min-h-screen p-4'>
			<div className='max-w-2xl mx-auto'>
				{/* Header */}
				<div className='flex justify-between items-center mb-6'>
					<h1 className='text-4xl font-bold text-center flex-grow'>
						Cyber Punk Cat
					</h1>
					<button
						onClick={handleFireClick}
						className='flex items-center gap-2 text-orange-500 hover:text-orange-400 transition-colors'
					>
						<span className='text-2xl'>🔥</span>
						<span>{fireCount}</span>
					</button>
				</div>

				{/* Cat Image */}
				<div className='mb-8'>
					<div className='rounded-lg overflow-hidden border-2 border-gray-700 mx-auto max-w-md'>
						<img
							src='/api/placeholder/400/320'
							alt='Cyberpunk Cat Family'
							className='w-full h-full object-cover'
						/>
					</div>
				</div>

				{/* Social Links */}
				<div className='flex justify-center gap-4 mb-8'>
					<button className='p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-colors'>
						<Twitter size={20} />
					</button>
					<button className='p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-colors'>
						<Globe size={20} />
					</button>
					<button className='p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-colors'>
						<svg
							width='20'
							height='20'
							viewBox='0 0 24 24'
							fill='none'
							xmlns='http://www.w3.org/2000/svg'
						>
							<path
								d='M19.73 4.27a10 10 0 0 0-14.15 0c-3.9 3.91-3.9 10.24 0 14.14 3.91 3.91 10.24 3.91 14.15 0 3.9-3.9 3.9-10.23 0-14.14zM7.89 7.89a6 6 0 0 1 8.3-.18l.12.1.13.12a6 6 0 0 1-8.51 8.51l-.04-.04a6 6 0 0 1 0-8.51z'
								fill='currentColor'
							/>
							<path
								d='M16.27 16.27a6 6 0 0 0 0-8.54 6 6 0 0 0-8.54 0 6 6 0 0 0 0 8.54 6 6 0 0 0 8.54 0zM12 10.8a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4z'
								fill='currentColor'
							/>
						</svg>
					</button>
				</div>
				<button onClick={()=>CreateTokenMint && CreateTokenMint("test", "TSB", "nourl")}>
					Mint test
				</button>
				{/* About Section */}
				<div className='mb-6'>
					<h2 className='text-2xl font-bold mb-4'>About CyberPunk Cat</h2>
					<p className='text-gray-300 leading-relaxed'>
						Lorem ipsum dictum faucibus ullamcorper amet nulla adipiscing
						rhoncus sed dui at tellus rutrum est id diam id sit pharetra nibh
						feugiat egestas dolor enim mattis mi amet id fermentum risus eu
						pulvinar lectus massa erat sapien pellentesque elementum at in nec
						molestie vitae feugiat nisi turpis bibendum mauris ac proin viverra
						vel varius sollicitudin in tellus vulputate erat non.
					</p>
				</div>
			</div>
		</div>
	);
}
