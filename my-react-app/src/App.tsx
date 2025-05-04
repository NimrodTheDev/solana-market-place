import NFTCollection from "./components/landingPage/collection";
import FeaturesSection from "./components/landingPage/features";
import Hero from "./components/landingPage/hero";
import HowItWorks from "./components/landingPage/howItWorks";
import OnboardingCard from "./components/landingPage/onboardingCard";
import LandingPage from "./pages/landingPage";

function App() {
	return (
		<div>
			<LandingPage />
			<Hero />
			<NFTCollection />
			<FeaturesSection />
			<HowItWorks />
			<OnboardingCard />
		</div>
	);
}

export default App;
