import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';

// Custom Tooltip for better readability
// It needs dvTargets passed to it to show the full context.
const CustomTooltip = ({ active, payload, label, dvTargets }) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;
        // Recreate the key to look up in dvTargets
        const nutrientKey = label.toLowerCase().replace(' ', '_');
        const targetValue = dvTargets[nutrientKey];
        const actualValue = (data.percentDV / 100 * targetValue).toFixed(1);
        
        let unit = 'g'; // Default unit
        if (['sodium', 'potassium', 'calcium', 'cholesterol'].includes(nutrientKey)) {
            unit = 'mg';
        } else if (nutrientKey === 'vitamin_d') {
            unit = 'mcg';
        } else if (nutrientKey === 'iron') {
            unit = 'mg';
        }

        return (
            <div className="bg-white p-3 border border-gray-300 rounded-lg shadow-xl">
                <p className="font-bold text-gray-800">{label}</p>
                <p className={`text-sm font-semibold ${payload[0].fill === '#f56565' ? 'text-red-600' : 'text-blue-600'}`}>
                    Achieved: {data.percentDV}% of Daily Value
                </p>
                 <p className="text-xs text-gray-500 mt-1">
                    {`(${actualValue} / ${targetValue}${unit})`}
                 </p>
            </div>
        );
    }
    return null;
};


const NutritionChart = ({ dailyTotals, dvTargets }) => {
    // We want to visualize the most important nutrients as a percentage of their DV.
    // These are nutrients you want to get enough of.
    const beneficialNutrients = [
        'protein', 'dietary_fiber', 'potassium', 'calcium', 'iron', 'vitamin_d'
    ];

    // These are nutrients you generally want to limit.
    const limitNutrients = [
        'sodium', 'saturated_fat', 'added_sugars', 'cholesterol'
    ];
    
    const nutrientsToChart = [...beneficialNutrients, ...limitNutrients];

    const chartData = nutrientsToChart.map(key => {
        const actual = dailyTotals[key] || 0;
        const target = dvTargets[key] || 1; // Avoid division by zero
        const percentDV = (actual / target) * 100;
        
        return {
            name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()), // Format name for display
            percentDV: parseFloat(percentDV.toFixed(1)),
            isUpperLimit: limitNutrients.includes(key)
        };
    });

    return (
        <div className="mb-8">
             <h4 className="font-bold text-2xl mb-4 text-gray-800 border-b pb-2">Nutrient Overview (% of Daily Value)</h4>
            <ResponsiveContainer width="100%" height={400}>
                <BarChart data={chartData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} interval={0} />
                    <YAxis 
                        label={{ value: '% of Daily Value', angle: -90, position: 'insideLeft' }} 
                        tickFormatter={(tick) => `${tick}%`}
                    />
                    {/* Pass dvTargets to the custom tooltip */}
                    <Tooltip content={<CustomTooltip dvTargets={dvTargets} />} cursor={{fill: 'rgba(230, 230, 230, 0.4)'}} />
                    <Legend />
                    <ReferenceLine y={100} stroke="#e53e3e" strokeDasharray="4 4" label={{ value: '100% DV', position: 'insideTopRight' }} />
                    <Bar dataKey="percentDV" name="% of Daily Value">
                        {
                            chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.isUpperLimit && entry.percentDV > 100 ? '#f56565' : '#4299e1'} />
                            ))
                        }
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default NutritionChart;
