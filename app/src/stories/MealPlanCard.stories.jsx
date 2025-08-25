// app/stories/MealPlanCard.stories.jsx
import MealPlanCard from '../MealPlanCard';
import '../app.css'; // Import global styles if needed

export default {
  title: 'Components/MealPlanCard',
  component: MealPlanCard,
};

const mockPlan = {
  rank: 1,
  micronutrient_score: 0.1234,
  daily_totals: {
    calories: 2000,
    protein: 150,
    total_fat: 70,
    total_carbohydrate: 250,
  },
  plan: {
    Breakfast: {
      total_calories: 500,
      items: [
        { item_name: 'Oatmeal', is_topping: false },
        { item_name: 'Blueberries', is_topping: true },
      ],
    },
    Lunch: {
      total_calories: 700,
      items: [
        { item_name: 'Chicken Salad', is_topping: false },
        { item_name: 'Avocado', is_topping: true },
      ],
    },
    Dinner: {
      total_calories: 800,
      items: [
        { item_name: 'Salmon', is_topping: false },
        { item_name: 'Quinoa', is_topping: false },
      ],
    },
  },
};

export const Default = () => (
  <MealPlanCard plan={mockPlan} onSelect={(p) => console.log('Selected plan:', p.rank)} />
);
