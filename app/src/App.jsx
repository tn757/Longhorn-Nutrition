import React, { useState, useEffect } from 'react';
import mealsData from '../public/meals.json';
import dvData from '../public/dv.json';
import menuData from '../public/menu.json'; 
import MealDetail from './MealDetail';
import MealPlanCard from './MealPlanCard';

// --- Main App Component ---
export default function App() {
    const [mealPlans, setMealPlans] = useState([]);
    const [fullFoodData, setFullFoodData] = useState([]); // State for menu data
    const [dvTargets, setDvTargets] = useState({});
    const [selectedPlan, setSelectedPlan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Since we are importing the JSON directly, we don't need to fetch.
        if (mealsData && dvData && menuData) {
            setMealPlans(mealsData);
            setDvTargets(dvData);
            setFullFoodData(menuData); // Load menu data into state
            setLoading(false);
        } else {
            setError("Could not load data from JSON files.");
            setLoading(false);
        }
    }, []); // Empty dependency array means this runs once on mount

    const handleSelectPlan = (plan) => {
        setSelectedPlan(plan);
    };

    const handleBack = () => {
        setSelectedPlan(null);
    };

    const renderContent = () => {
        if (loading) {
            return <p className="text-center text-gray-500">Loading meal plans...</p>;
        }
        if (error) {
            return <p className="text-center text-red-500">{error}</p>;
        }
        if (selectedPlan) {
            // Pass the required props to MealDetail, including fullFoodData
            return <MealDetail plan={selectedPlan} onBack={handleBack} dvTargets={dvTargets} fullFoodData={fullFoodData} />;
        }
        if (mealPlans.length > 0) {
            return (
                <div className="space-y-8">
                    {mealPlans.map(plan => (
                        <MealPlanCard key={plan.rank} plan={plan} onSelect={handleSelectPlan} />
                    ))}
                </div>
            );
        }
        return <p className="text-center text-gray-500">No meal plans available to display.</p>;
    };

    return (
        <div className="bg-gray-100 text-gray-800 min-h-screen" style={{ fontFamily: "'Inter', sans-serif" }}>
            <div className="container mx-auto p-4 md:p-8">
                <header className="text-center mb-10">
                    <h1 className="text-4xl md:text-5xl font-bold text-gray-900">Today's Meal Plans</h1>
                    <p className="text-lg text-gray-600 mt-2">Nutritionally balanced meal plans for the day.</p>
                </header>

                <main id="contentContainer">
                    {renderContent()}
                </main>
            </div>
        </div>
    );
}
