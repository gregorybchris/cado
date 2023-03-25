import AppConfig, { fetchConfig } from "../lib/appConfig";
import { useEffect, useState } from "react";

import Connection from "./Connection";

const DEFAULT_APP_CONFIG = {
  port: 8000,
  reconnectAttempts: 150,
  reconnectInterval: 2000,
};

export default function App() {
  const [appConfig, setAppConfig] = useState<AppConfig>(DEFAULT_APP_CONFIG);

  console.log("Loaded app config: ", appConfig);

  useEffect(() => {
    fetchConfig().then((c) => {
      if (!c) {
        console.info("No config.json found. Will use default configuration: ", appConfig);
        return;
      }
      setAppConfig({ ...appConfig, ...c });
    });
  }, []);

  return (
    <div className="min-w-screen font-main min-h-screen bg-rock font-sen text-gray-400">
      <Connection appConfig={appConfig} />
    </div>
  );
}
