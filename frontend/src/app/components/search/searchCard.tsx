"use client";

import { SearchCard as SearchCardProps } from "@/app/interfaces/card";

export default function SearchCard({
  logo,
  liveOrDeadStatus,
  correspondenceName,
  transactionDate,
}: SearchCardProps) {
  const isLive = liveOrDeadStatus === "Live";
  return (
    <div className="border border-gray-200 rounded-lg shadow-sm bg-white overflow-hidden w-full max-w-md">
      <div className="p-4 flex items-start gap-4">
        <div className="flex-shrink-0">
          {/* Usamos <img> para evitar configurar dominios remotos en next/image */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={logo}
            alt="Logo de la marca"
            className="h-16 w-16 object-contain rounded-md border"
          />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span
              className={`inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full ${
                isLive
                  ? "bg-green-100 text-green-800 border border-green-200"
                  : "bg-red-100 text-red-800 border border-red-200"
              }`}
            >
              {liveOrDeadStatus}
            </span>
          </div>
          <p className="text-sm text-gray-900 truncate">
            <span className="font-semibold">Correspondence:</span> {correspondenceName || "—"}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            <span className="font-semibold">Transaction date:</span> {transactionDate}
          </p>
        </div>
      </div>
    </div>
  );
}
