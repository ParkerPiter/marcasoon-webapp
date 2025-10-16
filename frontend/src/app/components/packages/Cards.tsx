"use client";

import { useEffect, useState } from 'react';
// import { paquetes } from '../../../../api/test'
import { getPlansAPI } from "../../../../api/api";
import { CardPrice } from '../../interfaces/card';
import CardPrices from './Card';
import Loader from '../Loader';

const Cards = () => {

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [paquetes, setPaquetes] = useState<CardPrice[]>([]);

  useEffect(() => {
    let alive = true;
    const MIN_SPINNER_MS = 600; // retardo mínimo del loader
    const FETCH_TIMEOUT_MS = 10000; // timeout de red

    const controller = new AbortController();
    const timerAbort = setTimeout(() => controller.abort('timeout'), FETCH_TIMEOUT_MS);

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      const start = Date.now();
      try {
        const data = await getPlansAPI(undefined, { signal: controller.signal });
        if (!alive) return;
        console.log('[Cards] Planes recibidos:', data?.length);
        setPaquetes(data);
      } catch (e: any) {
        if (!alive) return;
        const msg = e?.name === 'AbortError' ? 'La solicitud excedió el tiempo de espera.' : (e?.message || 'Error cargando planes');
        setError(msg);
        console.error('[Cards] Error al obtener planes:', e);
      } finally {
        clearTimeout(timerAbort);
        const elapsed = Date.now() - start;
        const wait = Math.max(0, MIN_SPINNER_MS - elapsed);
        await new Promise((r) => setTimeout(r, wait));
        if (alive) setLoading(false);
      }
    };
    fetchData();

    return () => {
      alive = false;
      clearTimeout(timerAbort);
      controller.abort('unmount');
    };
  }, []);

  console.log('[Cards] Render', paquetes);

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
