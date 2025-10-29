"use client";

import { useEffect, useState } from 'react';
import { loadPlansEnsuringDelay } from "@/store/store";
import { CardPrice } from '../../interfaces/card';
import CardPrices from './Card';
import Loader from '../Loader';

const Cards = () => {

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [paquetes, setPaquetes] = useState<CardPrice[]>([]);

  useEffect(() => {
    let alive = true;
    const run = async () => {
      setLoading(true);
      setError(null);
      const { data, error } = await loadPlansEnsuringDelay();
      if (!alive) return;
      if (error) {
        setError(error);
        setLoading(false);
        return;
      }
      setPaquetes(data);
      setLoading(false);
    };
    run();

    return () => {
      alive = false;
    };
  }, []);


  if (loading) return (
    <div className="w-full min-h-[50vh] flex items-center justify-center py-10">
      <Loader />
    </div>
  );
  if (error) return <p>Error: {error}</p>;
  if (!paquetes.length) return <p>No hay planes disponibles.</p>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  {paquetes.map((paquete) => (
        <CardPrices key={paquete.id} 
            id={paquete.id}
            title={paquete.title}
    client_objective={paquete.client_objective}
            description={paquete.description}
            includes={paquete.includes}
            price={paquete.price}
        />
      ))}
    </div>
  );
};

export default Cards;
