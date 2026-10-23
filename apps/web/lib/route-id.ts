// Some route parameters retain percent encoding. Normalize before allowlist lookup.
export function decodeRouteId(value: string): string {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}
