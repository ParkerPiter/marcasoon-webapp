export type ProtectType = "name" | "logo" | "slogan" | "sound";

// Valores manejados internamente por react-hook-form
export interface FormValues {
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  countryCode: string;
  phoneLocal: string;
  protect: ProtectType[];
  password: string;
  confirmPassword: string;
};

// Payload final que se envía al padre tras normalización
export type ProtectNormalized = ProtectType | { type: ProtectType }[];

export interface SubmitPayload {
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  phone?: string;
  protect: ProtectNormalized;
  password: string;
}