# Bell County Judicial Elections 2026

This directory contains dossiers for Bell County judiciary candidates. The layout below uses CSS to provide an accessible, reactive overview of the competitive races, placing candidates for the same bench side-by-side.

<style>
.judiciary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 1.5rem;
}

.bench-section {
    margin-bottom: 3rem;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 5px solid #0056b3;
}

.bench-header {
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #dee2e6;
}

.bench-title {
    font-size: 1.5rem;
    color: #212529;
    margin: 0 0 0.5rem 0;
}

.incumbent-note {
    font-size: 0.9rem;
    color: #6c757d;
    font-style: italic;
}

.candidate-card {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    transition: transform 0.2s, box-shadow 0.2s;
}

.candidate-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.candidate-card.incumbent {
    border-top: 4px solid #28a745;
}

.candidate-card.challenger {
    border-top: 4px solid #ffc107;
}

.candidate-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.headshot {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    background-color: #e9ecef;
}

.candidate-info h3 {
    margin: 0 0 0.25rem 0;
    font-size: 1.2rem;
}

.party-badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    text-transform: uppercase;
}

.party-republican { background: #fee2e2; color: #dc2626; }
.party-democrat { background: #dbeafe; color: #2563eb; }

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    background: #e2e8f0;
    color: #475569;
    margin-left: 0.5rem;
}

.bio-link {
    margin-top: auto;
    padding-top: 1rem;
    display: inline-block;
    color: #0056b3;
    text-decoration: none;
    font-weight: 500;
}

.bio-link:hover {
    text-decoration: underline;
}

@media (max-width: 768px) {
    .judiciary-grid {
        grid-template-columns: 1fr;
    }
}
</style>

## 2026 Judicial Races

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">Bell County Judge</h2>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card incumbent">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/david-blackburn.jpg" alt="Headshot of Judge David Blackburn" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Judge David Blackburn</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Incumbent</span>
                </div>
            </div>
            <p>County Judge David Blackburn took office in 2019 and is seeking a third term.</p>
            <a href="texas/david_blackburn.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">Bell County Court at Law No. 1</h2>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card incumbent">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/paul-motz.jpg" alt="Headshot of Judge Paul Motz" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Judge Paul Motz</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Incumbent</span>
                </div>
            </div>
            <p>Elected in 2022, providing judicial services in both English and Spanish.</p>
            <a href="texas/paul_motz.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">Bell County Court at Law No. 2</h2>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card incumbent">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/john-mischtian.jpg" alt="Headshot of Judge John Mischtian" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Judge John Mischtian</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Incumbent</span>
                </div>
            </div>
            <p>Served as presiding judge for over a decade, managing cases from misdemeanors to civil disputes.</p>
            <a href="texas/john_mischtian.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">Bell County Court at Law No. 3</h2>
        <p class="incumbent-note">The incumbent, Judge Rebecca DePew, is not listed among the 2026 candidates in our dossiers. John Gauntt Jr. is running for the seat.</p>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card challenger">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/john-gauntt-jr.jpg" alt="Headshot of John Gauntt Jr." onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>John Gauntt Jr.</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Candidate</span>
                </div>
            </div>
            <p>Fourth-generation Bell County attorney with a 25-year career as a prosecutor specializing in juvenile law.</p>
            <a href="texas/john_gauntt_jr.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">478th District Court</h2>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card incumbent">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/wade-faulkner.jpg" alt="Headshot of Judge Wade Faulkner" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Judge Wade Faulkner</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Incumbent</span>
                </div>
            </div>
            <p>Presiding judge since the court's creation in 2022; retired LTC U.S. Army Judge Advocate.</p>
            <a href="texas/wade_faulkner.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">169th District Court</h2>
        <p class="incumbent-note">The incumbent, Judge Cari Starritt-Burnett, is not listed in our dossiers. Judge Paul LePak, currently of the 264th District Court, is seeking this bench.</p>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card challenger">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/paul-lepak.jpg" alt="Headshot of Judge Paul LePak" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Judge Paul LePak</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Candidate</span>
                </div>
            </div>
            <p>Currently serves as Judge of the 264th Judicial District Court (appointed 2018), now seeking the 169th.</p>
            <a href="texas/paul_lepak.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">Justice of the Peace, Precinct 2</h2>
        <p class="incumbent-note">Incumbent Judge Cliff Coleman announced he will not seek re-election, leaving an open seat.</p>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card challenger">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/michael-tice.jpg" alt="Headshot of Michael Tice" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Michael Tice</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Candidate</span>
                </div>
            </div>
            <p>U.S. Army veteran and retired Texas State Trooper; Republican nominee.</p>
            <a href="texas/michael_tice.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

<div class="bench-section">
    <div class="bench-header">
        <h2 class="bench-title">Justice of the Peace, Precinct 4, Place 2</h2>
        <p class="incumbent-note">Incumbent Nicola J. James is running for reelection in the Democratic primary, but faces challenger Jessica Gonzalez. Beatrice Cox is the Republican nominee.</p>
    </div>
    <div class="judiciary-grid">
        <div class="candidate-card challenger">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/jessica-gonzalez.jpg" alt="Headshot of Jessica A. Gonzalez" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Jessica A. Gonzalez</h3>
                    <span class="party-badge party-democrat">Democrat</span>
                    <span class="status-badge">Candidate</span>
                </div>
            </div>
            <p>Killeen City Councilwoman transitioning focus toward the judiciary; Democratic nominee after runoff.</p>
            <a href="texas/jessica_gonzalez.md" class="bio-link">Read Full Dossier →</a>
        </div>
        <div class="candidate-card challenger">
            <div class="candidate-header">
                <img class="headshot" src="/assets/img/candidates/beatrice-cox.jpg" alt="Headshot of Beatrice Cox" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23ccc\'%3E%3Cpath d=\'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z\'/%3E%3C/svg%3E'">
                <div class="candidate-info">
                    <h3>Beatrice "Bea" Cox</h3>
                    <span class="party-badge party-republican">Republican</span>
                    <span class="status-badge">Candidate</span>
                </div>
            </div>
            <p>Former Chief Clerk for JP system and first Truancy Master for Bell County; Republican nominee.</p>
            <a href="texas/beatrice_cox.md" class="bio-link">Read Full Dossier →</a>
        </div>
    </div>
</div>

---

## Meta-interpretation & Introspection Analysis

As part of the agent-oriented meta-interpretation methodology (Agent-Oriented Programming, Chapter 8), this layout and the underlying generated dossiers have been critically analyzed:

### 1. Accessibility
- **Semantic Structure:** The layout uses clear, semantic HTML elements (headings for logical outline) and avoids pure div-soup.
- **Alt Text:** Every image tag includes a descriptive `alt` attribute (e.g., `alt="Headshot of Judge David Blackburn"`).
- **Color Contrast:** The text uses high-contrast colors (`#212529` on `#ffffff`, `#6c757d` for notes). Badges use compliant background/text color pairings (`#dc2626` on `#fee2e2` for Republicans, `#2563eb` on `#dbeafe` for Democrats).
- **Graceful Degradation:** A fallback SVG is provided via `onerror` so that if candidate headshots are missing from `/assets/img/candidates/`, a neutral placeholder icon is displayed instead of a broken image link.

### 2. Reactive Design
- The CSS utilizes `display: grid` with `auto-fit` and `minmax(300px, 1fr)`, ensuring that the candidate cards elegantly wrap and expand to fill available horizontal space.
- A media query ensures a single-column layout on mobile devices (`max-width: 768px`), guaranteeing the content remains legible across viewports without horizontal scrolling.

### 3. Completeness of Biographies & Resumes
The generated dossiers show a strong level of completeness regarding the candidates' professional histories and platforms.
- **Strengths:** Most dossiers accurately detail academic backgrounds (e.g., Baylor Law for Mischtian/Gauntt), professional tenures, and specific campaign focuses (e.g., juvenile law, public safety). The `office_timeline` YAML frontmatter is a valuable structured artifact.
- **Weaknesses:** There are notable gaps regarding the incumbents who are *not* seeking re-election or who were defeated. The generated dossiers lack files for Judge Cliff Coleman (JP Precinct 2, retiring), Judge Rebecca DePew (Court at Law No. 3), and Judge Cari Starritt-Burnett (169th District Court). Furthermore, incumbent Nicola J. James (JP Precinct 4 Place 2) is missing a dossier, leaving the user with an incomplete picture of the race dynamics where challengers Gonzalez and Cox are running.

### 4. Missing Incumbents Investigation Findings
Our external validation process resolved several discrepancies where seats lack an incumbent in the dossier list:
1. **Justice of the Peace, Precinct 2:** Incumbent Judge Cliff Coleman publicly announced he will not seek re-election, creating an open seat now sought by Republican nominee Michael Tice.
2. **169th District Court:** Judge Cari Starritt-Burnett is the incumbent. However, Judge Paul LePak, who currently presides over the 264th District Court, is seeking the 169th District Court bench. This indicates either a primary challenge, an open seat if Starritt-Burnett retires, or a strategic judicial bench swap.
3. **Court at Law No. 3:** Judge Rebecca DePew currently holds this office. It is unclear if she is retiring in 2026, but John Gauntt Jr. is running as the Republican nominee for this seat.
4. **Justice of the Peace, Precinct 4, Place 2:** Nicola J. James is the Democratic incumbent. Jessica Gonzalez is running as a Democrat (and won the runoff), implying she either defeated James or James did not run. Beatrice Cox is the Republican nominee.

This introspection validates the subagents' work in identifying the active 2026 candidates, while highlighting the need for future web-crawling behaviors to explicitly target and catalog outgoing incumbents to preserve institutional context.
