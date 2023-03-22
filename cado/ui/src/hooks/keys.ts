import { DependencyList, useEffect, useState } from "react";

import { Optional } from "../lib/types";

export interface Combo {
  pattern: string;
  callback: () => Optional<boolean>;
}

export function useKeyCombos(combos: Combo[], dependencies: DependencyList): void {
  const [keys, setKeys] = useState<string[]>([]);

  useEffect(() => {}, [keys]);

  function onDown(event: KeyboardEvent) {
    setKeys((keys) => {
      const key = event.key;
      if (keys.includes(key)) {
        return keys;
      }
      const newKeys = [...keys, key];
      const comboPattern = newKeys.join("+");
      for (let i = 0; i < combos.length; i++) {
        const combo = combos[i];
        if (comboPattern == combo.pattern) {
          const preventDefault = combo.callback() ?? true;
          if (preventDefault) event.preventDefault();
          break;
        }
      }
      return newKeys;
    });
  }

  function onUp(event: KeyboardEvent) {
    const key = event.key;
    const metaKeys = ["Meta", "Shift", "Command", "Alt", "Control"];
    if (metaKeys.includes(key)) {
      setKeys([]);
    } else {
      setKeys((keys) => (keys.includes(key) ? keys.filter((k) => k != key) : keys));
    }
  }

  useEffect(() => {
    window.addEventListener("keydown", onDown);
    window.addEventListener("keyup", onUp);

    return () => {
      window.removeEventListener("keydown", onDown);
      window.removeEventListener("keyup", onUp);
    };
  }, [dependencies]);
}
