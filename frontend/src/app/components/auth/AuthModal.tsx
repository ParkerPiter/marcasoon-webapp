"use client";

import { useEffect, useRef, useState } from "react";
import { X, Mail, Phone, User2, Quote, Image as ImageIcon, Music2, Type, AtSign, Lock } from "lucide-react";
import { useForm } from "react-hook-form";
import { FormValues, ProtectType, SubmitPayload } from "@/app/interfaces/inputs";
import { loginBasic, loginJWT, registerUserAPI, storeTokens, loginAndStoreToken, setStoredUsername } from "../../../../api/api";
import Loader from "../Loader";

interface Props {
  open: boolean;
  onClose: () => void;
  initialTab?: "login" | "register";
  onSuccess?: (type: "login" | "register") => void | Promise<void>;
}

export default function AuthModal({ open, onClose, initialTab = "login", onSuccess }: Props) {
  const [tab, setTab] = useState<"login" | "register">(initialTab);
  const dialogRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => { setTab(initialTab) }, [initialTab]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  useEffect(() => { if (open) setTimeout(() => dialogRef.current?.focus(), 0); }, [open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        className="relative w-[95vw] sm:w-[90vw] md:w-[80vw] lg:w-[70vw] max-w-2xl bg-white text-black rounded-2xl shadow-xl p-5 md:p-8 focus:outline-none max-h-[90vh] overflow-y-auto"
        tabIndex={-1}
      >
        <button onClick={onClose} aria-label="Close" className="absolute text-[#ED5E32] right-3 top-3 p-2 rounded-full bg-white/80 hover:bg-white shadow hover:cursor-pointer">
          <X className="w-5 h-5" />
        </button>

        <div className="mb-4">
          <div role="tablist" aria-label="Opciones de autenticación" className="relative grid grid-cols-2 bg-gray-100 rounded-xl p-1">
            {/* Indicador deslizante */}
            <span
              aria-hidden
              className={`absolute top-1 bottom-1 w-1/2 rounded-lg bg-white shadow transition-transform duration-200 ease-out pointer-events-none`}
              style={{ transform: tab === 'login' ? 'translateX(0%)' : 'translateX(100%)' }}
            />

            <button
              role="tab"
              aria-selected={tab === 'login'}
              className={`relative z-10 px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${tab === 'login' ? 'text-[#ED5E32]' : 'text-gray-600'} hover:cursor-pointer`}
              onClick={() => setTab('login')}
            >
              Iniciar sesión
            </button>
            <button
              role="tab"
              aria-selected={tab === 'register'}
              className={`relative z-10 px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${tab === 'register' ? 'text-[#ED5E32]' : 'text-gray-600'} hover:cursor-pointer`}
              onClick={() => setTab('register')}
            >
              Crear cuenta
            </button>
          </div>
        </div>

        {tab === 'login' ? (
          <LoginPanel onSuccess={async () => { await onSuccess?.('login'); onClose(); }} />
        ) : (
          <RegisterPanel onSuccess={async () => { await onSuccess?.('register'); onClose(); }} />
        )}
      </div>
    </div>
  );
}

function LoginPanel({ onSuccess }: { onSuccess: () => void | Promise<void> }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null); setLoading(true);
    try {
      await loginBasic({ username, password });
      const tokens = await loginJWT({ username, password });
      storeTokens(tokens, true);
      setStoredUsername(username, true);
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('auth-changed', { detail: { authed: true } }));
      }
      // Esperar 1.5s tras la respuesta para mostrar el loader
      await new Promise((r) => setTimeout(r, 1500));
      await onSuccess();
    } catch (err: any) {
      setError("Hubo un error al intentar iniciar sesión");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative">
      {loading && (
        <div className="absolute inset-0 bg-white/70 flex items-center justify-center z-10">
          <Loader />
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
      <h3 className="text-xl md:text-2xl font-semibold">Inicia sesión</h3>
      <div>
        <label className="block text-sm font-medium mb-1">Usuario</label>
        <input type="text" className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]" value={username} onChange={(e) => setUsername(e.target.value)} required />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Contraseña</label>
        <input type="password" className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#ED5E32]" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <button type="submit" disabled={loading} className="w-full bg-[#ED5E32] text-white py-2 rounded-lg font-semibold hover:opacity-90 disabled:opacity-60 hover:cursor-pointer">{loading ? "Ingresando..." : "Ingresar"}</button>
      </form>
    </div>
  );
}

