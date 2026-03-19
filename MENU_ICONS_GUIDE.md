# Menu Icons - Quick Reference Guide

## How to Add Icons to Menu Items

### Via Menu Admin (Recommended)

1. **Navigate to Menu Admin**
   - Go to `/admin/dashboard/menu/`
   - Click on the menu you want to edit (e.g., "Main Menu")

2. **Edit Menu Items Inline**
   - Scroll to the "Menu items" section
   - You'll see these columns:
     - **Order** - Drag to reorder
     - **Title** - Menu item text
     - **Icon** - Enter Font Awesome icon class
     - **Preview** - See what the icon looks like
     - **Type** - Page, Custom Link, Category, Post, etc.
     - **Page/URL** - Link destination
     - **Is Active** - Toggle visibility

3. **Add Icon Class**
   - In the **Icon** field, enter any Font Awesome icon class
   - See the **Preview** column to see the icon
   - See helpful suggestions below the icon field

### Via Individual Menu Item Admin

1. Go to `/admin/dashboard/menuitem/`
2. Click on any menu item
3. Fill in the **Icon** field in the "Basic Information" section
4. See icon suggestions and preview

## Popular Font Awesome Icons

### Navigation & Common
- `fas fa-home` - 🏠 Home
- `fas fa-user` - 👤 User/Profile
- `fas fa-users` - 👥 Users/Team
- `fas fa-cog` - ⚙️ Settings
- `fas fa-sign-out-alt` - 🚪 Logout
- `fas fa-sign-in-alt` - 🚪 Login

### Business & Services
- `fas fa-building` - 🏢 Building/About
- `fas fa-briefcase` - 💼 Briefcase/Services
- `fas fa-concierge-bell` - 🔔 Services
- `fas fa-handshake` - 🤝 Partnerships
- `fas fa-award` - 🏆 Awards
- `fas fa-certificate` - 📜 Certifications

### Contact & Communication
- `fas fa-envelope` - ✉️ Email/Contact
- `fas fa-phone` - 📞 Phone
- `fas fa-fax` - 📠 Fax
- `fas fa-comment` - 💬 Comments
- `fas fa-question-circle` - ❓ FAQ/Help
- `fas fa-info-circle` - ℹ️ Information

### Content & Media
- `fas fa-newspaper` - 📰 News/Blog
- `fas fa-file-alt` - 📄 Documents
- `fas fa-images` - 🖼️ Gallery
- `fas fa-video` - 🎥 Videos
- `fas fa-camera` - 📷 Camera
- `fas fa-music` - 🎵 Music

### Products & Shopping
- `fas fa-box` - 📦 Products
- `fas fa-shopping-cart` - 🛒 Cart
- `fas fa-tags` - 🏷️ Tags/Categories
- `fas fa-search` - 🔍 Search
- `fas fa-filter` - 🔽 Filters

### Arrows & Indicators
- `fas fa-chevron-right` - › Right arrow
- `fas fa-chevron-down` - ⬇ Down arrow
- `fas fa-arrow-right` - → Arrow
- `fas fa-angle-right` - › Angle
- `fas fa-angle-down` - ⬇ Angle

### Misc
- `fas fa-star` - ⭐ Star/Featured
- `fas fa-heart` - ❤️ Favorites
- `fas fa-book` - 📚 Books/Resources
- `fas fa-graduation-cap` - 🎓 Training/Courses
- `fas fa-calendar` - 📅 Calendar/Events
- `fas fa-map-marker-alt` - 📍 Location

## Icon Styles

- **`fas`** - Solid icons (filled in) - Default style
- **`far`** - Regular icons (outlined)
- **`fab`** - Brand icons (social media, etc.)

## Examples

```
Home              → fas fa-home
About Us          → fas fa-building
Our Services      → fas fa-concierge-bell
Products          → fas fa-box
Blog              → fas fa-newspaper
Gallery           → fas fa-images
Videos            → fas fa-video
Contact Us        → fas fa-envelope
FAQs              → fas fa-question-circle
Get a Quote       → fas fa-file-invoice-dollar
Login             → fas fa-sign-in-alt
Register          → fas fa-user-plus
```

## Tips

1. **Icons are optional** - Menu items work perfectly without icons
2. **Use sparingly** - Don't overuse icons, they work best for emphasis
3. **Be consistent** - Use the same icon style (fas, far, fab) throughout
4. **Test it** - Refresh your homepage to see icons in the navigation
5. **Browse more** - Visit https://fontawesome.com/icons?d=gallery&m=free for all free icons

## How It Looks

When editing a menu, you'll see:

```
┌─────────────────────────────────────────────────────────────────┐
│ Menu items                                                        │
├──────┬─────────────┬──────────────────┬──────────┬──────────────┤
│Order │ Title       │ Icon              │ Preview  │ Type         │
├──────┼─────────────┼──────────────────┼──────────┼──────────────┤
│  1   │ Home        │ fas fa-home       │   🏠      │ custom_link  │
│  2   │ About       │ fas fa-building   │   🏢      │ page         │
│  3   │ Services    │ fas fa-concierge- │   🔔      │ custom_link  │
│      │             │ bell              │          │              │
│  4   │ Contact     │ fas fa-envelope   │   ✉️      │ page         │
└──────┴─────────────┴──────────────────┴──────────┴──────────────┘
```

## Frontend Display

Icons will appear in your main navigation like this:

```
🏠 Home  🏢 About  🔔 Services  📦 Products  ✉️ Contact
```

And in dropdowns:

```
Services 🔽
  ├─ 🏗️ Engineering
  ├─ 🏠 Vastu Consulting
  └─ 📚 Training
```

---

**Need more icons?** Visit: https://fontawesome.com/icons?d=gallery&m=free
