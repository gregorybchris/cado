import AppConfig from "../lib/appConfig";
import Connection from "./Connection";

const APP_CONFIG: AppConfig = {
  host: window.location.host,
  reconnectAttempts: 150,
  reconnectInterval: 2000,
};

export default function App() {
  console.log("Using app config: ", APP_CONFIG);
  return (
    <div className="min-w-screen font-main min-h-screen bg-rock font-sen text-gray-400">
      <Connection appConfig={APP_CONFIG} />
    </div>
  );
}
