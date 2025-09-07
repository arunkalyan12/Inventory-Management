import { useInventory } from "../context/InventoryContext";

export default function InventoryTable() {
  const { items, updateQuantity } = useInventory();

  return (
    <div className="bg-gray-800 rounded-2xl p-4 mt-4 shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Inventory</h2>
        <button className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700">
          Add Item
        </button>
      </div>
      <table className="w-full text-left border-collapse">
        <thead>
          <tr>
            <th className="border-b p-2">Item</th>
            <th className="border-b p-2">Quantity</th>
            <th className="border-b p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-gray-700">
              <td className="p-2">{item.name}</td>
              <td className="p-2">{item.quantity}</td>
              <td className="p-2 space-x-2">
                <button
                  onClick={() => updateQuantity(item.id, 1)}
                  className="px-2 py-1 bg-green-500 rounded hover:bg-green-600"
                >
                  +
                </button>
                <button
                  onClick={() => updateQuantity(item.id, -1)}
                  className="px-2 py-1 bg-red-500 rounded hover:bg-red-600"
                >
                  −
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
