"use client";
import { useEffect, useState } from "react";
import { Moon, Sun } from "lucide-react";
import { themeStorageKey } from "@/lib/theme";

export function ThemeToggle() {
  const [theme, setTheme] = useState("light");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const system = window.matchMedia("(prefers-color-scheme: dark)");
    function sync() {
      let saved;
      try {
        saved = localStorage.getItem(themeStorageKey);
      } catch {}
      const next =
        saved === "light" || saved === "dark"
          ? saved
          : system.matches
            ? "dark"
            : "light";
      document.documentElement.dataset.theme = next;
      setTheme(next);
    }
    function storage(event: StorageEvent) {
      if (event.key === themeStorageKey || event.key === null) sync();
    }
    sync();
    setReady(true);
    system.addEventListener("change", sync);
    window.addEventListener("storage", storage);
    return () => {
      system.removeEventListener("change", sync);
      window.removeEventListener("storage", storage);
    };
  }, []);

  function toggle() {
    const next = theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    setTheme(next);
    try {
      localStorage.setItem(themeStorageKey, next);
    } catch {}
  }

  const label =
    theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
  return (
    <button
      className="theme-toggle"
      onClick={toggle}
      disabled={!ready}
      aria-label={label}
      title={label}
    >
      {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
      <span>{theme === "dark" ? "Light" : "Dark"}</span>
    </button>
  );
}
