export interface FormValues {
  fullName: string;
  email: string;
  countryCode: string;
  phoneLocal: string;
  protect: ProtectType[];
};

export type ProtectType = "name" | "logo" | "slogan" | "sound";