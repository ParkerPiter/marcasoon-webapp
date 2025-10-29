"use client";

import SearchCards from "./SearchCards";

export default function SearchComponent() {
  // Componente contenedor ligero que delega toda la lógica y render en SearchCards
  return (
    <div className="w-full">
      <SearchCards />
    </div>
  );
}
