// app/stories/MealDetail.stories.jsx
import MealDetail from '../MealDetail';
import '../App.css';

export default {
  title: 'Components/MealDetail',
  component: MealDetail,
  parameters: {
    layout: 'padded',
  },
};

const mockPlan = {
  rank: 1,
  micronutrient_score: 0.1234,
  daily_totals: {
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
  },
  plan: {
    Breakfast: {
      total_calories: 500,
      items: [
        { item_name: 'Oatmeal', is_topping: false, servings: 1 },
        { item_name: 'Blueberries', is_topping: true, servings: 0.5 },
        { item_name: 'Almonds', is_topping: true, servings: 0.25 },
      ],
    },
    Lunch: {
      total_calories: 700,
      items: [
        { item_name: 'Chicken Salad', is_topping: false, servings: 1 },
        { item_name: 'Avocado', is_topping: true, servings: 0.5 },
        { item_name: 'Mixed Greens', is_topping: false, servings: 1 },
      ],
    },
    Dinner: {
      total_calories: 800,
      items: [
        { item_name: 'Salmon', is_topping: false, servings: 1 },
        { item_name: 'Quinoa', is_topping: false, servings: 0.75 },
        { item_name: 'Broccoli', is_topping: false, servings: 1 },
      ],
    },
  },
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

const mockFullFoodData = [
  {
    item_name: 'Oatmeal',
    calories: '150',
    protein: '5.5',
    total_fat: '3',
    dietary_fiber: '4',
    potassium: '150',
    calcium: '20',
    iron: '1.5',
  },
  {
    item_name: 'Blueberries',
    calories: '85',
    protein: '1.1',
    total_fat: '0.5',
    dietary_fiber: '3.6',
    potassium: '114',
    calcium: '9',
    iron: '0.4',
  },
  {
    item_name: 'Almonds',
    calories: '164',
    protein: '6',
    total_fat: '14',
    dietary_fiber: '3.5',
    potassium: '200',
    calcium: '76',
    iron: '1.1',
  },
  {
    item_name: 'Chicken Salad',
    calories: '300',
    protein: '25',
    total_fat: '18',
    dietary_fiber: '2',
    potassium: '400',
    calcium: '30',
    iron: '2.5',
  },
  {
    item_name: 'Avocado',
    calories: '160',
    protein: '2',
    total_fat: '15',
    dietary_fiber: '6.7',
    potassium: '485',
    calcium: '12',
    iron: '0.6',
  },
  {
    item_name: 'Mixed Greens',
    calories: '20',
    protein: '2',
    total_fat: '0.2',
    dietary_fiber: '1.2',
    potassium: '200',
    calcium: '30',
    iron: '1.2',
  },
  {
    item_name: 'Salmon',
    calories: '280',
    protein: '34',
    total_fat: '12',
    dietary_fiber: '0',
    potassium: '600',
    calcium: '20',
    iron: '0.5',
  },
  {
    item_name: 'Quinoa',
    calories: '222',
    protein: '8',
    total_fat: '3.6',
    dietary_fiber: '5.2',
    potassium: '318',
    calcium: '31',
    iron: '2.8',
  },
  {
    item_name: 'Broccoli',
    calories: '55',
    protein: '3.7',
    total_fat: '0.6',
    dietary_fiber: '5.2',
    potassium: '316',
    calcium: '47',
    iron: '0.7',
  },
];

export const Default = () => (
  <MealDetail 
    plan={mockPlan} 
    onBack={() => console.log('Back button clicked')} 
    dvTargets={mockDvTargets}
    fullFoodData={mockFullFoodData}
  />
);
