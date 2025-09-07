import { createContext, useContext, useState } from "react";

const InventoryContext = createContext();

export function InventoryProvider({ children }) {
  const [items, setItems] = useState([
    { id: 1, name: "Apples", quantity: 5 },
    { id: 2, name: "Milk", quantity: 2 },
    { id: 3, name: "Bread", quantity: 0 }
  ]);

  const updateQuantity = (id, change) => {
    setItems((prev) =>
      prev.map((item) =>
        item.id === id
          ? { ...item, quantity: Math.max(0, item.quantity + change) }
          : item
      )
    );
  };

  const setItemQuantity = (id, quantity) => {
    setItems((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, quantity: Math.max(0, quantity) } : item
      )
    );
  };

  return (
    <InventoryContext.Provider value={{ items, updateQuantity, setItemQuantity }}>
      {children}
    </InventoryContext.Provider>
  );
}

export function useInventory() {
  return useContext(InventoryContext);
}
