import React, { useState, useEffect } from 'react';
// In a real project, you would need to install recharts: npm install recharts
import NutritionChart from './NutritionChart'; // IMPORT THE NEW COMPONENT
import mealsData from '../public/meals.json';
import dvData from '../public/dv.json';
// Re-enabled menu.json import
import menuData from '../public/menu.json'; 

// --- Components ---

// NutritionChart component is now in its own file: NutritionChart.jsx

const MealItemDetail = ({ item, servings, fullFoodData }) => {
    // This component relies on 'fullFoodData' from 'menu.json'.
    if (!fullFoodData || fullFoodData.length === 0) {
        return (
            <tr className="border-b border-gray-200">
                <td className="py-2 pr-2 font-medium text-gray-800">{item.item_name} {servings > 1 ? `(x${servings})` : ''}</td>
                <td colSpan="7" className="py-2 px-2 text-center text-gray-400">Detailed nutrition data not available</td>
            </tr>
        );
    }

    const foodDetails = fullFoodData.find(food => food.item_name === item.item_name);

    if (!foodDetails) {
        return <tr><td colSpan="8" className="text-red-500">Could not find details for {item.item_name}</td></tr>;
    }
    
    // Helper to parse string values (e.g., "6.8g") and multiply by servings
    const calc = (value) => {
        if (typeof value !== 'string' && typeof value !== 'number') return 0;
        return (parseFloat(value) || 0) * servings;
    }

    return (
        <tr className="border-b border-gray-200 hover:bg-gray-50">
            <td className="py-2 pr-2 font-medium text-gray-800">{item.item_name} {servings > 1 ? `(x${servings})` : ''}</td>
            <td className="py-2 px-2 text-center">{calc(foodDetails.calories).toFixed(0)}</td>
            <td className="py-2 px-2 text-center">{calc(foodDetails.protein).toFixed(1)}g</td>
            <td className="py-2 px-2 text-center">{calc(foodDetails.total_fat).toFixed(1)}g</td>
            <td className="py-2 px-2 text-center">{calc(foodDetails.dietary_fiber).toFixed(1)}g</td>
            <td className="py-2 px-2 text-center">{calc(foodDetails.potassium).toFixed(0)}mg</td>
            <td className="py-2 px-2 text-center">{calc(foodDetails.calcium).toFixed(0)}mg</td>
            <td className="py-2 px-2 text-center">{calc(foodDetails.iron).toFixed(1)}mg</td>
        </tr>
    );
};

// The fullFoodData prop is now accepted here to pass down
const MealDetail = ({ plan, onBack, dvTargets, fullFoodData }) => {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 animate-fade-in">
            <button onClick={onBack} className="mb-6 bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300">
                &larr; Back to All Plans
            </button>
            
            <div className="mb-6">
                <h3 className="text-3xl font-bold text-blue-600">Meal Plan #{plan.rank} - Detailed View</h3>
            </div>

            {/* The self-contained chart component is used here */}

            {Object.entries(plan.plan).map(([mealName, mealDetails]) => (
                <div key={mealName} className="mb-8">
                    <h4 className="font-bold text-2xl mb-3 text-gray-800 border-b pb-2">{mealName}</h4>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-gray-100 text-gray-600 uppercase">
                                <tr>
                                    <th className="py-2 pr-2">Item</th>
                                    <th className="py-2 px-2 text-center">Calories</th>
                                    <th className="py-2 px-2 text-center">Protein</th>
                                    <th className="py-2 px-2 text-center">Fat</th>
                                    <th className="py-2 px-2 text-center">Fiber</th>
                                    <th className="py-2 px-2 text-center">Potassium</th>
                                    <th className="py-2 px-2 text-center">Calcium</th>
                                    <th className="py-2 px-2 text-center">Iron</th>
                                </tr>
                            </thead>
                            <tbody>
                                {mealDetails.items.map((item, index) => (
                                    // Pass the fullFoodData down to the item detail component
                                    <MealItemDetail key={index} item={item} servings={item.servings} fullFoodData={fullFoodData} />
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            ))}
            <NutritionChart dailyTotals={plan.daily_totals} dvTargets={dvTargets} />


        </div>
    );
};

const MealPlanCard = ({ plan, onSelect }) => {
    const { rank, micronutrient_score, daily_totals, plan: meals } = plan;

    return (
        <div onClick={() => onSelect(plan)} className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 hover:shadow-xl hover:border-blue-300 cursor-pointer transition-all duration-300">
            <div className="mb-6">
                <div className="flex flex-col sm:flex-row justify-between sm:items-center">
                    <div>
                        <h3 className="text-3xl font-bold text-blue-600">Meal Plan #{rank}</h3>
                        <p className="text-sm text-gray-500 mt-1">
                            Micronutrient Score: <span className="font-semibold text-blue-800">{micronutrient_score.toFixed(4)}</span> (Lower is better)
                        </p>
                    </div>
                    <div className="bg-blue-50 border border-blue-200 text-blue-800 rounded-lg p-3 mt-4 sm:mt-0 text-right">
                        <p className="text-lg font-semibold">{daily_totals.calories.toFixed(0)} Total Calories</p>
                        <p className="text-xs">
                            P: {daily_totals.protein.toFixed(1)}g | 
                            F: {daily_totals.total_fat.toFixed(1)}g | 
                            C: {daily_totals.total_carbohydrate.toFixed(1)}g
                        </p>
                    </div>
                </div>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
                {Object.entries(meals).map(([name, details]) => (
                     <div key={name} className="bg-gray-50 p-4 rounded-lg shadow-inner">
                        <h4 className="font-bold text-xl mb-2 text-gray-800">{name}</h4>
                        <p className="text-sm text-gray-500 mb-3 font-medium">{details.total_calories.toFixed(0)} calories</p>
                        <ul className="text-sm space-y-2">
                            {details.items.map((item, index) => (
                                <li key={index} className="flex justify-between items-center text-gray-700">
                                    <span>{item.item_name}</span>
                                    {item.is_topping && (
                                        <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full font-medium">Topping</span>
                                    )}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
        </div>
    );
};

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
