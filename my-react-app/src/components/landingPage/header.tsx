import { useState } from "react";
import { Bell, MessageSquare, Menu, X } from "lucide-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";

export default function Header() {
	const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

	return (
		<header className='bg-[#0e0f14] text-white px-4 py-3 shadow-md'>
			<div className='max-w-7xl mx-auto flex items-center justify-between'>
				{/* Logo and Toggle */}
				<div className='flex items-center justify-between w-full md:w-auto'>
					<span className='text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent'>
						Notty Terminal
					</span>

					{/* Mobile toggle */}
					<button
						className='md:hidden text-gray-300'
						onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
					>
						{mobileMenuOpen ? (
							<X className='w-6 h-6' />
						) : (
							<Menu className='w-6 h-6' />
						)}
					</button>
				</div>

				{/* Navigation links */}
				<nav
					className={`${
						mobileMenuOpen ? "block" : "hidden"
					} md:flex md:items-center gap-6 text-sm text-gray-300 mt-4 md:mt-0`}
				>
					<a href='#' className='block md:inline hover:text-white'>
						Wallet
					</a>
					<a href='#' className='block md:inline hover:text-white'>
						AI Tools
					</a>
					<a href='#' className='block md:inline hover:text-white'>
						On Chain News
					</a>
					<a href='#' className='block md:inline hover:text-white'>
						DRS System
					</a>
					<a href='#' className='block md:inline hover:text-white'>
						Talent Pool
					</a>
				</nav>

				{/* Right icons + button */}
				<div className='hidden md:flex items-center gap-4'>
					<div className='relative'>
						<Bell className='w-5 h-5 text-gray-300 hover:text-white' />
						<span className='absolute top-0 right-0 h-2 w-2 rounded-full bg-red-500' />
					</div>
					<MessageSquare className='w-5 h-5 text-gray-300 hover:text-white' />
					{/* <button className='bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-md text-sm flex items-center gap-2'>
						Connect Wallet
						<svg
							xmlns='http://www.w3.org/2000/svg'
							fill='none'
							viewBox='0 0 24 24'
							stroke='currentColor'
							className='w-4 h-4'
						>
							<path
								strokeLinecap='round'
								strokeLinejoin='round'
								strokeWidth={2}
								d='M4 7h16M4 12h8m-8 5h16'
							/>
						</svg>
					</button> */}
					<WalletMultiButton />
				</div>
			</div>

			{/* Right icons + button (mobile view) */}
			{mobileMenuOpen && (
				<div className='md:hidden mt-4 flex flex-col gap-3 items-start'>
					<div className='flex items-center gap-4'>
						<div className='relative'>
							<Bell className='w-5 h-5 text-gray-300 hover:text-white' />
							<span className='absolute top-0 right-0 h-2 w-2 rounded-full bg-red-500' />
						</div>
						<MessageSquare className='w-5 h-5 text-gray-300 hover:text-white' />
					</div>
					<button className='bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-md text-sm flex items-center gap-2'>
						Connect Wallet
						<svg
							xmlns='http://www.w3.org/2000/svg'
							fill='none'
							viewBox='0 0 24 24'
							stroke='currentColor'
							className='w-4 h-4'
						>
							<path
								strokeLinecap='round'
								strokeLinejoin='round'
								strokeWidth={2}
								d='M4 7h16M4 12h8m-8 5h16'
							/>
						</svg>
					</button>
				</div>
			)}
		</header>
	);
}
