/**
 * Russian pluralization function
 * Returns correct word form based on number
 *
 * @param n - The number to check
 * @param forms - Array of 3 forms: [one, few, many]
 *   - one: 1, 21, 31, ... (e.g., "месяц")
 *   - few: 2-4, 22-24, ... (e.g., "месяца")
 *   - many: 5-20, 25-30, ... (e.g., "месяцев")
 * @returns The correct plural form
 */
export function pluralize(n: number, forms: [string, string, string]): string {
  const n10 = n % 10
  const n100 = n % 100

  if (n100 >= 11 && n100 <= 19) {
    return forms[2] // many
  }

  if (n10 === 1) {
    return forms[0] // one
  }

  if (n10 >= 2 && n10 <= 4) {
    return forms[1] // few
  }

  return forms[2] // many
}
