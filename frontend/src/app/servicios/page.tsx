"use client";

import Image from "next/image";
import Button from '@/app/components/buttons/homeButtons';
import { Asterisk } from 'lucide-react';
import { useEffect } from 'react';

/* Imagenes */
import registro from '../../../public/4146246_2205926-Photoroom.png';
import documentos from '../../../public/51017075_paper_2-Photoroom.png';
import patente from '../../../public/10756756_4501491-Photoroom.png';
import busqueda from '../../../public/5145027_2516805-Photoroom.png';
import protocolo from '../../../public/145019-Photoroom.png';

const ServicesPage = () => {
    // Smooth scroll al cargar con hash o cuando cambia el hash
    useEffect(() => {
        const scrollToHash = () => {
            if (typeof window === 'undefined') return;
            const hash = window.location.hash?.replace('#','');
            if (!hash) return;
            const el = document.getElementById(hash);
            if (el) {
                // delay mínimo para asegurar layout listo
                setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
            }
        };
        scrollToHash();
        window.addEventListener('hashchange', scrollToHash);
        return () => window.removeEventListener('hashchange', scrollToHash);
    }, []);

  return (
    <div className="m-0 pt-12 space-y-16 bg-[#F9F9F9]">
        <h3 className="md:text-3xl text-2xl font-semibold text-black uppercase font-playfair italic text-center">Nuestros servicios</h3>
                <section className="w-full text-black  px-4 sm:px-8 md:px-16 lg:px-8 scroll-mt-24 md:scroll-mt-28" id="registro">
            {/* <h3 className="md:text-3xl text-2xl font-semibold text-center mb-4 font-playfair italic uppercase">Registro de Marca</h3> */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div className="md:order-1 order-2 w-full">
                <Image
                src={registro}
                alt="Registro-marcasoon"
                sizes="(min-width: 1024px) 70vw, (min-width: 768px) 85vw, 96vw"
                className="w-auto md:h-[580px] h-auto rounded-2xl"
                />
            </div> 
            <div className="md:order-2 orden-1 md:pr-22">
                <h3 className="md:text-3xl text-2xl font-semibold mb-4 font-playfair italic">Registro de Marca</h3>
                <ul>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Obtén la Exclusividad: Asegura el derecho legal único sobre tu nombre, logo o eslogan distintivo.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Protección por 10 Años: Tu registro inicial tiene una vigencia de una década, con posibilidad de renovación indefinida.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Activo Comercial: Convierte tu marca en un activo valioso para franquiciar, licenciar y aumentar el valor de tu negocio.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Respaldo Legal: Te entregamos el Título de Registro oficial para defenderte contra el uso no autorizado.</li>
                </ul>
                <Button />
            </div>
            </div>
        </section>
    <section className="w-full text-black px-4 sm:px-8 md:px-16 lg:px-8 scroll-mt-24 md:scroll-mt-28" id="documentos">
            {/* <h3 className="md:text-3xl text-2xl font-semibold text-center mb-4 font-playfair italic uppercase">Registro de Marca</h3> */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div className="md:order-2 order-1 w-full">
                <Image
                src={documentos}
                alt="documentos-marcasoon"
                sizes="(min-width: 1024px) 70vw, (min-width: 768px) 85vw, 96vw"
                className="w-auto md:h-[580px] h-auto rounded-2xl"
                />
            </div> 
            <div className="md:order-1 orden-2 md:pl-22">
                <h3 className="md:text-3xl text-2xl font-semibold mb-4 font-playfair italic">Documentos para el Registro y Solicitudes</h3>
                <ul>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Clasificación Correcta: Asesoría experta para clasificar tus productos/servicios según la normativa internacional (Clasificación de Niza).</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Gestión Integral de Solicitudes: Nos encargamos de completar y presentar toda la documentación técnica y legal requerida.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Seguimiento Proactivo: Gestionamos todas las notificaciones y posibles requerimientos de la oficina de registro hasta la concesión final.</li>
                </ul>
                <Button />
            </div>
            </div>
        </section>
        
    <section className="w-full text-black px-4 sm:px-8 md:px-16 lg:px-8 scroll-mt-24 md:scroll-mt-28" id="patentes">
            {/* <h3 className="md:text-3xl text-2xl font-semibold text-center mb-4 font-playfair italic uppercase">Registro de Marca</h3> */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div className="md:order-1 order-2 w-full">
                <Image
                src={patente}
                alt="Registro-patente"
                sizes="(min-width: 1024px) 70vw, (min-width: 768px) 85vw, 96vw"
                className="w-auto md:h-[580px] h-auto rounded-2xl"
                />
            </div> 
            <div className="md:order-2 orden-1 md:pr-22">
                <h3 className="md:text-3xl text-2xl font-semibold mb-4 font-playfair italic">Registro de Copyrights y Patentes</h3>
                <ul>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Registro de Copyright (Derechos de Autor): Protege la expresión original de tus obras creativas (libros, software, música, arte, contenido web).</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Registro de Patentes: Protege tus invenciones o soluciones técnicas novedosas (productos o procesos) para obtener un monopolio temporal de explotación.",</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Protección 360°: Aseguramos legalmente tanto tu identidad comercial como tu innovación técnica y artística.</li>
                </ul>
                <Button />
            </div>
            </div>
        </section>
    {/* Última sección: eliminamos el espacio en blanco antes del footer anulando el margin-top del footer (mt-16) con un margin-bottom negativo */}
    <section className="w-full text-black px-4 sm:px-8 md:px-16 lg:px-8  mb-16 pb-12 scroll-mt-24 md:scroll-mt-28" id="busqueda-monitoreo-mantenimiento">
            {/* <h3 className="md:text-3xl text-2xl font-semibold text-center mb-4 font-playfair italic uppercase">Registro de Marca</h3> */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div className="md:order-2 order-1 w-full">
                <Image
                src={busqueda}
                alt="busqueda-monitoreo-mantenimiento"
                sizes="(min-width: 1024px) 70vw, (min-width: 768px) 85vw, 96vw"
                className="w-auto md:h-[580px] h-auto rounded-2xl"
                />
            </div> 
            <div className="md:order-1 orden-2 md:pl-22">
                <h3 className="md:text-3xl text-2xl font-semibold mb-4 font-playfair italic">Búsqueda, Monitoreo y Mantenimiento</h3>
                <ul>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Búsqueda de Viabilidad: Realizamos un análisis de anterioridad exhaustivo antes de registrar para confirmar que tu marca sea única y evitar rechazos costosos.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Monitoreo Continuo: Vigilamos activamente los registros y el uso en el mercado para detectar imitadores o marcas conflictivas a tiempo.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Mantenimiento y Renovación: Gestionamos automáticamente los trámites periódicos y las renovaciones necesarias para garantizar que tu protección legal nunca caduque.</li>
                </ul>
                <Button />
            </div>
            </div>
        </section>
        <section className="w-full text-black px-4 sm:px-8 md:px-16 lg:px-8 bg-[#F9F9F9] -mb-16 pb-12 scroll-mt-24 md:scroll-mt-28" id="protocolo-madrid">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div className="md:order-1 order-2 w-full">
                <Image
                src={protocolo}
                alt="protocolo-madrid"
                sizes="(min-width: 1024px) 70vw, (min-width: 768px) 85vw, 96vw"
                className="w-auto md:h-[580px] h-auto rounded-2xl"
                />
            </div> 
            <div className="md:order-2 orden-1 md:pl-22 space-y-4">
                <h3 className="md:text-3xl text-2xl font-semibold mb-4 font-playfair italic">Protocolo de Madrid</h3>
                <p> <span className="font-semibold">El Protocolo de Madrid</span> es un sistema internacional que permite <span className="font-semibold">registrar una marca en varios países con un solo trámite</span>, haciendo todo mucho más simple y eficiente. <span className="font-semibold">Cómo funciona con Marcasoon:</span></p>
                <ul>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Primero, solicitamos tu marca en los Estados Unidos.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Seguidamente iniciamos el proceso internacional bajo el Protocolo de Madrid, extendiendo la protección a más de 130 países miembros del sistema.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />La Oficina Internacional revisa tu solicitud y la envía a los países elegidos. Cada país evalúa la marca según sus propias leyes.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Una vez cumplimentado cada proceso, tu marca quedara protegida en todos esos países, sin tener que hacer trámites separados en cada uno.</li>
                </ul>
                <p><span className="font-semibold">Beneficios:</span></p>
                <ul>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Ahorro de tiempo y dinero: un solo formulario, un solo pago, una sola estrategia global.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Cobertura internacional rápida: protege tu marca en múltiples países a la vez.</li>
                    <li className="flex items-start mt-2 gap-2"><Asterisk className="flex-shrink-0 mt-0.5 w-5 h-5 text-[#192A56]" />Gestión sencilla: cualquier cambio, modificación o renovación se hace desde Marcasoon.</li>
                </ul>
                <Button />
            </div>
            </div>
        </section>
    </div>
  );
};
export default ServicesPage;