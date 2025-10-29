"use client";

import { useRef, useState } from "react";
import { Search, BrushCleaning } from "lucide-react";

interface Props {
  onSearch: (query: string) => void;
  loading?: boolean;
  onClear?: () => void;
}

export default function SearchBar({ onSearch, loading, onClear }: Props) {
  const [query, setQuery] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const q = query.trim();
    if (!q) return;
    onSearch(q);
    setHasSearched(true);
  };

  return (
    <form onSubmit={submit} className="flex mb-6 w-full max-w-4xl mx-auto">
      <input
        type="text"
        value={query}
        ref={inputRef}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Buscar marca (ej: google)"
        className="text-black flex-1 border-t border-b border-l bg-white border-[#ED5E32] rounded-s-2xl px-4 py-2 focus:outline-none  "
      />
      {/* Botón limpiar: sólo visible tras haber presionado buscar */}
      {hasSearched ? (
        <button
          type="button"
          onClick={() => {
            setQuery("");
            onClear?.();
            // Foco de vuelta al input
            inputRef.current?.focus();
            setHasSearched(false);
          }}
          // Permitimos limpiar incluso si está cargando (cancela búsqueda en el padre)
          aria-label="Limpiar búsqueda"
          className="border-y border-[#ED5E32] bg-white text-[#ED5E32] px-3 disabled:opacity-40 disabled:cursor-not-allowed hover:cursor-pointer"
        >
          <BrushCleaning className="w-5 h-5" />
        </button>
      ) : null}
      <button
        type="submit"
        disabled={loading || !query.trim()}
        className="bg-[#ED5E32] rounded-e-2xl hover:opacity-90 text-white font-semibold px-5 py-2 hover:cursor-pointer  "
      >
        <Search className="text-white" />
      </button>
    </form>
  );
}
