export default function MealPlanCard ({ plan, onSelect }) {
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