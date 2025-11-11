"use client";

import { useEffect, useRef } from "react";
import { X, CreditCard, Wallet } from "lucide-react";

interface Props {
  open: boolean;
  onClose: () => void;
  onSelect: (method: "stripe" | "paypal") => void | Promise<void>;
}

export default function PaymentMethodModal({ open, onClose, onSelect }: Props) {
  const dialogRef = useRef<HTMLDivElement | null>(null);

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
        className="relative w-[90vw] sm:w-[70vw] md:w-[50vw] lg:w-[40vw] max-w-lg bg-white text-black rounded-2xl shadow-xl p-6 md:p-8 focus:outline-none max-h-[80vh] overflow-y-auto"
        tabIndex={-1}
      >
        <button onClick={onClose} aria-label="Close" className="absolute text-[#ED5E32] right-3 top-3 p-2 rounded-full bg-white/80 hover:bg-white shadow hover:cursor-pointer">
          <X className="w-5 h-5" />
        </button>
        <h3 className="text-xl md:text-2xl font-semibold mb-2">Elige tu método de pago</h3>
        <p className="text-sm text-gray-600 mb-6">Selecciona cómo deseas continuar con el pago del plan.</p>

        <div className="grid grid-cols-1 gap-4">
          <button
            onClick={() => onSelect("stripe")}
            className="group flex items-center gap-4 border rounded-xl p-5 hover:shadow-md transition cursor-pointer text-left"
          >
            <div className="flex items-center justify-center w-14 h-14 rounded-lg bg-[#6772e5]/10 group-hover:bg-[#6772e5]/20">
              <CreditCard className="w-7 h-7 text-[#6772e5]" />
            </div>
            <div className="flex-1">
              <div className="font-semibold text-[#222]">Stripe</div>
              <div className="text-xs text-gray-500">Tarjeta de crédito / débito y métodos adicionales.</div>
            </div>
          </button>

          <button
            onClick={() => onSelect("paypal")}
            className="group flex items-center gap-4 border rounded-xl p-5 hover:shadow-md transition cursor-pointer text-left"
          >
            <div className="flex items-center justify-center w-14 h-14 rounded-lg bg-[#FFC439]/20 group-hover:bg-[#FFC439]/30">
              <Wallet className="w-7 h-7 text-[#003087]" />
            </div>
            <div className="flex-1">
              <div className="font-semibold text-[#222]">PayPal</div>
              <div className="text-xs text-gray-500">Usa tu cuenta PayPal para un pago rápido y seguro.</div>
            </div>
          </button>
        </div>

        <div className="flex justify-end mt-8">
          <button onClick={onClose} className="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-sm hover:cursor-pointer">Cancelar</button>
        </div>
      </div>
    </div>
  );
}