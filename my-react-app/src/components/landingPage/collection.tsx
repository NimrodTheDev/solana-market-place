import { useState } from "react";
import { Link } from "react-router-dom";

// Define TypeScript interfaces
interface NFT {
	id: number;
	title: string;
	description: string;
	marketCap: string;
	drs: number;
}

interface NFTCardProps {
	nft: NFT;
}

export default function NFTCollection() {
	const [nfts] = useState<NFT[]>([
		{
			id: 1,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
		{
			id: 2,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
		{
			id: 3,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
		{
			id: 4,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
		{
			id: 5,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
		{
			id: 6,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
		{
			id: 7,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
		{
			id: 8,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			marketCap: "$5K",
			drs: 500,
		},
	]);

	return (
		<div className='bg-black min-h-screen p-4 sm:p-8'>
			<div className='max-w-7xl mx-auto'>
				<div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6'>
					{nfts.map((nft) => (
						<NFTCard key={nft.id} nft={nft} />
					))}
				</div>
				<div className='flex justify-center mt-6'>
					<button className='text-white'>
						<svg
							className='w-8 h-8'
							fill='none'
							stroke='currentColor'
							viewBox='0 0 24 24'
						>
							<path
								strokeLinecap='round'
								strokeLinejoin='round'
								strokeWidth='2'
								d='M19 9l-7 7-7-7'
							/>
						</svg>
					</button>
				</div>
			</div>
		</div>
	);
}

export function NFTCard({ nft }: NFTCardProps) {
	return (
		<div className='bg-gray-900 rounded-lg overflow-hidden border border-gray-800'>
			<div className='relative pb-[100%]'>
				<img
					src='/api/placeholder/400/320'
					alt='NFT Cat'
					className='absolute inset-0 w-full h-full object-cover'
				/>
			</div>

			<div className='p-4'>
				<h3 className='text-white text-xl font-bold mb-2'>{nft.title}</h3>
				<p className='text-gray-400 text-sm mb-4'>{nft.description}</p>

				<div className='flex justify-between items-center mb-4'>
					<div>
						<p className='text-purple-400 text-xs font-medium'>MARKET CAP:</p>
						<p className='text-purple-400 font-medium'>{nft.marketCap}</p>
					</div>
					<div className='text-right'>
						<p className='text-gray-500 text-xs'>DRS:</p>
						<p className='text-gray-400'>{nft.drs}</p>
					</div>
				</div>

				<Link
					to={`/coin/${nft.id}`}
					className='w-full bg-purple-500 hover:bg-purple-600 text-white py-2 px-4 rounded flex items-center justify-center gap-1 transition-colors'
				>
					View Details
					<svg
						className='w-4 h-4'
						fill='none'
						stroke='currentColor'
						viewBox='0 0 24 24'
					>
						<path
							strokeLinecap='round'
							strokeLinejoin='round'
							strokeWidth='2'
							d='M14 5l7 7m0 0l-7 7m7-7H3'
						/>
					</svg>
				</Link>
			</div>
		</div>
	);
}
