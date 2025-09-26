"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp } from 'lucide-react';
import LogoComponent from "./LogoComponent";

function NavComponent() {
 const [isServicesOpen, setIsServicesOpen] = useState(false);
 const [isResourcesOpen, setIsResourcesOpen] = useState(false);
 
  return (
    <nav className=" border-[#192A56] shadow-[#192a5667] shadow-lg py-4 flex  w-full sticky top-0 z-50 bg-white">
        <div className="flex gap-4 text-black justify-evenly w-full">
            <LogoComponent />
            <p><a href="/">Inicio</a></p>
            <div
              className="relative"
              onClick={() => {setIsServicesOpen(!isServicesOpen)
                             setIsResourcesOpen(false);}
              }
            >
              <p className="cursor-pointer">Servicios {isServicesOpen ? <ChevronUp className="inline w-4 h-4" /> : <ChevronDown className="inline w-4 h-4" />}</p>
              {isServicesOpen && (
                <div className="absolute top-full left-0 mt-0.5 w-48 bg-white rounded-md shadow-lg z-10 border border-[#192A56]  p-0.5">
                  <a href="/servicios/registro" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Registro de Marca</a>
                  <a href="/servicios/busqueda" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Búsqueda Fonética</a>
                  <a href="/servicios/consultoria" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Consultoría Legal</a>
                </div>
              )}
            </div>

            <div
              className="relative"
              onClick={() => {setIsResourcesOpen(!isResourcesOpen)
                              setIsServicesOpen(false);}
              }
            >
              <p className="cursor-pointer">Recursos {isResourcesOpen ? <ChevronUp className="inline w-4 h-4" /> : <ChevronDown className="inline w-4 h-4" />}</p>
              {isResourcesOpen && (
                <div className="absolute top-full border-[#192A56] left-0 mt-0.5 w-48 bg-white rounded-md shadow-lg z-10 border-1 p-0.5">
                  <a href="/recursos/blog" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Blog</a>
                  <a href="/recursos/guides" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Guías</a>
                  <a href="/recursos/webinars" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Webinars</a>
                </div>
              )}
            </div>

            <p><a href="/about">Sobre nosotros</a></p>
            <p><a href="/contact">Contacto</a></p>
        </div>
    </nav>
  );
}

export default NavComponent;