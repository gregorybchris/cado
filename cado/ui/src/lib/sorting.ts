export function sorter<T, K>(items: T[], accesssor: (item: T) => K) {
  return items.sort((a, b) => (accesssor(a) > accesssor(b) ? -1 : 1));
}
