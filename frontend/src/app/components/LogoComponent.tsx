"use client";

import Image from "next/image";
import Link from "next/link";

function LogoComponent() {
  
  return (
    <div className="flex items-center">
      <Link href="/">
        <Image src="/LOGO-PNG-PRINCIPAL.png" alt="Logo" width={150} height={25} />
      </Link>
    </div>
  );
}

export default LogoComponent;
