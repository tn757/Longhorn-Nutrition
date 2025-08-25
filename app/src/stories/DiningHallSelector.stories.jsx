// app/stories/DiningHallSelector.stories.jsx
import DiningHallSelector from '../DiningHallSelector';
import '../App.css';

export default {
  title: 'Components/DiningHallSelector',
  component: DiningHallSelector,
  parameters: {
    layout: 'padded',
  },
};

export const Default = () => (
  <DiningHallSelector />
);
