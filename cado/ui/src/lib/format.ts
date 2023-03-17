import { DateTime } from "luxon";

export function formatDateDiff(date: string) {
  return DateTime.fromISO(date).toRelative(DateTime.now());
}
