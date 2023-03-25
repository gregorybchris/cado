import { None, Optional } from "./types";

export default interface AppConfig {
  port: number;
  reconnectAttempts: number;
  reconnectInterval: number;
}

export async function fetchConfig(): Promise<Optional<AppConfig>> {
  try {
    const response = await fetch("config.json");
    return await response.json();
  } catch (error) {
    return None;
  }
}
