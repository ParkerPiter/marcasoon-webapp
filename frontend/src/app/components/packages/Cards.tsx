"use client";

import { paquetes } from '../../../../api/test'
import CardPrice from './Card';

const Cards = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {paquetes.map((paquete) => (
        <CardPrice key={paquete.id} 
            id={paquete.id}
            title={paquete.title}
            client_objetive={paquete.client_objetive}
            description={paquete.description}
            includes={paquete.includes}
            price={paquete.price}

        />
      ))}
    </div>
  );
};

export default Cards;
