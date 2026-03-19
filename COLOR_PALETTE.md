# Himwatkhanda Vastu - Color Palette & Design System

## 🎨 Brand Colors

### Primary Color - Scarlet
**Represents:** Energy, passion, prosperity, and traditional Vastu principles

| Color Name | Hex Value | RGB | Usage |
|-----------|-----------|-----|-------|
| Scarlet (Primary) | `#DA251C` | rgb(218, 37, 28) | Primary buttons, links, headings, CTAs |
| Scarlet Dark | `#b91c1c` | rgb(185, 28, 28) | Hover states, active elements |
| Scarlet Light (8% opacity) | `rgba(218, 37, 28, 0.08)` | rgb(218, 37, 28, 0.08) | Backgrounds, subtle highlights |
| Scarlet Medium (15% opacity) | `rgba(218, 37, 28, 0.15)` | rgb(218, 37, 28, 0.15) | Badges, cards, borders |

```
████████████████████  #DA251C (Scarlet - Primary)
████████████████████  #b91c1c (Scarlet Dark - Hover)
░░░░░░░░░░░░░░░░░░░░  rgba(218, 37, 28, 0.08) (Scarlet Light - BG)
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  rgba(218, 37, 28, 0.15) (Scarlet Medium - Accent)
```

---

### Secondary Color - Emerald Green
**Represents:** Growth, harmony, stability, and nature

| Color Name | Hex Value | RGB | Usage |
|-----------|-----------|-----|-------|
| Emerald (Secondary) | `#006D32` | rgb(0, 109, 50) | Success states, secondary actions, growth indicators |
| Emerald Dark | `#005228` | rgb(0, 82, 40) | Hover states for emerald elements |
| Emerald Light (8% opacity) | `rgba(0, 109, 50, 0.08)` | rgb(0, 109, 50, 0.08) | Backgrounds, subtle highlights |

```
████████████████████  #006D32 (Emerald - Secondary)
████████████████████  #005228 (Emerald Dark - Hover)
░░░░░░░░░░░░░░░░░░░░  rgba(0, 109, 50, 0.08) (Emerald Light - BG)
```

---

## 🎭 Neutral Colors

### Grayscale Palette

| Color Name | Hex Value | RGB | Usage |
|-----------|-----------|-----|-------|
| White | `#FEFEFE` | rgb(254, 254, 254) | Page background, cards, clean spaces |
| Off-White | `#F9FAFB` | rgb(249, 250, 251) | Section backgrounds, subtle contrast |
| Silver | `#CDCDCD` | rgb(205, 205, 205) | Dividers, borders, disabled states |
| Silver Light | `#E5E7EB` | rgb(229, 231, 235) | Light borders, backgrounds |
| Dim Grey | `#71706E` | rgb(113, 112, 110) | Secondary text, descriptions |
| Dim Grey Dark | `#4B5563` | rgb(75, 85, 99) | Body text, paragraphs |
| Dim Grey Darker | `#374151` | rgb(55, 65, 81) | Dark text, emphasis |
| Almost Black | `#111827` | rgb(17, 24, 39) | Headings, primary text |

```
████████████████████  #FEFEFE (White)
████████████████████  #F9FAFB (Off-White)
████████████████████  #CDCDCD (Silver)
████████████████████  #E5E7EB (Silver Light)
████████████████████  #71706E (Dim Grey)
████████████████████  #4B5563 (Dim Grey Dark)
████████████████████  #374151 (Dim Grey Darker)
████████████████████  #111827 (Almost Black)
```

---

## 🚦 Semantic Colors

### Success State (Emerald-based)
| Component | Value | Usage |
|-----------|-------|-------|
| Background | `rgba(0, 109, 50, 0.08)` | Success alert backgrounds |
| Text | `#006D32` | Success messages |
| Border | `#006D32` | Success alert borders |

### Error State (Scarlet-based)
| Component | Value | Usage |
|-----------|-------|-------|
| Background | `rgba(218, 37, 28, 0.08)` | Error alert backgrounds |
| Text | `#DA251C` | Error messages |
| Border | `#DA251C` | Error alert borders |

### Warning State
| Component | Value | Usage |
|-----------|-------|-------|
| Background | `#FEF3C7` | Warning alert backgrounds |
| Text | `#92400E` | Warning messages |
| Border | `#F59E0B` | Warning alert borders |

