"use client";
import FormContact from "../components/form/contactForm";
import Image from "next/image";
import banner from "../../../public/arte3.png";

const ContactoPage = () => {
  return (
    <div>
      <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-12 items-stretch">
        <div className="flex flex-col w-full space-y-2 py-6 md:col-span-1 md:h-full md:justify-center">
        <h3 className="md:text-3xl text-2xl font-semibold text-black uppercase font-playfair italic text-center">Contacto</h3>
        <p className="md:text-lg text-base text-[#192A56] font-semibold text-center">Si tienes alguna pregunta, no dudes en contactarnos.</p>
          <FormContact />
        </div>
        <div className="relative w-full md:col-span-2 h-[24vh] md:h-[55vh] lg:h-[65vh] xl:h-[72vh]">
          <Image
            src={banner}
            alt="Descripción de la imagen"
            fill
            className="object-cover object-center md:object-[center_top]"
          />
        </div>
      </div>

    </div>
  );
};

export default ContactoPage;