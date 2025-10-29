"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import Card from "./Card";
import { testimonials } from "../../../../api/test";

interface SliderTestimonialProps {
  intervalMs?: number;
}

const usePageSize = () => {
  const [pageSize, setPageSize] = useState(2); // default desktop
  useEffect(() => {
    const update = () => setPageSize(window.innerWidth < 640 ? 1 : 2); // < sm => 1
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);
  return pageSize;
};

const SliderTestimonial = ({ intervalMs = 8000 }: SliderTestimonialProps) => {
  const pageSize = usePageSize();

  const pages = useMemo(() => {
    const p: typeof testimonials[] = [];
    for (let i = 0; i < testimonials.length; i += pageSize) {
      p.push(testimonials.slice(i, i + pageSize));
    }
    return p;
  }, [pageSize]);

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
    <div className="relative w-full py-6">
      {/* Contenedor principal del carrusel */}
  <div className="overflow-hidden w-full max-w-[1700px] mx-auto px-2">
        <div
          className="flex transition-transform duration-500 ease-out"
          style={{ transform: `translateX(-${page * 100}%)` }}
        >
          {pages.map((group, idx) => {
            const isSingleInDouble = pageSize === 2 && group.length === 1;
            const gridClass = pageSize === 1
              ? "grid grid-cols-1 gap-10 w-full max-w-[1600px] mx-auto"
              : isSingleInDouble
                ? "grid grid-cols-1 gap-10 w-full max-w-[1600px] mx-auto"
                : "grid grid-cols-1 sm:grid-cols-2 gap-10 w-full max-w-[1600px] mx-auto";
            return (
              <div key={idx} className="w-full flex-shrink-0 flex justify-center">
                <div className={gridClass + " justify-items-center"}>
                  {group.map((t) => (
                    <Card
                      key={t.id}
                      id={t.id}
                      name={t.name}
                      testimonial={t.quote}
                      logo={t.logo}
                      countryName={t.country}
                    />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default SliderTestimonial;