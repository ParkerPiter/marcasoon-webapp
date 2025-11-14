"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import Card from "./Card";
import { testimonials } from "../../../../api/test";

interface SliderTestimonialProps {
  intervalMs?: number;
}

// Determina cuántas tarjetas mostrar por página según ancho
const usePageSize = () => {
  const calc = () => {
    const w = window.innerWidth;
    if (w < 640) return 1;       // móvil
    if (w < 1024) return 2;      // tablet
    return 3;                    // desktop
  };
  const [pageSize, setPageSize] = useState<number>(typeof window === 'undefined' ? 3 : calc());
  useEffect(() => {
    const onResize = () => setPageSize(calc());
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  return pageSize;
};

const SliderTestimonial = ({ intervalMs = 8000 }: SliderTestimonialProps) => {
  const pageSize = usePageSize();

  // Paginación en grupos del tamaño actual de página (avanza de a 'pageSize')
  // Modo de una sola tarjeta por página siempre (animación de referencia)
  const pages = useMemo(() => testimonials.map(t => [t]), []);

  const [page, setPage] = useState(0);
  const total = pages.length;

  // Reset página al cambiar pageSize
  useEffect(() => {
    setPage(0);
  }, [pageSize]);

  const next = useCallback(() => {
    setPage((p) => (p + 1) % total);
  }, [total]);

  const prev = () => setPage((p) => (p - 1 + total) % total);

  useEffect(() => {
    if (total <= 1) return;
    const id = setInterval(next, intervalMs);
    return () => clearInterval(id);
  }, [next, intervalMs, total]);

  return (
    <div className="relative w-full py-6 ">
      <div className="overflow-hidden w-full max-w-5xl mx-auto px-0 ">
        <div
          className="flex transition-transform duration-500 ease-out"
          style={{ transform: `translateX(-${page * 100}%)` }}
        >
          {pages.map((group, idx) => (
            <div key={idx} className="w-full flex-shrink-0 space-x-4">
              <div className="w-full max-w-4xl mx-auto ">
                <Card
                  key={group[0].id}
                  id={group[0].id}
                  name={group[0].name}
                  testimonial={group[0].quote}
                  logo={group[0].logo}
                  countryName={group[0].country}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Dots */}
        {total > 1 && (
          <div className="flex justify-center gap-2 mt-8">
            {pages.map((_, i) => (
              <button
                key={i}
                onClick={() => setPage(i)}
                className={`w-3 h-3 rounded-full transition-colors ${i === page ? 'bg-[#192A56]' : 'bg-gray-300 hover:bg-gray-400'}`}
                aria-label={`Ir a página ${i + 1}`}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SliderTestimonial;