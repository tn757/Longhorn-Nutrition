// DiningHallCard.jsx
export default function DiningHallCard({ name }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 animate-fade-in cursor-pointer hover:shadow-xl transition-shadow">
      <h2 className="text-3xl font-bold text-blue-600 mb-4">{name}</h2>
      <p className="text-gray-700">Click to view menu</p>
    </div>
  );
}
