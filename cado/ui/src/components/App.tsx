import Notebook from "./Notebook";
import Toolbar from "./Toolbar";

export default function App() {
  return (
    <div className="min-w-screen font-main min-h-screen bg-rock font-sen text-gray-400">
      <div className="select-none py-10 text-center text-3xl font-bold">Cado Notebook</div>
      <Toolbar />
      <Notebook />
    </div>
  );
}