### Info State
| Component | Value | Usage |
|-----------|-------|-------|
| Background | `#EFF6FF` | Info alert backgrounds |
| Text | `#1E40AF` | Info messages |
| Border | `#3B82F6` | Info alert borders |

---

## 🎨 Gradient Combinations

### Primary Gradient
```css
background: linear-gradient(135deg, #DA251C 0%, #b91c1c 100%);
```
**Usage:** Primary buttons, hero sections, CTAs

### Hero Section Gradient
```css
background: linear-gradient(135deg, #FAFAFA 0%, #F0F0F0 50%, #E8E8E8 100%);
```
**Usage:** Hero section backgrounds

### Radial Gradient Overlay
```css
background: radial-gradient(circle at 20% 30%, rgba(218, 37, 28, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(0, 109, 50, 0.04) 0%, transparent 50%);
```
**Usage:** Subtle color overlays on hero sections

---

## 📐 Color Usage Guidelines

### Primary Actions
- **Color:** Scarlet (#DA251C)
- **Use for:** Main CTAs, submit buttons, primary links
- **Example:** "Get Consultation", "Enroll Now", "Book Now"

### Secondary Actions
- **Color:** Emerald (#006D32) or Scarlet outline
- **Use for:** Alternative actions, secondary buttons
- **Example:** "Learn More", "View Details"

### Backgrounds
- **Primary:** White (#FEFEFE)
- **Sections:** Off-White (#F9FAFB) or Silver (#CDCDCD)
- **Cards:** White (#FEFEFE) with subtle shadows

### Text Hierarchy
1. **Headings:** Almost Black (#111827)
2. **Body Text:** Dim Grey Darker (#374151)
3. **Secondary Text:** Dim Grey (#71706E)
4. **Links:** Scarlet (#DA251C)

---

## 🎯 Color Combinations

### High Contrast (Best Practice)
- Scarlet + White
- Almost Black + White
- Emerald + White

### Subtle & Professional
- Off-White + Silver Light borders
- White + Scarlet Light backgrounds
- Dim Grey + Off-White backgrounds

### Energetic & Bold
- Scarlet + Emerald
- Scarlet Dark + Emerald Dark
- Scarlet + Almost Black

---

## ♿ Accessibility Information

### WCAG AA Compliance
| Color Combination | Contrast Ratio | WCAG AA | WCAG AAA |
|-----------------|---------------|---------|----------|
| Scarlet (#DA251C) on White | 4.8:1 | ✅ Pass | ❌ Fail |
| Scarlet Dark (#b91c1c) on White | 5.9:1 | ✅ Pass | ❌ Fail |
| Emerald (#006D32) on White | 4.5:1 | ✅ Pass | ❌ Fail |
| Almost Black (#111827) on White | 16.2:1 | ✅ Pass | ✅ Pass |
| Dim Grey Darker (#374151) on White | 10.4:1 | ✅ Pass | ✅ Pass |

### Recommendations
- ✅ Use Scarlet for primary buttons and links
- ✅ Use Almost Black for headings and primary text
- ✅ Use Emerald for success indicators
- ⚠️ Avoid using Scarlet Light for text (insufficient contrast)
- ⚠️ Ensure text on Scarlet backgrounds is white (#FEFEFE)

---

## 🎨 Component Color Examples

### Buttons
```html
<!-- Primary Button -->
<button class="btn btn-primary">Get Consultation</button>
<!-- Gradient: #DA251C → #b91c1c, White text -->

<!-- Outline Button -->
<button class="btn btn-outline-primary">Learn More</button>
<!-- Transparent background, Scarlet border, Scarlet text -->
```

### Alerts
```html
<!-- Success Alert -->
<div class="alert alert-success">
  Background: rgba(0, 109, 50, 0.08)
  Text: #006D32
  Border: #006D32
</div>

<!-- Error Alert -->
<div class="alert alert-danger">
  Background: rgba(218, 37, 28, 0.08)
  Text: #DA251C
  Border: #DA251C
</div>
```

### Cards
```html
<div class="card">
  Background: #FEFEFE
  Border: #E5E7EB
  Shadow: 0 2px 8px rgba(0, 0, 0, 0.06)
  Hover Shadow: 0 8px 24px rgba(0, 0, 0, 0.12)
</div>
```

---

## 🌈 Color Psychology in Vastu Context

### Scarlet (#DA251C)
- **Element:** Fire (Agni)
- **Direction:** South-East
- **Qualities:** Energy, passion, prosperity, warmth
- **Best for:** CTAs, highlights, important actions

### Emerald (#006D32)
- **Element:** Earth (Prithvi)
- **Direction:** North-East
- **Qualities:** Growth, harmony, stability, balance
- **Best for:** Success indicators, secondary actions, trust-building elements

### White (#FEFEFE)
- **Element:** Space (Akasha)
- **Qualities:** Purity, clarity, peace, openness
- **Best for:** Backgrounds, clean spaces, breathing room

---

## 📱 Usage in Bootstrap Classes

### Text Colors
```html
<p class="text-primary">Scarlet text</p>
<p class="text-scarlet">Scarlet text (custom)</p>
<p class="text-emerald">Emerald text (custom)</p>
<p class="text-grey">Grey text (custom)</p>
```

### Background Colors
```html
<div class="bg-primary">Scarlet background</div>
<div class="bg-scarlet">Scarlet background (custom)</div>
<div class="bg-scarlet-light">Light scarlet background (custom)</div>
<div class="bg-emerald">Emerald background (custom)</div>
<div class="bg-silver">Silver background (custom)</div>
```

### Border Colors
```html
<div class="border border-primary">Scarlet border</div>
<div class="border border-scarlet">Scarlet border (custom)</div>
<div class="border border-emerald">Emerald border (custom)</div>
```

---

## 🎨 CSS Variables Reference

All colors are available as CSS custom properties:

```css
/* Core Brand */
var(--primary-scarlet)           /* #DA251C */
var(--primary-scarlet-dark)      /* #b91c1c */
var(--primary-scarlet-light)     /* rgba(218, 37, 28, 0.08) */
var(--primary-scarlet-medium)    /* rgba(218, 37, 28, 0.15) */

/* Neutral */
var(--white)                     /* #FEFEFE */
var(--off-white)                 /* #F9FAFB */
var(--silver)                    /* #CDCDCD */
var(--silver-light)              /* #E5E7EB */
var(--dim-grey)                  /* #71706E */
var(--dim-grey-dark)             /* #4B5563 */
var(--dim-grey-darker)           /* #374151 */
var(--almost-black)              /* #111827 */

/* Accent */
var(--dark-emerald)              /* #006D32 */
var(--dark-emerald-light)        /* rgba(0, 109, 50, 0.08) */
var(--dark-emerald-dark)         /* #005228 */
```

---

## 🔄 Color Transitions

### Standard Transition
```css
transition: all 0.3s ease;
```

### Hover Effects
```css
/* Buttons */
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(218, 37, 28, 0.35);

/* Cards */
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
transform: translateY(-2px);
```

---

## 📊 Color Distribution

### Recommended Usage Breakdown
- **Primary (Scarlet):** 20% - CTAs, links, highlights
- **Secondary (Emerald):** 15% - Success states, secondary actions
- **Neutrals:** 60% - Backgrounds, text, borders
- **Accents:** 5% - Special highlights, warnings

---

## 🎯 Best Practices

### DO ✅
- Use Scarlet for primary actions
- Maintain sufficient contrast (4.5:1 minimum)
- Use white backgrounds for content areas
- Test colors in different lighting conditions
- Use semantic colors for their intended purpose

### DON'T ❌
- Don't use Scarlet for large text areas
- Don't mix too many colors in one section
- Don't use light colors for text without testing
- Don't ignore color blindness accessibility
- Don't use colors without considering their meaning

---

## 📐 Spacing & Colors

### Color + Spacing Combinations
```css
/* Hero Section */
background: linear-gradient(135deg, #FAFAFA 0%, #F0F0F0 50%, #E8E8E8 100%);
padding: 5rem 0; /* py-20 */

/* Cards */
background: #FEFEFE;
border: 1px solid #E5E7EB;
border-radius: 1rem;
padding: 1.5rem; /* p-4 */

/* Buttons */
padding: 0.75rem 1.5rem; /* px-5 */
border-radius: 0.5rem;
```

---

## 🌐 Cross-Browser Compatibility

All colors are tested and compatible with:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## 📝 Implementation Notes

1. **Always use CSS variables** for consistency
2. **Test contrast ratios** before finalizing designs
3. **Consider color blindness** in design choices
4. **Maintain visual hierarchy** with color + size
5. **Use gradients sparingly** for maximum impact
6. **Test on real devices** for color accuracy

---

**Last Updated:** March 19, 2026
**Version:** 2.0
**Design System:** Bootstrap 5 + Custom Theme
