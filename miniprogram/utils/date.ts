// Asia/Shanghai timezone date helper
// Aligns with backend TIME_ZONE = 'Asia/Shanghai'
export function getShanghaiDateString(): string {
  const now = new Date();
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  const shanghai = new Date(utc + 8 * 3600000);

  const year = shanghai.getFullYear();
  const month = String(shanghai.getMonth() + 1).padStart(2, '0');
  const day = String(shanghai.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}
