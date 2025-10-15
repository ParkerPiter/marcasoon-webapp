"use client";

import Image from "next/image";

function LogoComponent() {
  return (
    <div className="flex items-center">
      <Image src="/LOGO-PNG-PRINCIPAL.png" alt="Logo" width={150} height={25} />
    </div>
  );
}

export default LogoComponent;
