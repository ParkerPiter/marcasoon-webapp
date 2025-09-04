import Image from "next/image";
import NavComponent from "./components/NavComponent";

export default function Home() {
  return (
    <div className="font-sans min-h-screen p-8 pb-20 flex flex-col gap-16 items-center">
      <NavComponent />
      {/* Hero */}
      <section className="w-full py-16 text-black">
        <h1 className="text-4xl font-bold text-center mb-4">Bienvenido a Marcasoon</h1>
        <p className="text-center text-lg">Protege tu marca de forma fácil y rápida.</p>
      </section>

      {/* Cómo trabajamos */}
      <section className="w-full py-12 text-black">
        <h2 className="text-2xl font-semibold text-center mb-4">¿Cómo trabajamos?</h2>
        <p className="text-center">Te guiamos en cada paso del proceso de registro y protección de tu marca.</p>
      </section>

      {/* Precios */}
      <section className="w-full py-12 text-black">
        <h2 className="text-2xl font-semibold text-center mb-4">Precios</h2>
        <p className="text-center">Planes accesibles para emprendedores y empresas.</p>
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
