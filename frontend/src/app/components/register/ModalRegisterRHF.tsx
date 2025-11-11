"use client";

import { useEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import { X, Mail, Phone, User2, Quote, Image as ImageIcon, Music2, Type, AtSign, Lock } from "lucide-react";
import { FormValues, ProtectType, SubmitPayload } from "@/app/interfaces/inputs";
import { registerUserAPI, obtainTokenPair, storeTokens } from "../../../../api/api";

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit?: (payload: SubmitPayload) => void | Promise<void>;
}

export default function ModalRegisterRHF({ open, onClose, onSubmit }: Props) {
  const dialogRef = useRef<HTMLDivElement | null>(null);

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

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  useEffect(() => {
    if (open) setTimeout(() => dialogRef.current?.focus(), 0);
  }, [open]);

  const onSubmitForm = async (values: FormValues) => {
    const phone = values.phoneLocal ? `${values.countryCode} ${values.phoneLocal}` : "";
    const selections = values.protect || [];
    const normalizedProtect: SubmitPayload["protect"] =
      selections.length === 1 ? selections[0] : selections.map((t) => ({ type: t }));

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
      // 1. Registrar usuario
      await registerUserAPI(payload);
      // 2. Obtener tokens JWT
      const tokens = await obtainTokenPair({ username: payload.username, password: payload.password });
      storeTokens(tokens, true);
      // 3. Callback opcional por si el padre quiere reaccionar
      await onSubmit?.(payload);
      // 4. TODO: abrir modal de selección de pago (emitir evento o estado externo)
    } catch (e: any) {
      console.error("Register or login failed", e?.message || e);
      // Podríamos mostrar un toast / mensaje de error aquí (no implementado aún)
      return; // No cerramos si falla
    }

    reset();
    onClose();
  };

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

  <h3 className="text-xl md:text-2xl font-semibold mb-1">¡Regístrate para poder ponernos en contacto!</h3>
        <p className="text-sm text-gray-600 mb-6">Su información será privada y confidencial, no compartiremos sus datos.</p>

        <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-5">
          {/* First / Last name */}
          <div>
            <label className="block text-sm font-medium mb-1">Nombre y Apellido <span className="text-red-600">*</span></label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="relative">
                <User2 className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Nombre"
                  className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none"
                  {...register("firstName", { required: "Required field." })}
                />
                {errors.firstName && <p className="text-xs text-red-600 mt-1">{errors.firstName.message}</p>}
              </div>
              <div className="relative">
                <User2 className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Apellido"
                  className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none"
                  {...register("lastName", { required: "Required field." })}
                />
                {errors.lastName && <p className="text-xs text-red-600 mt-1">{errors.lastName.message}</p>}
              </div>
            </div>
          </div>

          {/* Passwords */}
          <div>
            <label className="block text-sm font-medium mb-1">Contraseña <span className="text-red-600">*</span></label>
            <div className="relative mb-2">
              <Lock className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                placeholder="Ingresa tu contraseña"
                className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none"
                {...register("password", {
                  required: "Required field.",
                  minLength: { value: 8, message: "Mínimo 8 caracteres." },
                  validate: (v) => /[A-Za-z]/.test(v) && /\d/.test(v) || "Debe incluir letras y números.",
                })}
              />
            </div>
            {errors.password && <p className="text-xs text-red-600 mt-1">{String(errors.password.message)}</p>}

            <label className="block text-sm font-medium mb-1 mt-4">Confirmar contraseña <span className="text-red-600">*</span></label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                placeholder="Repite tu contraseña"
                className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none"
                {...register("confirmPassword", {
                  required: "Required field.",
                  validate: (v) => v === watch("password") || "Las contraseñas no coinciden.",
                })}
              />
            </div>
            {errors.confirmPassword && <p className="text-xs text-red-600 mt-1">{String(errors.confirmPassword.message)}</p>}
          </div>

          {/* Username */}
          <div>
            <label className="block text-sm font-medium mb-1">Username <span className="text-red-600">*</span></label>
            <div className="relative">
              <AtSign className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Tu usuario"
                className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none"
                {...register("username", {
                  required: "Required field.",
                  minLength: { value: 3, message: "At least 3 characters." },
                })}
              />
            </div>
            {errors.username && <p className="text-xs text-red-600 mt-1">{errors.username.message}</p>}
          </div>

          {/* Phone */}
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
              <input
                type="tel"
                inputMode="tel"
                placeholder="Número de teléfono"
                className="text-black flex-1 border border-[#ED5E32] rounded-lg px-3 py-2 focus:outline-none"
                {...register("phoneLocal")}
              />
            </div>
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-medium mb-1">Correo electrónico <span className="text-red-600">*</span></label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                placeholder="Ingresa tu correo electrónico"
                className="text-black w-full border border-[#ED5E32] rounded-lg pl-9 pr-3 py-2 focus:outline-none"
                {...register("email", {
                  required: "Required field.",
                  pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: "Enter a valid email." },
                })}
              />
            </div>
            {errors.email && <p className="text-xs text-red-600 mt-1">{errors.email.message}</p>}
          </div>

          {/* What are you trying to protect? */}
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
                  <label
                    key={key}
                    className={`flex items-center gap-3 border rounded-xl p-4 cursor-pointer transition hover:shadow-sm ${selected ? "border-[#192A56] ring-1 ring-[#192A56]" : "border-gray-200"}`}
                  >
                    <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100 text-gray-700">
                      <Icon className="w-6 h-6" />
                    </div>
                    <div className="flex-1">
                      <div className="font-semibold">{title}</div>
                      <div className="text-xs text-gray-500">{subtitle}</div>
                    </div>
                    <input
                      type="checkbox"
                      className="w-5 h-5 accent-[#ED5E32]"
                      value={key}
                      {...register("protect", { validate: (v) => (v && v.length > 0) || "Campo obligatorio. Seleccione una opción." })}
                    />
                  </label>
                );
              })}
            </div>
            {errors.protect && (
              <p className="text-xs text-red-600 mt-2">{String(errors.protect.message || "Campo obligatorio. Seleccione una opción.")}</p>
            )}
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button type="button" onClick={onClose} className="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50">Cancelar</button>
            <button type="submit" className="px-5 py-2 rounded-lg bg-[#ED5E32] text-white font-semibold hover:opacity-90">Continuar</button>
          </div>
        </form>
      </div>
    </div>
  );
}
