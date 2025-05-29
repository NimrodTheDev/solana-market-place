
// tailwind.config.js
module.exports = {
	content: ["./src/**/*.{js,jsx,ts,tsx}"],
	theme: {
		extend: {
			colors: {
				'custom-dark-blue': '#11141F',
				'custom-light-purple': '#7E6DC8',
				"custom-hero-back": '#080a0f',
			},
			gridTemplateColumns: {
				'custom-2-1': '2fr 1fr',
				'custom-3-1': '3fr 1fr',
			},
		},
	},
	plugins: [],
};