function RegisterPanel({ onSuccess }: { onSuccess: () => void | Promise<void> }) {
  const { register, handleSubmit, watch, formState: { errors }, reset } = useForm<FormValues>({
    defaultValues: {
      firstName: "",
      lastName: "",
      username: "",
      email: "",
      countryCode: "+1",
      phoneLocal: "",
      protect: [],
      password: "",
      confirmPassword: "",
    },
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmitForm = async (values: FormValues) => {
    setError(null);
    setLoading(true);
    const phone = values.phoneLocal ? `${values.countryCode} ${values.phoneLocal}` : "";
    const selections = values.protect || [];
    const normalizedProtect: SubmitPayload["protect"] = selections.length === 1 ? selections[0] : selections.map((t) => ({ type: t }));

    const payload: SubmitPayload = {
      firstName: values.firstName.trim(),
      lastName: values.lastName.trim(),
      username: values.username.trim(),
      email: values.email.trim(),
      phone: phone || undefined,
      protect: normalizedProtect,
      password: values.password,
    };

    try {
      await registerUserAPI(payload);
      await loginAndStoreToken({ username: payload.username, password: payload.password }, true);
      setStoredUsername(payload.username, true);
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('auth-changed', { detail: { authed: true } }));
      }
      // Esperar 1.5s tras la respuesta antes de cerrar
      await new Promise((r) => setTimeout(r, 1500));
      reset();
      await onSuccess();
    } catch (e: any) {
      setError("No se pudo crear la cuenta. Inténtalo nuevamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative">
      {loading && (
        <div className="absolute inset-0 bg-white/70 flex items-center justify-center z-10">
          <Loader />
        </div>
      )}
      <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-5">
      <h3 className="text-xl md:text-2xl font-semibold">Crear cuenta</h3>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="relative">
          <User2 className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input type="text" placeholder="Nombre" className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none" {...register("firstName", { required: "Required field." })} />
          {errors.firstName && <p className="text-xs text-red-600 mt-1">{String(errors.firstName.message)}</p>}
        </div>
        <div className="relative">
          <User2 className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input type="text" placeholder="Apellido" className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none" {...register("lastName", { required: "Required field." })} />
          {errors.lastName && <p className="text-xs text-red-600 mt-1">{String(errors.lastName.message)}</p>}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Username <span className="text-red-600">*</span></label>
        <div className="relative">
          <AtSign className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input type="text" placeholder="Tu usuario" className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none" {...register("username", { required: "Required field.", minLength: { value: 3, message: "At least 3 characters." } })} />
        </div>
        {errors.username && <p className="text-xs text-red-600 mt-1">{String(errors.username.message)}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Número de teléfono <span className="text-gray-500">(opcional)</span></label>
        <div className="flex gap-2">
          <div className="relative">
            <Phone className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <select className="text-black border border-[#ED5E32] rounded-lg pl-9 pr-8 py-2 focus:outline-none" {...register("countryCode")}>
              <option value="+1">🇺🇸 +1</option>
              <option value="+34">🇪🇸 +34</option>
              <option value="+54">🇦🇷 +54</option>
              <option value="+52">🇲🇽 +52</option>
              <option value="+57">🇨🇴 +57</option>
              <option value="+58">🇻🇪 +58</option>
            </select>
          </div>
          <input type="tel" inputMode="tel" placeholder="Número de teléfono" className="text-black flex-1 border border-[#ED5E32] rounded-lg px-3 py-2 focus:outline-none" {...register("phoneLocal")} />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Correo electrónico <span className="text-red-600">*</span></label>
        <div className="relative">
          <Mail className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input type="email" placeholder="Ingresa tu correo electrónico" className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none" {...register("email", { required: "Required field.", pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: "Enter a valid email." } })} />
        </div>
        {errors.email && <p className="text-xs text-red-600 mt-1">{String(errors.email.message)}</p>}
      </div>

        <div>
            <label className="block text-sm font-medium mb-1">Contraseña <span className="text-red-600">*</span></label>
            <div className="relative mb-2">
                <Lock className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
                <input type="password" placeholder="Ingresa tu contraseña" className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none" {...register("password", { required: "Required field.", minLength: { value: 8, message: "Mínimo 8 caracteres." }, validate: (v) => /[A-Za-z]/.test(v) && /\d/.test(v) || "Debe incluir letras y números.", })} />
            </div>
            {errors.password && <p className="text-xs text-red-600 mt-1">{String(errors.password.message)}</p>}

            <label className="block text-sm font-medium mb-1 mt-4">Confirmar contraseña <span className="text-red-600">*</span></label>
            <div className="relative">
                <Lock className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
                <input type="password" placeholder="Repite tu contraseña" className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none" {...register("confirmPassword", { required: "Required field.", validate: (v) => v === watch("password") || "Las contraseñas no coinciden.", })} />
            </div>
            {errors.confirmPassword && <p className="text-xs text-red-600 mt-1">{String(errors.confirmPassword.message)}</p>}
        </div>

      <div>
        <p className="text-sm font-medium mb-2">¿Qué estás tratando de proteger? <span className="text-red-600">*</span></p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {[
            { key: "name", title: "Nombre", subtitle: "Nombre comercial que identifica tu marca", Icon: Type },
            { key: "logo", title: "Logo", subtitle: "Diseño gráfico que identifica tu marca", Icon: ImageIcon },
            { key: "slogan", title: "Slogan", subtitle: "Frase corta que identifica tu marca", Icon: Quote },
            { key: "sound", title: "Sonido", subtitle: "Sonidos únicos que identifican tu marca", Icon: Music2 },
          ].map(({ key, title, subtitle, Icon }) => {
            const selected = (watch("protect") || []).includes(key as ProtectType);
            return (
              <label key={key} className={`flex items-center gap-3 border rounded-xl p-4 cursor-pointer transition hover:shadow-sm ${selected ? "border-[#192A56] ring-1 ring-[#192A56]" : "border-gray-200"}`}>
                <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100 text-gray-700"><Icon className="w-6 h-6" /></div>
                <div className="flex-1">
                  <div className="font-semibold">{title}</div>
                  <div className="text-xs text-gray-500">{subtitle}</div>
                </div>
                <input type="checkbox" className="w-5 h-5 accent-[#ED5E32]" value={key} {...register("protect", { validate: (v) => (v && v.length > 0) || "Campo obligatorio. Seleccione una opción." })} />
              </label>
            );
          })}
        </div>
        {errors.protect && <p className="text-xs text-red-600 mt-2">{String(errors.protect.message || "Campo obligatorio. Seleccione una opción.")}</p>}
      </div>

      <div className="flex items-center justify-end gap-3 pt-2">
        <button type="submit" disabled={loading} className="px-5 py-2 rounded-lg bg-[#ED5E32] text-white font-semibold hover:opacity-90 disabled:opacity-60 hover:cursor-pointer">{loading ? "Creando cuenta..." : "Crear cuenta"}</button>
      </div>
      </form>
    </div>
  );
}
