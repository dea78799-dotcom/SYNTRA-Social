import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.119.2';

const SUPABASE_URL = 'https://qmrhlbovksrspmauijrz.supabase.co';
const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_YNn7UKlZb83lY5HVwzIVIg_28if2RnI';

try {
  const client = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true,
    },
  });

  if (typeof window.syntraCloudInit === 'function') {
    await window.syntraCloudInit(client);
  } else {
    console.error('SYNTRA Cloud bootstrap function is unavailable.');
  }
} catch (error) {
  console.error('SYNTRA Cloud could not initialize:', error);
  const status = document.getElementById('cloudAccountStatus');
  if (status) status.textContent = 'Không kết nối được SYNTRA Cloud. Hãy tải lại trang và thử lại.';
}
