"use client";

import { useEffect, useState } from "react";

type UseMediaQueryOptions = {
  initializeWithValue?: boolean;
  defaultValue?: boolean;
};

export function useMediaQuery(
  query: string,
  { initializeWithValue = true, defaultValue = false }: UseMediaQueryOptions = {}
) {
  const [matches, setMatches] = useState(() => {
    if (!initializeWithValue || typeof window === "undefined") {
      return defaultValue;
    }

    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);

    setMatches(mediaQuery.matches);

    const listener = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    mediaQuery.addEventListener("change", listener);

    return () => {
      mediaQuery.removeEventListener("change", listener);
    };
  }, [query]);

  return matches;
}
