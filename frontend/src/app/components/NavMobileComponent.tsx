"use client";

import { useState } from 'react';
import { Menu, X, ChevronDown, ChevronUp } from 'lucide-react';
import LogoComponent from './LogoComponent';

const NavMobileComponent = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isServicesOpen, setIsServicesOpen] = useState(false);
  const [isResourcesOpen, setIsResourcesOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
  <nav className="bg-white shadow-md w-full md:hidden sticky top-0 z-50">
      {/* Barra superior visible */}
      <div className="flex items-center justify-between p-4">
        <LogoComponent />
        <button onClick={toggleMenu} className="text-[#192A56]">
          {isMenuOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Menú desplegable */}
      {isMenuOpen && (
        <div className="absolute top-full left-0 w-full bg-white shadow-lg py-4 px-5 z-50">
          <ul className="flex flex-col gap-4">
            <li>
              <a href="/" className="text-lg text-gray-700 hover:text-[#192A56]">Inicio</a>
            </li>
            
            {/* Sub-menú Servicios */}
            <li>
              <div onClick={() => setIsServicesOpen(!isServicesOpen)} className="flex justify-between items-center cursor-pointer">
                <span className="text-lg text-gray-700 hover:text-[#192A56]">Servicios</span>
                {isServicesOpen ? <ChevronUp className='w-4 h-4 text-black'/> : <ChevronDown className='w-4 h-4 text-black'/>}
              </div>
              {isServicesOpen && (
                <ul className="pl-4 mt-2 flex flex-col gap-2">
                  <li><a href="/servicios/registro" className="text-gray-600 hover:text-black">Registro de Marca</a></li>
                  <li><a href="/servicios/busqueda" className="text-gray-600 hover:text-black">Búsqueda Fonética</a></li>
                  <li><a href="/servicios/consultoria" className="text-gray-600 hover:text-black">Consultoría Legal</a></li>
                </ul>
              )}
            </li>

            {/* Sub-menú Recursos */}
            <li>
              <div onClick={() => setIsResourcesOpen(!isResourcesOpen)} className="flex justify-between items-center cursor-pointer">
                <span className="text-lg text-gray-700 hover:text-[#192A56]">Recursos</span>
                {isResourcesOpen ? <ChevronUp className='w-4 h-4 text-black'/> : <ChevronDown className='w-4 h-4 text-black'/>}
              </div>
              {isResourcesOpen && (
                <ul className="pl-4 mt-2 flex flex-col gap-2">
                  <li><a href="/recursos/blog" className="text-gray-600 hover:text-black">Blog</a></li>
                  <li><a href="/recursos/guias" className="text-gray-600 hover:text-black">Guías</a></li>
                  <li><a href="/recursos/webinars" className="text-gray-600 hover:text-black">Webinars</a></li>
                </ul>
              )}
            </li>

            <li>
              <a href="/about" className="text-lg text-gray-700 hover:text-[#192A56]">Sobre nosotros</a>
            </li>
            <li>
              <a href="/contact" className="text-lg text-gray-700 hover:text-[#192A56]">Contacto</a>
            </li>
          </ul>
        </div>
      )}
    </nav>
  );
};

export default NavMobileComponent;