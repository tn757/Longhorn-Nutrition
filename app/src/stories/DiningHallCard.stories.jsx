// app/stories/DiningHallCard.stories.jsx
import DiningHallCard from '../DiningHallCard';
import '../App.css';

export default {
  title: 'Components/DiningHallCard',
  component: DiningHallCard,
  parameters: {
    layout: 'centered',
  },
};

export const Default = () => (
  <DiningHallCard name="Jester" />
);

export const Kinsolving = () => (
  <DiningHallCard name="Kinsolving" />
);

export const Perry = () => (
  <DiningHallCard name="Perry" />
);
