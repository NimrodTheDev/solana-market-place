import { ArrowRight, Wallet } from "lucide-react";

export default function OnboardingCard() {
	return (
		<div className='flex justify-center items-center min-h-screen bg-gray-900'>
			<div className='w-full max-w-3xl mx-auto p-12 rounded-lg bg-gray-900 border border-gray-800 flex justify-between'>
				<div className='max-w-md'>
					<h2 className='text-3xl font-bold text-white mb-3'>
						Ready to join the future of Web3?
					</h2>
					<p className='text-gray-400 mb-8'>
						Whether you're looking to launch a project, find talent or join a
						community, we have everything you need.
					</p>
					<button className='flex items-center gap-2 px-5 py-3 rounded-md bg-indigo-500 text-white font-medium transition-all'>
						Connect Wallet
						<ArrowRight size={18} />
					</button>
				</div>
				<div className='flex items-start'>
					<div className='bg-indigo-900 bg-opacity-50 p-6 rounded-full'>
						<Wallet size={48} className='text-indigo-300' />
					</div>
				</div>
			</div>
		</div>
	);
}
