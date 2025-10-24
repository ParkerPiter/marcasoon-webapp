"use client";

import Cards from "./components/packages/Cards";
import SliderTestimonial from "./components/testimonials/SliderTestimonial";
import CarruselComponent from "./components/carrusel/carruselComponent";
import BlogCards from "./components/blog/Cards";
import FaqComponent from "./components/faq/faqComponent";
import Banner from "./components/Banner";
import Button from "./components/buttons/homeButtons";
import Image from "next/image";

import proceso from '../../public/arte2.png';
import protocolo_madrid from '../../public/BANNER-PRINCIPAL.png';


export default function Home() {

  return (
    <div className="font-sans min-h-screen  pb-20 flex flex-col gap-16 items-center">

      {/* Hero */}
      <section className="w-full py-0 text-black">
        <Banner />
      </section>

      {/* Cómo trabajamos */}
      <section className="w-full text-black px-4 sm:px-8 md:px-16 lg:px-20">
        <h2 className="md:text-3xl text-2xl font-semibold text-center mb-4">¿Cómo <span className="font-playfair italic">trabajamos</span>?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div className="md:order-1 order-2 w-full">
            <Image
              src={proceso}
              alt="Cómo trabajamos"
              width={800}
              height={800}
              sizes="(min-width: 1024px) 70vw, (min-width: 768px) 85vw, 96vw"
              placeholder="blur"
              className="w-full h-auto rounded-2xl"
            />
          </div> 
          <div className="md:order-2 orden-1 ">
            <h3 className="md:text-xl text-xl font-semibold mb-2 md:text-start text-center">Paso a paso</h3>
            <p className="text-center md:text-lg text-base md:text-left">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque suscipit luctus orci in hendrerit. Nulla velit urna, aliquet accumsan turpis a, faucibus tincidunt lorem. Sed euismod commodo risus et luctus. Nulla tempor erat eget venenatis tincidunt. Duis feugiat leo quis elit luctus, eu placerat ligula lobortis. Aenean tincidunt finibus dictum. Curabitur finibus ornare ornare. Quisque egestas dui sapien, vitae luctus justo tincidunt ut. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec feugiat leo elit, ac feugiat turpis commodo ut. Nam id nisi quis metus ultrices commodo luctus in magna. Donec sodales efficitur ullamcorper. Aenean convallis tincidunt mollis.</p>
            <Button />
          </div>
        </div>
      </section>

      {/* Precios */}
      <section className="w-5/6 py-12 text-black">
        <h3 className="text-2xl text-center mb-4 uppercase font-semibold font-archivo">Nuestros <span className="font-playfair font-semibold italic">Paquetes</span></h3>
        <Cards></Cards>
      </section>

      {/* Otros servicios */}
      <section className="w-full bg-[#ED5E32]">
        {/* <h2 className="md:text-3xl text-2xl font-semibold text-center mb-6">¿Cómo <span className="font-playfair italic">trabajamos</span>?</h2> */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center ">
          <div className="order-1 md:order-1 w-full md:w-[940px] md:px-0 px-0">
            <Image
              src={protocolo_madrid}
              alt="Protocolo de Madrid"
              width={680}
              height={680}
              sizes="(min-width: 1024px) 70vw, (min-width: 768px) 85vw, 96vw"
              placeholder="blur"
              className="w-full h-auto "
            />
          </div> 
          <div className="order-2 md:order-2 py-12 md:pr-12 px-4 md:px-0">
            <p className="text-center md:text-lg text-base md:text-left">
              El <span className="italic font-playfair font-semibold ">Protocolo de Madrid</span> es un sistema internacional que permite registrar una marca en varios países con un solo trámite,
              haciendo todo mucho más simple y eficiente.
            </p>

            <div className="space-y-2 mt-3">
              <h3 className="font-semibold">Cómo funciona con Marcasoon:</h3>
              <ul className="list-disc pl-6 space-y-2">
                <li>Primero, solicitamos tu marca en los Estados Unidos.</li>
                <li>Seguidamente iniciamos el proceso internacional bajo el Protocolo de Madrid, extendiendo la protección a más de 130 países miembros del sistema.</li>
                <li>La Oficina Internacional revisa tu solicitud y la envía a los países elegidos. Cada país evalúa la marca según sus propias leyes.</li>
                <li>Una vez cumplimentado cada proceso, tu marca quedará protegida en todos esos países, sin tener que hacer trámites separados en cada uno.</li>
              </ul>
            </div>

            <div className="space-y-2 mt-4">
              <h3 className="font-semibold">Beneficios:</h3>
              <ul className="list-disc pl-6 space-y-2">
                <li><span className="font-semibold">Ahorro de tiempo y dinero:</span> un solo formulario, un solo pago, una sola estrategia global.</li>
                <li><span className="font-semibold">Cobertura internacional rápida:</span> protege tu marca en múltiples países a la vez.</li>
                <li><span className="font-semibold">Gestión sencilla:</span> cualquier cambio, modificación o renovación se hace desde Marcasoon.</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonios de nuestros clientes */}
      <section className="w-full py-12 text-black">
        <h2 className="text-2xl font-semibold text-center mb-4 font-archivo"><span className="font-playfair italic">Testimonios</span> de nuestros clientes</h2>
        <SliderTestimonial />
      </section>

      {/* Logo Carrusel */}
      <section className="w-full py-2 text-black">
        {/* <h2 className="text-2xl font-semibold text-center mb-4">Nuestros Clientes</h2> */}
        <CarruselComponent />
      </section>

      {/* Blog */}
      <section className="w-full py-12 text-black">
        <h2 className="text-2xl font-semibold text-center mb-4">Nuestro Blog</h2>
        <BlogCards />
      </section>

      {/* FAQs */}
      <section className="w-full py-6 text-black">
        <FaqComponent items={[
          {
            question: "¿Qué es una marca y por qué es tan importante para mi negocio?",
            answer: "Tu marca es la identidad de tu negocio: es tu nombre, logo y todo lo que te hace único. Registrarla es el único camino para protegerla legalmente en el mercado, asegurando que nadie más pueda copiar o robar tu idea. Es la base fundamental para construir una empresa segura, respetada y con valor."
          },
          {
            question: "¿La protección de mi marca aplica a nivel mundial?",
            answer: "El registro de una marca es territorial, lo que significa que la protección inicial es válida solo en el país donde se registra. Sin embargo, a través del Protocolo de Madrid, te facilitamos un solo trámite para que puedas registrar tu marca en múltiples países a la vez, incluyendo EE. UU., de manera eficiente."
          },
          {
            question: "¿Mi registro es un proceso rápido?",
            answer: "El proceso de registro con la USPTO (la oficina de marcas de EE. UU.) suele tomar entre 8 y 12 meses. Nuestra misión es guiarte para que el camino sea lo más rápido y fluido posible, minimizando demoras y obstáculos gracias a nuestra experiencia."
          },
          {
            question: "¿Cómo puedo saber si mi marca está disponible para registro?",
            answer: "La única forma segura es a través de una búsqueda profesional y profunda. Evitar una búsqueda adecuada es el error más común y la causa principal de rechazos. Nosotros realizamos un análisis exhaustivo en las bases de datos oficiales para identificar cualquier marca idéntica o similar que pueda representar un riesgo. Con nuestro informe, tomas la mejor decisión."
          },
            {
            question: '¿Qué son las "Clases de Niza" y por qué debo elegir la correcta?',
            answer: 'La Clasificación de Niza es un sistema internacional que agrupa productos y servicios en 45 categorías (o "clases"). Es la base para tu solicitud de registro. Es vital elegirlas correctamente porque tu marca solo estará protegida legalmente para los productos o servicios específicos que declares. Si no incluyes una clase importante para tu negocio, podrías dejar una puerta abierta a que un competidor use tu marca en ese sector. Nosotros te asesoramos para elegir las clases adecuadas que blinden tu negocio completamente.'
          },
          //   {
          //   question: "¿Qué pasa si mi marca ya está registrada?",
          //   answer: "Si tu marca no está disponible, no es el final. Te asesoraremos para encontrar la mejor alternativa legal. Podemos ayudarte a modificarla o a crear una nueva que sea única y viable, para que puedas seguir adelante con tu negocio sin tener que empezar de cero."
          // },
          //   {
          //   question: "¿Qué incluye el servicio de Marcasoon?",
          //   answer: "Nuestro servicio es integral. No solo nos encargamos del papeleo. Te ofrecemos una asesoría completa que incluye la búsqueda inicial de viabilidad, la preparación y presentación de la solicitud, y el monitoreo de tu marca durante todo el proceso ante la USPTO."
          // },
          //   {
          //   question: "¿Cómo funciona la Garantía de Éxito?",
          //   answer: "Creemos firmemente en nuestro trabajo. Si tu marca es rechazada por un error de nuestra parte en la solicitud o en la asesoría, te devolvemos el 100% de nuestros honorarios profesionales. Tu inversión está protegida, dándote total tranquilidad."
          // },
          //   {
          //   question: "¿El costo del servicio incluye las tarifas del gobierno?",
          //   answer: "No. El costo de nuestro servicio profesional cubre nuestra asesoría y gestión experta. Las tarifas gubernamentales de la USPTO o de la OMPI son un pago separado que se gestiona directamente a las oficinas. Te daremos un desglose transparente de todos los costos."
          // },
          //   {
          //   question: "¿Qué pasa después del registro? ¿Tengo que renovar mi marca?",
          //   answer: "¡Absolutamente! El registro de una marca en EE. UU. (USPTO) es válido por 10 años, pero debes presentar una Declaración de Uso (Secciones 8 y 15) entre el quinto y sexto año para mantenerla activa. Si no se presenta, tu marca se cancela. Dentro de nuestro servicio, te monitoreamos y te notificamos con suficiente tiempo para que nunca pierdas tu protección."
          // },
          // {
          //   question: "¿Qué me diferencia de otros servicios de registro de marca?",
          //   answer: "No somos solo un portal automatizado. Somos tu aliado. Te damos la tranquilidad de estar en manos de expertos que entienden tanto el proceso legal complejo como tu cultura de negocio. Nuestro objetivo es que tu marca se convierta en un activo fuerte, seguro y respetado, no solo en un certificado."
          // }
        ]} />
      </section>

      {/* Footer */}
    </div>
  );
}
