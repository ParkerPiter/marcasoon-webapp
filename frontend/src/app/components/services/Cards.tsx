"use client";

import { useEffect, useState } from 'react';
import { servicios } from '../../../../api/test';
import { CardService } from '../../interfaces/card';
import Card from './Card';

const Cards = () => {
  const [lista, setLista] = useState<CardService[]>([]);

  useEffect(() => {
    // Fuente local estática: api/test.js
    setLista(servicios);
  }, []);

  if (!lista.length) return <p>No hay servicios disponibles.</p>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
      {lista.map((svc) => (
        <Card
          key={svc.id}
          id={svc.id}
          title={svc.title}
          bullets={svc.bullets}
        />
      ))}
    </div>
  );
};

export default Cards;
