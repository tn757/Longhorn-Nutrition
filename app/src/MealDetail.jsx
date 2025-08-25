import NutritionChart from './NutritionChart'; // IMPORT THE NEW COMPONENT

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
export default function MealDetail  ({ plan, onBack, dvTargets, fullFoodData }) {
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