import { useState } from "react";
import { MessageSquare, Send } from "lucide-react";

export default function CoinComments() {
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
		<div className='bg-gray-900 text-white p-4 w-full max-w-3xl mx-auto'>
			{/* Header Section */}
			<div className='flex items-center mb-6'>
				<div className='w-16 h-16 rounded-lg overflow-hidden mr-4'>
					<img
						src='/api/placeholder/80/80'
						alt='CyberPunkCat'
						className='w-full h-full object-cover'
					/>
				</div>
				<div>
					<h2 className='text-2xl font-bold'>CyberPunkCat</h2>
					<div className='flex items-center text-gray-400'>
						<span>{comments.length} comments</span>
					</div>
				</div>
			</div>

			{/* Leave a comment prompt */}
			<div className='mb-4 text-lg'>Leave a comment below</div>

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
	);
}
