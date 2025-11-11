"use client";

import { useState } from "react";
import { ChevronDown } from 'lucide-react';
import LogoComponent from "./LogoComponent";
import UserMenu from "./auth/UserMenu";
import AuthModal from "./auth/AuthModal";
import { useEffect } from "react";
import Link from "next/link";
import Select, { components, type StylesConfig } from "react-select";
import { useRouter } from "next/navigation";
import { fetchCurrentUser, getStoredAccessToken, setStoredUsername } from "../../../api/api";
import userImg from "../../../public/user.png";

function NavComponent() {
 // Menús reemplazados por Select animados de react-select
 const [showAuth, setShowAuth] = useState(false);
 const [authed, setAuthed] = useState(false);
 const [displayName, setDisplayName] = useState<string>("");
 const router = useRouter();

 // Helper local para evitar fetch a /auth/me
 const hasStoredToken = () => {
   if (typeof window === 'undefined') return false;
   return !!(localStorage.getItem('access') || sessionStorage.getItem('access'));
 };

 useEffect(() => {
  // helper: precargar icono de usuario
  const preloadIcon = () => {
    if (typeof window === 'undefined') return;
    const img = new Image();
    img.src = (userImg as any).src || (userImg as any);
  };

  const hydrateUser = async () => {
    const token = getStoredAccessToken();
    if (!token) return;
    try {
      const me = await fetchCurrentUser(undefined, token);
      if (me?.username) {
        setDisplayName(me.username);
        setStoredUsername(me.username, true);
      }
    } catch {}
  };

  // Estado inicial basado solo en tokens
  const ok = hasStoredToken();
  setAuthed(ok);
  if (ok) {
    preloadIcon();
    hydrateUser();
  }

  const handler = (e: Event) => {
    const det: any = (e as CustomEvent).detail;
    if (typeof det?.authed === 'boolean') {
      setAuthed(det.authed);
      if (det.authed) {
        preloadIcon();
        hydrateUser();
      } else {
        setDisplayName("");
      }
    }
  };
  window.addEventListener('auth-changed', handler as EventListener);
  return () => window.removeEventListener('auth-changed', handler as EventListener);
 }, []);
 
  return (
    <nav className=" border-[#192A56] shadow-[#192a5667] shadow-lg py-4 flex  w-full sticky top-0 z-50 bg-white">
      <div className="flex gap-4 text-black justify-evenly w-full items-center">
            <LogoComponent />
            <p className="text-[#192A56] font-semibold"><Link href="/">Inicio</Link></p>
            {/* Select Servicios */}
            <div className="min-w-[180px]">
              <NavSelect
                placeholder="Servicios"
                options={[
                  { label: "Registro de Marca", href: "/servicios/#registro" },
                  { label: "Consultoría Legal", href: "/servicios/#documentos" },
                  { label: "Registro de Patentes", href: "/servicios/#patentes" },
                  { label: "Búsqueda Fonética", href: "/servicios/#busqueda-monitoreo-mantenimiento" },
                ]}
                onNavigate={(href) => router.push(href)}
              />
            </div>

            {/* Select Recursos */}
            <div className="min-w-[160px]">
              <NavSelect
                placeholder="Recursos"
                options={[
                  { label: "Blog", href: "/recursos/blog" },
                  { label: "Guías", href: "/recursos/guides" },
                  { label: "Webinars", href: "/recursos/webinars" },
                ]}
                onNavigate={(href) => router.push(href)}
              />
            </div>

            <p className="text-[#192A56] font-semibold"><a href="/about">Sobre nosotros</a></p>
            <p className="text-[#192A56] font-semibold"><a href="/contact">Contacto</a></p>
            {authed ? (
              <UserMenu initialName={displayName} />
            ) : (
              <button
                onClick={() => setShowAuth(true)}
                className="px-4 py-2 text-sm font-semibold rounded-lg border border-[#192A56] text-[#192A56] hover:bg-[#192A56] hover:text-white transition hover:cursor-pointer"
              >
                Iniciar sesión
              </button>
            )}
        </div>
        {showAuth && (
            <AuthModal
              open={showAuth}
              initialTab="login"
              onClose={() => setShowAuth(false)}
              onSuccess={async (type) => {
                // Ya se disparó evento auth-changed desde el modal; aseguramos estado inmediato
                setAuthed(true);
                setShowAuth(false);
              }}
            />
        )}
    </nav>
  );
}

export default NavComponent;

// Tipos y componentes para react-select en el Nav
type NavOption = { label: string; href: string };

const DropdownIndicator = (props: any) => {
  const { selectProps } = props;
  const isOpen = !!selectProps.menuIsOpen;
  return (
    <components.DropdownIndicator {...props}>
      <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
    </components.DropdownIndicator>
  );
};

const selectStyles: StylesConfig<NavOption, false> = {
  control: (base, state) => ({
    ...base,
    minHeight: 36,
    height: 36,
    borderRadius: 8,
    borderColor: 'transparent',
    boxShadow: 'none',
    backgroundColor: 'transparent',
    ':hover': { borderColor: 'transparent' },
    cursor: 'pointer',
  }),
  valueContainer: (base) => ({ ...base, padding: '0 5px' }),
  placeholder: (base) => ({ ...base, color: '#192A56', fontWeight: 600 }),
  singleValue: (base) => ({ ...base, color: '#192A56', fontWeight: 600 }),
  indicatorSeparator: () => ({ display: 'none' }),
  dropdownIndicator: (base) => ({ ...base, color: '#192A56' }),
  menu: (base) => ({
    ...base,
    zIndex: 60,
    border: 'none',
    boxShadow: '0 10px 20px rgba(25,42,86,0.15)',
  }),
  option: (base, state) => ({
    ...base,
    cursor: 'pointer',
    backgroundColor: state.isFocused ? '#f3f4f6' : 'white',
    color: '#111827',
  }),
};

function NavSelect({ placeholder, options, onNavigate }: { placeholder: string; options: NavOption[]; onNavigate: (href: string) => void; }) {
  return (
    <Select<NavOption, false>
      instanceId={placeholder}
      classNamePrefix="nav-select"
      isSearchable={false}
      placeholder={placeholder}
      options={options}
      value={null}
      onChange={(opt) => { if (opt) onNavigate(opt.href); }}
      components={{ DropdownIndicator, IndicatorSeparator: () => null }}
      styles={selectStyles}
      menuPlacement="auto"
    />
  );
}