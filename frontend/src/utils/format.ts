export function formatMoney(value: number | string): string {
  const amount = Number(value)
  return amount === 0 ? '免费' : `¥${amount.toFixed(2)}`
}

export function formatMinutes(minutes: number): string {
  if (minutes < 60) return `${minutes} 分钟`
  return `${Math.floor(minutes / 60)} 小时 ${minutes % 60} 分钟`
}
