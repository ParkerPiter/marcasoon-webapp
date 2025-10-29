"use client";

import { useRef, useState } from "react";
import SearchCard from "./searchCard";
import SearchBar from "./SearchBar";
import Loader from "../Loader";
import type { SearchCard as SearchCardType } from "@/app/interfaces/card";
import { searchTrademarksByName } from "../../../../api/api";

const POST_RESPONSE_DELAY_MS = 1500;

export default function SearchCards() {
  const [results, setResults] = useState<SearchCardType[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestIdRef = useRef(0);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query: string) => {
    const q = query.trim();
    if (!q) return;
    // Nuevo request: invalidar cualquier respuesta previa
    requestIdRef.current += 1;
    const myId = requestIdRef.current;
    setLoading(true);
    setError(null);
    setHasSearched(true);
    try {
      const data = await searchTrademarksByName(q);
      // Mantener el loader visible 1.5s después de la respuesta
      await new Promise((resolve) => setTimeout(resolve, POST_RESPONSE_DELAY_MS));
      if (myId !== requestIdRef.current) return; // respuesta obsoleta
      setResults(data);
    } catch (e: any) {
      // Mantener el loader visible 1.5s también en caso de error
      await new Promise((resolve) => setTimeout(resolve, POST_RESPONSE_DELAY_MS));
      if (myId !== requestIdRef.current) return; // respuesta obsoleta
      setError(e?.message || "Error al buscar");
    } finally {
      if (myId === requestIdRef.current) setLoading(false);
    }
  };

  const handleClear = () => {
    // Invalidar cualquier request en curso y limpiar resultados/errores
    requestIdRef.current += 1;
    setResults([]);
    setError(null);
    setLoading(false);
    setHasSearched(false);
  };

  return (
    <div className="w-full flex flex-col items-center">
      <SearchBar onSearch={handleSearch} loading={loading} onClear={handleClear} />

      {!loading && error && (
        <div className="text-red-600 text-sm mb-4">{error}</div>
      )}

      {loading ? (
        <div className="flex justify-center items-center py-8">
          <Loader />
        </div>
      ) : hasSearched ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full pt-6 md:px-32 px-3 pb-6">
          {results.map((it, idx) => (
            <SearchCard key={idx} {...it} />
          ))}
        </div>
      ) : null}
    </div>
  );
}
