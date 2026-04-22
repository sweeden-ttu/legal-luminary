/**
 * Bell County Municipal Elections 2026 — Candidate Filter JS
 * Works with the new .elections-candidate-card + city section layout.
 */
document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("candidateSearch");
  const resultCount = document.getElementById("candidateResultCount");
  const cityTabs = Array.from(document.querySelectorAll(".elections-city-tab"));
  const allCards = Array.from(
    document.querySelectorAll(".elections-candidate-card"),
  );
  const citySections = Array.from(
    document.querySelectorAll("[data-city-section]"),
  );

  let activeCity = "";

  /* ── Apply city + search filter ──────────────────────── */
  function applyFilters() {
    const query = (searchInput?.value || "").trim().toLowerCase();
    let visible = 0;

    allCards.forEach((card) => {
      const city = card.dataset.city || "";
      const name = card.dataset.name || "";
      const office = card.dataset.office || "";

      const cityPass = !activeCity || city === activeCity;
      const queryPass =
        !query || name.includes(query) || office.includes(query);
      const show = cityPass && queryPass;

      card.hidden = !show;
      if (show) visible++;
    });

    // Show/hide city section headers
    citySections.forEach((section) => {
      const secCity = section.dataset.citySection;
      const hasCards = Array.from(
        section.querySelectorAll(".elections-candidate-card"),
      ).some((c) => !c.hidden);
      section.hidden = !hasCards;
    });

    if (resultCount) {
      resultCount.textContent = `${visible} candidate${visible !== 1 ? "s" : ""}`;
    }
  }

  /* ── City tab clicks ─────────────────────────────────── */
  cityTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      activeCity = tab.dataset.city || "";
      cityTabs.forEach((t) => {
        const active = t.dataset.city === activeCity;
        t.classList.toggle("is-active", active);
        t.setAttribute("aria-pressed", active ? "true" : "false");
      });
      // Update URL hash
      const hash = activeCity ? `city=${activeCity}` : "";
      history.replaceState({}, "", hash ? `#${hash}` : location.pathname);
      applyFilters();
      // Scroll to city section if filtering to one city
      if (activeCity) {
        const section = document.getElementById(`city-${activeCity}`);
        if (section)
          section.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  /* ── Search input ────────────────────────────────────── */
  searchInput?.addEventListener("input", applyFilters);

  /* ── Read hash on load ───────────────────────────────── */
  const params = new URLSearchParams(window.location.hash.replace(/^#/, ""));
  const cityFromHash = params.get("city");
  if (cityFromHash) {
    activeCity = cityFromHash;
    cityTabs.forEach((t) => {
      const active = t.dataset.city === activeCity;
      t.classList.toggle("is-active", active);
      t.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  applyFilters();
});
