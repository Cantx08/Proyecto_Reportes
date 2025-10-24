'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function DepartamentosPage() {
  const router = useRouter();
  
  useEffect(() => {
    router.push('/departments-management');
  }, [router]);

  return null;
}
