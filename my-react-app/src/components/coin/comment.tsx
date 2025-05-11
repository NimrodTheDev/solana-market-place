import { useState } from "react";
import { Send } from "lucide-react";


interface CoinData {
	address: string;
	created_at: string;
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


interface CoinCommentsProps {
	coinData: CoinData;
}

export default function CoinComments({ coinData }: CoinCommentsProps) {
	const [newComment, setNewComment] = useState("");

	const comments = [
		{ id: 1, username: "Specialdev", text: "Cyberpunkcat is amazing 🔥" },
		{ id: 2, username: "Specialdev", text: "Cyberpunkcat is amazing 🔥" },
		{ id: 3, username: "Specialdev", text: "Cyberpunkcat is amazing 🔥" },
		{ id: 4, username: "Specialdev", text: "Cyberpunkcat is amazing 🔥" },
		{ id: 5, username: "Specialdev", text: "Cyberpunkcat is amazing 🔥" },
	];

	const handleSubmitComment = () => {
		if (newComment.trim()) {
			// Handle new comment logic here
			console.log("New comment:", newComment);
			setNewComment("");
		}
	};

	return (
		<div className='bg-gray-800 p-4 rounded-lg'>
			<h2 className='text-xl font-bold mb-4'>Comments</h2>
			<div className='space-y-4'>
				<p className='text-gray-400'>Comments for {coinData.name}</p>
				{/* Comments section */}
				<div>
					{comments.map((comment) => (
						<div key={comment.id} className='border-t border-gray-700 py-4'>
							<div className='flex items-center mb-2'>
								<span className='text-yellow-400 mr-2'>👋</span>
								<a className='text-gray-300 underline cursor-pointer'>
									{comment.username}
								</a>
							</div>
							<p>{comment.text}</p>
						</div>
					))}
				</div>

				{/* Comment input */}
				<div className='mt-4'>
					<div className='flex items-center border border-gray-700 rounded-lg overflow-hidden'>
						<input
							type='text'
							value={newComment}
							onChange={(e) => setNewComment(e.target.value)}
							placeholder='Add a comment...'
							className='flex-1 bg-gray-800 p-3 outline-none'
							onKeyPress={(e) => {
								if (e.key === "Enter") {
									handleSubmitComment();
								}
							}}
						/>
						<button
							onClick={handleSubmitComment}
							className='bg-blue-600 hover:bg-blue-700 p-3 text-white'
						>
							<Send className='w-5 h-5' />
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}
