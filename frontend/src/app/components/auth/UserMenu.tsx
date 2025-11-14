"use client";

import Image from "next/image";
import userImg from "../../../../public/user.png";
import { useEffect, useRef, useState } from "react";
import { ChevronDown, LogOut } from "lucide-react";
import { logoutAll, getStoredUsername, fetchCurrentUser, getStoredAccessToken } from "../../../../api/api";
import Select, { components, type StylesConfig } from "react-select";
interface Props { initialName?: string }

export default function UserMenu({ initialName }: Props) {
  const [authed, setAuthed] = useState(false);
  const [displayName, setDisplayName] = useState<string>(initialName || "");
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const hasToken = () => {
      if (typeof window === 'undefined') return false;
      return !!(localStorage.getItem('access') || sessionStorage.getItem('access'));
    };

    const hydrateFromAPI = async () => {
      const token = getStoredAccessToken();
      if (!token) return;
      try {
        const user = await fetchCurrentUser(undefined, token);
        if (user?.username) {
          setDisplayName(user.username);
        } else {
          const stored = getStoredUsername();
          setDisplayName(stored || 'Usuario');
        }
      } catch (e) {
        // Si falla usamos storage como fallback
        const stored = getStoredUsername();
        setDisplayName(stored || 'Usuario');
      }
    };

    const init = async () => {
      const ok = hasToken();
      setAuthed(ok);
      if (ok) {
        if (initialName && initialName.length > 0) {
          setDisplayName(initialName);
          return;
        }
        await hydrateFromAPI();
      }
    };
    init();

    const handler = async (e: Event) => {
      const det: any = (e as CustomEvent).detail;
      if (det?.authed) {
        setAuthed(true);
        if (initialName && initialName.length > 0) {
          setDisplayName(initialName);
        } else {
          await hydrateFromAPI();
        }
      } else {
        setAuthed(false);
        setDisplayName('');
      }
    };
    window.addEventListener('auth-changed', handler as EventListener);
    return () => window.removeEventListener('auth-changed', handler as EventListener);
  }, []);

  if (!authed) return null;

  // Estilos consistentes con los selects del Nav
  const selectStyles: StylesConfig<{ label: string; value: string }, false> = {
    control: (base) => ({
      ...base,
      minHeight: 36,
      height: 36,
      borderRadius: 9999,
      borderColor: 'transparent',
      boxShadow: 'none',
      backgroundColor: 'transparent',
      ':hover': { borderColor: 'transparent' },
      cursor: 'pointer',
    }),
    valueContainer: (base) => ({ ...base, padding: '0 6px' }),
    placeholder: (base) => ({ ...base, color: '#111827' }),
    indicatorSeparator: () => ({ display: 'none' }),
    dropdownIndicator: (base) => ({ ...base, color: '#111827' }),
    menu: (base) => ({
      ...base,
      zIndex: 60,
      border: 'none',
      boxShadow: '0 10px 20px rgba(25,42,86,0.15)'
    }),
    option: (base, state) => ({
      ...base,
      cursor: 'pointer',
      backgroundColor: state.isFocused ? '#f3f4f6' : 'white',
      color: '#111827',
    })
  };

  const DropdownIndicator = (props: any) => {
    const { selectProps } = props;
    const isOpen = !!selectProps.menuIsOpen;
    return (
      <components.DropdownIndicator {...props}>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </components.DropdownIndicator>
    );
  };

  const Placeholder = (props: any) => (
    <components.Placeholder {...props}>
      <span className="flex items-center gap-2">
        <Avatar displayName={displayName} />
        <span className="hidden md:block text-sm font-medium">{displayName || 'Usuario'}</span>
      </span>
    </components.Placeholder>
  );

  const options = [
    { label: 'Salir', value: 'logout' },
  ];

  return (
    <div className="relative" ref={ref}>
      <Select<{ label: string; value: string }, false>
        instanceId="user-menu"
        isSearchable={false}
        value={null}
        placeholder={displayName || 'Usuario'}
        options={options}
        onChange={async (opt) => {
          if (!opt) return;
          if (opt.value === 'logout') {
            await logoutAll();
            if (typeof window !== 'undefined') {
              window.dispatchEvent(new CustomEvent('auth-changed', { detail: { authed: false } }));
            }
            setAuthed(false);
            location.reload();
          }
        }}
        components={{ DropdownIndicator, IndicatorSeparator: () => null, Placeholder }}
        styles={selectStyles}
        menuPlacement="bottom"
      />
    </div>
  );
}

function Avatar({ displayName }: { displayName: string }) {
  const [imgError, setImgError] = useState(false);
  const initial = (displayName || 'U').trim().charAt(0).toUpperCase();
  if (imgError) {
    return (
      <span className="w-8 h-8 rounded-full bg-[#192A56] text-white flex items-center justify-center text-sm font-semibold">
        {initial}
      </span>
    );
  }
  return (
    <span className="relative w-8 h-8">
      <Image src={userImg} alt="user" fill className="rounded-full object-cover" onError={() => setImgError(true)} />
    </span>
  );
}
