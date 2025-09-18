import { useState } from 'react';

function AddProduct() {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const product = { name, price: parseFloat(price) };

    try {
      const res = await fetch('http://localhost:8000/products/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(product),
      });

      if (res.ok) {
        setMessage('Producto agregado con éxito ✅');
        setName('');
        setPrice('');
      } else {
        setMessage('Error al agregar producto ❌');
      }
    } catch (err) {
      console.error('Error al enviar:', err);
      setMessage('Error de red o CORS 🚫');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Agregar producto</h2>
      <input
        type="text"
        placeholder="Nombre"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Precio"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        required
      />
      <button type="submit">Agregar</button>
      {message && <p>{message}</p>}
    </form>
  );
}

export default AddProduct;