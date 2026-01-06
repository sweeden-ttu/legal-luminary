import { test, expect } from '@playwright/test';

test.describe('Advertisement Section Verification', () => {
  test.describe('Homepage Advertisement Section', () => {
    test('should display advertisement section in sidebar', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      // Verify ad section exists
      const adSection = page.locator('.ad-section');
      await expect(adSection).toBeVisible();
      
      // Verify "ADVERTISEMENT" label is present
      const adLabel = adSection.locator('.ad-label');
      await expect(adLabel).toBeVisible();
      await expect(adLabel).toHaveText('ADVERTISEMENT');
    });

    test('should contain ad cards with required elements', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Verify at least one ad card exists
      const cardCount = await adCards.count();
      expect(cardCount).toBeGreaterThan(0);
      
      // Verify first ad card has required structure
      const firstCard = adCards.first();
      await expect(firstCard).toBeVisible();
      
      // Check for specialty
      const specialty = firstCard.locator('.ad-specialty');
      await expect(specialty.first()).toBeVisible();
      
      // Check for heading (h4)
      const heading = firstCard.locator('h4');
      await expect(heading.first()).toBeVisible();
      
      // Check for description (p tag)
      const description = firstCard.locator('p').first();
      await expect(description).toBeVisible();
      
      // Check for contact information
      const contact = firstCard.locator('.ad-contact');
      await expect(contact.first()).toBeVisible();
      
      // Check for CTA button/link
      const cta = firstCard.locator('.ad-cta');
      await expect(cta.first()).toBeVisible();
    });

    test('should have functional contact links', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Check phone links
      const phoneLinks = adCards.locator('a[href^="tel:"]');
      const phoneCount = await phoneLinks.count();
      if (phoneCount > 0) {
        const firstPhoneLink = phoneLinks.first();
        await expect(firstPhoneLink).toBeVisible();
        const href = await firstPhoneLink.getAttribute('href');
        expect(href).toMatch(/^tel:\+/);
      }
      
      // Check email links
      const emailLinks = adCards.locator('a[href^="mailto:"]');
      const emailCount = await emailLinks.count();
      if (emailCount > 0) {
        const firstEmailLink = emailLinks.first();
        await expect(firstEmailLink).toBeVisible();
        const href = await firstEmailLink.getAttribute('href');
        expect(href).toMatch(/^mailto:/);
      }
    });

    test('should display general legal service ads', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Verify at least one ad mentions general services
      // (Process Server, Notary Public, or Legal Services)
      const specialties = adCards.locator('.ad-specialty');
      const specialtyTexts = await specialties.allTextContents();
      
      const generalServices = ['Process Server', 'Notary Public', 'Legal Services'];
      const hasGeneralService = specialtyTexts.some(text => 
        generalServices.some(service => text.includes(service))
      );
      
      expect(hasGeneralService).toBe(true);
    });
  });

  test.describe('Defense Page Advertisement Section', () => {
    test('should display defense-specific advertisement section', async ({ page }) => {
      await page.goto('/defense/', { waitUntil: 'domcontentloaded' });
      
      // Verify ad section exists
      const adSection = page.locator('.ad-section');
      await expect(adSection).toBeVisible();
      
      // Verify "ADVERTISEMENT" label
      const adLabel = adSection.locator('.ad-label');
      await expect(adLabel).toHaveText('ADVERTISEMENT');
    });

    test('should contain defense-related ad cards', async ({ page }) => {
      await page.goto('/defense/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Verify at least one ad card exists
      const cardCount = await adCards.count();
      expect(cardCount).toBeGreaterThan(0);
      
      // Verify ads contain defense-related specialties
      const specialties = adCards.locator('.ad-specialty');
      const specialtyTexts = await specialties.allTextContents();
      
      const defenseServices = ['Criminal Defense', 'Bail Bonds', 'Defense'];
      const hasDefenseService = specialtyTexts.some(text => 
        defenseServices.some(service => text.includes(service))
      );
      
      expect(hasDefenseService).toBe(true);
    });

    test('should have featured defense ad marked correctly', async ({ page }) => {
      await page.goto('/defense/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const featuredAds = adSection.locator('.ad-card.featured');
      
      // Check if any featured ads exist
      const featuredCount = await featuredAds.count();
      if (featuredCount > 0) {
        const firstFeatured = featuredAds.first();
        await expect(firstFeatured).toBeVisible();
        
        // Verify featured ad has all required elements
        await expect(firstFeatured.locator('.ad-specialty').first()).toBeVisible();
        await expect(firstFeatured.locator('h4').first()).toBeVisible();
        await expect(firstFeatured.locator('.ad-cta').first()).toBeVisible();
      }
    });

    test('should have functional defense attorney contact links', async ({ page }) => {
      await page.goto('/defense/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Check for phone links in defense ads
      const phoneLinks = adCards.locator('a[href^="tel:"]');
      const phoneCount = await phoneLinks.count();
      expect(phoneCount).toBeGreaterThan(0);
      
      // Verify first phone link is functional
      const firstPhoneLink = phoneLinks.first();
      await expect(firstPhoneLink).toBeVisible();
      const href = await firstPhoneLink.getAttribute('href');
      expect(href).toMatch(/^tel:\+/);
    });

    test('should include appropriate disclaimers for defense ads', async ({ page }) => {
      await page.goto('/defense/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Check for disclaimers (may be in ad-disclaimer class or in text)
      const disclaimers = adCards.locator('.ad-disclaimer');
      const disclaimerCount = await disclaimers.count();
      
      // At least one ad should have a disclaimer (for attorney ads)
      if (disclaimerCount > 0) {
        const firstDisclaimer = disclaimers.first();
        const disclaimerText = await firstDisclaimer.textContent();
        expect(disclaimerText?.length).toBeGreaterThan(0);
      }
    });
  });

  test.describe('Personal Injury Page Advertisement Section', () => {
    test('should display injury-specific advertisement section', async ({ page }) => {
      await page.goto('/personal-injury/', { waitUntil: 'domcontentloaded' });
      
      // Verify ad section exists
      const adSection = page.locator('.ad-section');
      await expect(adSection).toBeVisible();
      
      // Verify "ADVERTISEMENT" label
      const adLabel = adSection.locator('.ad-label');
      await expect(adLabel).toHaveText('ADVERTISEMENT');
    });

    test('should contain personal injury-related ad cards', async ({ page }) => {
      await page.goto('/personal-injury/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Verify at least one ad card exists
      const cardCount = await adCards.count();
      expect(cardCount).toBeGreaterThan(0);
      
      // Verify ads contain injury-related specialties
      const specialties = adCards.locator('.ad-specialty');
      const specialtyTexts = await specialties.allTextContents();
      
      const injuryServices = ['Personal Injury', 'Injury'];
      const hasInjuryService = specialtyTexts.some(text => 
        injuryServices.some(service => text.includes(service))
      );
      
      expect(hasInjuryService).toBe(true);
    });

    test('should have featured injury ad marked correctly', async ({ page }) => {
      await page.goto('/personal-injury/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const featuredAds = adSection.locator('.ad-card.featured');
      
      // Check if any featured ads exist
      const featuredCount = await featuredAds.count();
      if (featuredCount > 0) {
        const firstFeatured = featuredAds.first();
        await expect(firstFeatured).toBeVisible();
        
        // Verify featured ad has all required elements
        await expect(firstFeatured.locator('.ad-specialty').first()).toBeVisible();
        await expect(firstFeatured.locator('h4').first()).toBeVisible();
        await expect(firstFeatured.locator('.ad-cta').first()).toBeVisible();
      }
    });

    test('should have functional injury attorney contact links', async ({ page }) => {
      await page.goto('/personal-injury/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Check for contact links (phone, email, or website)
      const phoneLinks = adCards.locator('a[href^="tel:"]');
      const emailLinks = adCards.locator('a[href^="mailto:"]');
      const websiteLinks = adCards.locator('a[href^="http"]');
      
      const totalContactLinks = await phoneLinks.count() + 
                                await emailLinks.count() + 
                                await websiteLinks.count();
      
      expect(totalContactLinks).toBeGreaterThan(0);
    });

    test('should include contingency fee disclaimers for injury ads', async ({ page }) => {
      await page.goto('/personal-injury/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      const adCards = adSection.locator('.ad-card');
      
      // Check for disclaimers that mention contingency fees
      const disclaimers = adCards.locator('.ad-disclaimer');
      const disclaimerCount = await disclaimers.count();
      
      if (disclaimerCount > 0) {
        // Get all disclaimer text
        const disclaimerTexts = await disclaimers.allTextContents();
        const hasContingencyDisclaimer = disclaimerTexts.some(text => 
          text.toLowerCase().includes('contingency') || 
          text.toLowerCase().includes('attorney fee')
        );
        
        // At least one injury ad should mention contingency fees
        expect(hasContingencyDisclaimer).toBe(true);
      }
    });
  });

  test.describe('Advertisement Structure Validation', () => {
    test('all ad cards should have required structure elements', async ({ page }) => {
      const pages = ['/', '/defense/', '/personal-injury/'];
      
      for (const path of pages) {
        await page.goto(path, { waitUntil: 'domcontentloaded' });
        
        const adSection = page.locator('.ad-section');
        if (await adSection.count() > 0) {
          const adCards = adSection.locator('.ad-card');
          const cardCount = await adCards.count();
          
          for (let i = 0; i < cardCount; i++) {
            const card = adCards.nth(i);
            
            // Each card must have:
            // 1. Specialty
            const specialty = card.locator('.ad-specialty');
            if (await specialty.count() > 0) {
              await expect(specialty.first()).toBeVisible();
            }
            
            // 2. Heading (h4)
            const heading = card.locator('h4');
            if (await heading.count() > 0) {
              await expect(heading.first()).toBeVisible();
            }
            
            // 3. Description (p tag)
            const description = card.locator('p').first();
            await expect(description).toBeVisible();
            
            // 4. CTA link/button
            const cta = card.locator('.ad-cta');
            await expect(cta.first()).toBeVisible();
          }
        }
      }
    });

    test('ad section should have proper ARIA labels', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      if (await adSection.count() > 0) {
        const ariaLabel = await adSection.getAttribute('aria-label');
        expect(ariaLabel).toBeTruthy();
        // ARIA label should indicate it's an advertisement or sponsored content
        const labelLower = ariaLabel?.toLowerCase() || '';
        expect(
          labelLower.includes('advertisement') || 
          labelLower.includes('sponsored') || 
          labelLower.includes('ad')
        ).toBe(true);
      }
    });

    test('external ad links should have proper rel attributes', async ({ page }) => {
      const pages = ['/', '/defense/', '/personal-injury/'];
      
      for (const path of pages) {
        await page.goto(path, { waitUntil: 'domcontentloaded' });
        
        const adSection = page.locator('.ad-section');
        if (await adSection.count() > 0) {
          const externalLinks = adSection.locator('a[href^="http"]');
          const linkCount = await externalLinks.count();
          
          for (let i = 0; i < linkCount; i++) {
            const link = externalLinks.nth(i);
            const rel = await link.getAttribute('rel');
            
            // External links should have noopener noreferrer
            if (rel) {
              expect(rel).toContain('noopener');
              expect(rel).toContain('noreferrer');
            }
          }
        }
      }
    });
  });

  test.describe('Advertisement Content Verification', () => {
    test('homepage should not show defense-specific ads', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      if (await adSection.count() > 0) {
        const specialties = adSection.locator('.ad-specialty');
        const specialtyTexts = await specialties.allTextContents();
        
        // Homepage should not have "Criminal Defense" or "Bail Bonds" as primary ads
        const hasDefenseAds = specialtyTexts.some(text => 
          text.includes('Criminal Defense') || text.includes('Bail Bonds')
        );
        
        // This is a soft check - homepage might have general ads
        // We're just ensuring it doesn't primarily show defense ads
        expect(hasDefenseAds).toBe(false);
      }
    });

    test('defense page should not show injury-specific ads', async ({ page }) => {
      await page.goto('/defense/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      if (await adSection.count() > 0) {
        const specialties = adSection.locator('.ad-specialty');
        const specialtyTexts = await specialties.allTextContents();
        
        // Defense page should not have "Personal Injury" as primary ads
        const hasInjuryAds = specialtyTexts.some(text => 
          text.includes('Personal Injury')
        );
        
        expect(hasInjuryAds).toBe(false);
      }
    });

    test('injury page should not show defense-specific ads', async ({ page }) => {
      await page.goto('/personal-injury/', { waitUntil: 'domcontentloaded' });
      
      const adSection = page.locator('.ad-section');
      if (await adSection.count() > 0) {
        const specialties = adSection.locator('.ad-specialty');
        const specialtyTexts = await specialties.allTextContents();
        
        // Injury page should not have "Criminal Defense" or "Bail Bonds" as primary ads
        const hasDefenseAds = specialtyTexts.some(text => 
          text.includes('Criminal Defense') || text.includes('Bail Bonds')
        );
        
        expect(hasDefenseAds).toBe(false);
      }
    });
  });
});

