import NFTCollection from "../components/landingPage/collection";
import FeaturesSection from "../components/landingPage/features";
import Hero from "../components/landingPage/hero";
import HowItWorks from "../components/landingPage/howItWorks";
import OnboardingCard from "../components/landingPage/onboardingCard";

const LandingPage = () => {
	return (
		<div>
			<Hero />
			<NFTCollection />
			<FeaturesSection />
			<HowItWorks />
			<OnboardingCard />
		</div>
	);
};

export default LandingPage;
