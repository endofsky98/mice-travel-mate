import HomeClient, { InitialData } from './HomeClient';

async function getInitialData(): Promise<InitialData> {
  const apiUrl = process.env.INTERNAL_API_URL || 'http://localhost:8007';

  const safeFetch = async (url: string) => {
    try {
      const res = await fetch(url, { cache: 'no-store' });
      if (!res.ok) return { items: [] };
      return res.json();
    } catch {
      return { items: [] };
    }
  };

  const [restaurants, courses, products, guides, festivals, banners] = await Promise.all([
    safeFetch(`${apiUrl}/api/restaurants/?lang=en&per_page=10`),
    safeFetch(`${apiUrl}/api/courses?lang=en&per_page=10`),
    safeFetch(`${apiUrl}/api/products?lang=en&per_page=10`),
    safeFetch(`${apiUrl}/api/guides?lang=en&per_page=10`),
    safeFetch(`${apiUrl}/api/festivals?lang=en&per_page=6`),
    safeFetch(`${apiUrl}/api/banners`),
  ]);

  return {
    restaurants: restaurants.items || [],
    courses: courses.items || [],
    products: products.items || [],
    guides: guides.items || [],
    festivals: festivals.items || [],
    banners: banners.items || [],
  };
}

export default async function Home() {
  const data = await getInitialData();
  return <HomeClient initialData={data} />;
}
