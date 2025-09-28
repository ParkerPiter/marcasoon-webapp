"use client";
import Image from "next/image";
import NavComponent from "./components/NavComponent";
import NavMobileComponent from "./components/NavMobileComponent";
import Cards from "./components/packages/Cards";
import { useState, useEffect } from "react";

export default function Home() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div className="font-sans min-h-screen  pb-20 flex flex-col gap-16 items-center">
      {isMobile &&
      <NavMobileComponent />
       } {!isMobile &&
      <NavComponent />
       }
      {/* Hero */}
      <section className="w-full py-16 text-black">
        <h1 className="text-4xl font-bold text-center mb-4">Bienvenido a <span className="text-[#192A56]">Marca</span><span className="text-[#FF6B6B]">soon</span></h1>
        <p className="text-center text-lg">Protege tu marca de forma fácil y rápida.</p>
      </section>

      {/* Cómo trabajamos */}
      <section className="w-full py-12 text-black">
        <h2 className="text-2xl font-semibold text-center mb-4">¿Cómo trabajamos?</h2>
        <p className="text-center">Te guiamos en cada paso del proceso de registro y protección de tu marca.</p>
      </section>

      {/* Precios */}
      <section className="w-5/6 py-12 text-black">
        <h3 className="text-2xl font-medium text-center mb-4 uppercase">Paquetes</h3>
        <Cards></Cards>
      </section>

      {/* Otros servicios */}
      <section className="w-full py-12 text-black">
        <h2 className="text-2xl font-semibold text-center mb-4">Otros servicios</h2>
        <p className="text-center">Consultoría, vigilancia de marcas y más soluciones legales.</p>
      </section>

      {/* Testimoniales */}
      <section className="w-full py-12 text-black">
        <h2 className="text-2xl font-semibold text-center mb-4">Testimoniales</h2>
        <p className="text-center">"Excelente servicio, rápido y confiable." - Cliente satisfecho</p>
      </section>
    </div>
  );
}
