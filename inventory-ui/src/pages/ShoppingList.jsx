import Header from "../components/Header";

export default function ShoppingList() {
  const user = { name: "Fiona Fox" };
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header user={user} />
      <div className="max-w-4xl mx-auto px-4 py-6">
        <h2 className="text-xl font-bold">Shopping List</h2>
        <p className="mt-4 text-gray-400">Here will be your shopping items.</p>
      </div>
    </div>
  );
}
