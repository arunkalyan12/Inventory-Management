import Header from "../components/Header";
import InventoryTable from "../components/InventoryTable";

export default function Dashboard() {
  const user = { name: "Fiona Fox" };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header user={user} />
      <div className="max-w-4xl mx-auto px-4 py-6">
        <InventoryTable />
      </div>
    </div>
  );
}
