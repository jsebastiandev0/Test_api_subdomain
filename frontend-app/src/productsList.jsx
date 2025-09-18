import { useEffect, useState } from 'react';

function ProductsList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://test-api.jsebastian.dev/products/?skip=0&limit=10') // API de prueba
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.products);
        setLoading(false);
        console.log(data, 'data')
      })
      .catch((err) => {
        console.error('Error al cargar products:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando products...</p>;

  return (
    <ul>
      {products.map((product) => (
        <li key={product.id}>
          <strong>{product.name}</strong> 
          - <strong>{product.price}</strong>
          - 
          <span>{product.stock}</span>
        </li>
      ))}
    </ul>
  );
}

export default ProductsList;