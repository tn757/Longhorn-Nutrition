import DiningHallCard from './DiningHallCard';

const diningHalls = [
  { name: "Jester" },
  { name: "Kinsolving" },
  { name: "Perry" },
];

export default function DiningHallSelector() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {diningHalls.map(hall => (
        <DiningHallCard key={hall.name} name={hall.name} />
      ))}
    </div>
  );
}
