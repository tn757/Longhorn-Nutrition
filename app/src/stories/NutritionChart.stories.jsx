// app/stories/NutritionChart.stories.jsx
import NutritionChart from '../NutritionChart';
import '../App.css';

export default {
  title: 'Components/NutritionChart',
  component: NutritionChart,
  parameters: {
    layout: 'padded',
  },
};

const mockDailyTotals = {
  calories: 2000,
  protein: 150,
  total_fat: 70,
  total_carbohydrate: 250,
  dietary_fiber: 25,
  sodium: 2300,
  potassium: 3500,
  calcium: 1000,
  iron: 18,
  saturated_fat: 20,
  added_sugars: 50,
  cholesterol: 300,
  vitamin_d: 20,
};

const mockDvTargets = {
  calories: 2000,
  protein: 50,
  total_fat: 65,
  total_carbohydrate: 300,
  dietary_fiber: 28,
  sodium: 2300,
  potassium: 3500,
  calcium: 1300,
  iron: 18,
  saturated_fat: 20,
  added_sugars: 50,
  cholesterol: 300,
  vitamin_d: 20,
};

export const Default = () => (
  <NutritionChart 
    dailyTotals={mockDailyTotals} 
    dvTargets={mockDvTargets} 
  />
);

export const HighProtein = () => (
  <NutritionChart 
    dailyTotals={{
      ...mockDailyTotals,
      protein: 200, // Higher protein
    }} 
    dvTargets={mockDvTargets} 
  />
);

export const LowFiber = () => (
  <NutritionChart 
    dailyTotals={{
      ...mockDailyTotals,
      dietary_fiber: 10, // Lower fiber
    }} 
    dvTargets={mockDvTargets} 
  />
);

export const HighSodium = () => (
  <NutritionChart 
    dailyTotals={{
      ...mockDailyTotals,
      sodium: 3500, // Higher sodium (exceeds DV)
    }} 
    dvTargets={mockDvTargets} 
  />
);
