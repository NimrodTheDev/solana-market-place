export default function Hero() {
	return (
		<div className='bg-black min-h-screen flex items-center justify-center relative overflow-hidden'>
			{/* Background decorative elements */}
			<div className='absolute inset-0 overflow-hidden'>
				{/* Purple icon decorations */}
				<div className='absolute top-20 left-24 text-purple-500 opacity-30 text-6xl'>
					⚡
				</div>
				<div className='absolute top-40 right-32 text-purple-500 opacity-30 text-7xl'>
					♾️
				</div>
				<div className='absolute bottom-24 left-40 text-purple-500 opacity-30 text-6xl'>
					♦️
				</div>
				<div className='absolute top-60 left-96 text-purple-500 opacity-30 text-5xl'>
					⚛️
				</div>
				<div className='absolute bottom-40 right-48 text-purple-500 opacity-30 text-6xl'>
					🔮
				</div>
				<div className='absolute bottom-32 left-32 text-purple-500 opacity-30 text-5xl'>
					🌐
				</div>
			</div>

			{/* Main content */}
			<div className='relative z-10 text-center px-6 py-12 max-w-4xl'>
				{/* Label */}
				<div className='inline-block mb-6 px-4 py-1 rounded-full bg-gray-800 text-purple-300 text-sm font-medium'>
					Web3 Launchpad
				</div>

				{/* Headline */}
				<h1 className='text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-purple-200 text-transparent bg-clip-text'>
					The Ultimate Platform For
					<br />
					Web3 Talent & Projects
				</h1>

				{/* Subheading */}
				<p className='text-gray-300 text-lg mb-10 max-w-2xl mx-auto'>
					Connect with top Web3 talent, launch your projects, and build the
					future of decentralized applications in one seamless ecosystem.
				</p>

				{/* CTA Buttons */}
				<div className='flex flex-col sm:flex-row gap-4 justify-center'>
					<button className='px-6 py-3 bg-purple-500 hover:bg-purple-600 rounded-md text-white font-medium flex items-center justify-center gap-2 transition-colors'>
						Launch Coin <span className='ml-1'>↗</span>
					</button>
					<button className='px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-md text-white font-medium transition-colors'>
						Join Talent Pool
					</button>
				</div>
			</div>
		</div>
	);
}
