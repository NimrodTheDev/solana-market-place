import { NFTCard } from "../landingPage/collection";

export default function SimilarCoins() {
	const coins = [
		{
			id: 1,
			title: "Cyber Punk Cat",
			description:
				"A digital masterpiece featuring a cybernetic feline in a neon-lit future.",
			image: "/api/placeholder/320/240",
			marketCap: "$5K",
			drs: 500,
			created: "2/02/2025",
			artist: "NeonArtist",
			isPurchasable: true,
		},
		{
			id: 2,
			title: "Cyber Punk Cat",
			description: "Inspired by the iconic digital rain from the matrix movie",
			image: "/api/placeholder/320/240",
			marketCap: "$5K",
			drs: 500,
			created: "2/02/2025",
			artist: "NeonArtist",
			isPurchasable: false,
		},
		{
			id: 3,
			title: "Cyber Punk Cat",
			description: "Humorous take on artificial intelligence and robots",
			image: "/api/placeholder/320/240",
			marketCap: "$5K",
			drs: 500,
			created: "2/02/2025",
			artist: "NeonArtist",
			isPurchasable: false,
		},
		{
			id: 4,
			title: "Cyber Punk Cat",
			description: "Humorous take on artificial intelligence and robots",
			image: "/api/placeholder/320/240",
			marketCap: "$5K",
			drs: 500,
			created: "2/02/2025",
			artist: "NeonArtist",
			isPurchasable: false,
		},
	];

	return (
		<div className='bg-black text-white min-h-screen p-6'>
			<h1 className='text-2xl font-bold mb-6'>Similar Coins</h1>

			<div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2'>
				{coins.map((coin) => (
					<NFTCard key={coin.id} nft={coin} />
				))}
			</div>
		</div>
	);
}
