from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from dashboard.models import Post, Category, Tag, Product, Gallery, GalleryImage

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with Vaastu and construction related content'

    def handle(self, *args, **options):
        self.stdout.write('Populating Vaastu and construction content...')

        # Get or create admin user
        # First try to get existing admin
        admin_user = User.objects.filter(
            Q(email='admin@himwatkhanda.com') | Q(username='admin')
        ).first()

        if admin_user:
            self.stdout.write(self.style.WARNING(f'Using existing admin user: {admin_user.email}'))
        else:
            admin_user = User.objects.create(
                username='admin_vastu',
                email='admin@himwatkhanda.com',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
                is_superuser=True,
            )
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.email}'))

        # ===== Create Categories =====
        categories_data = [
            {'name': 'Vastu Shastra', 'description': 'Ancient Indian science of architecture'},
            {'name': 'Construction', 'description': 'Building and construction techniques'},
            {'name': 'Remedies', 'description': 'Vastu remedies and corrections'},
            {'name': 'Vastu Tips', 'description': 'Practical Vastu tips for daily life'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['name'].lower().replace(' ', '-'),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'status': 'active',
                }
            )
            categories[category.name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # ===== Create Tags =====
        tags_data = ['Vastu', 'Construction', 'Architecture', 'Vastu Remedies',
                     'Building Design', 'Vastu Tips', 'Home Design', 'Vastu Consultation']

        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                slug=tag_name.lower().replace(' ', '-'),
                defaults={
                    'name': tag_name,
                    'status': 'active',
                }
            )
            tags[tag.name] = tag
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tag: {tag.name}'))

        # ===== Create 5 Posts =====
        posts_data = [
            {
                'title': 'Essential Vastu Principles for Home Construction',
                'slug': 'essential-vastu-principles-home-construction',
                'content': '''<h2>Introduction to Vastu Shastra in Construction</h2>
<p>Vastu Shastra, the ancient Indian science of architecture, offers timeless principles for creating harmonious living spaces. When building a new home, incorporating Vastu principles from the ground up ensures positive energy flow and prosperity for inhabitants.</p>

<h3>1. Orientation and Placement</h3>
<p>The orientation of your home is crucial in Vastu. The main entrance should ideally face north or east to receive maximum beneficial sunlight. The kitchen should be located in the southeast corner, while the master bedroom is best placed in the southwest direction.</p>

<h3>2. Room Layout Guidelines</h3>
<ul>
<li><strong>Living Room:</strong> North or east facing for positive energy</li>
<li><strong>Kitchen:</strong> Southeast corner, with cooking platform facing east</li>
<li><strong>Master Bedroom:</strong> Southwest direction for stability</li>
<li><strong>Pooja Room:</strong> Northeast corner, the most sacred direction</li>
<li><strong>Bathroom:</strong> West or northwest directions</li>
</ul>

<h3>3. Foundation and Construction Materials</h3>
<p>Start construction during an auspicious time after consulting a Vastu expert. Use high-quality materials and ensure the foundation is strong. The boundary walls should be slightly higher in the south and west directions.</p>

<h3>4. Windows and Ventilation</h3>
<p>Windows should be larger in the north and east for maximum sunlight. The number of windows and doors should be even (2, 4, 6, etc.) for optimal energy flow. Proper cross-ventilation ensures fresh air circulation.</p>

<h3>5. Water Storage and Drainage</h3>
<p>Underground water tanks should be in the northeast. Overhead tanks work best in the southwest. Ensure drainage flows toward the northeast corner of the property.</p>

<p>Following these Vastu principles during construction creates a home that promotes health, wealth, and happiness for all residents.</p>''',
                'excerpt': 'Learn essential Vastu Shastra principles for constructing your dream home. From orientation to room placement, discover how to build harmonious living spaces.',
                'category': 'Vastu Shastra',
                'tags': ['Vastu', 'Construction', 'Architecture', 'Home Design'],
                'status': 'published',
                'published_at': timezone.now(),
            },
            {
                'title': '5 Powerful Vastu Remedies for Construction Flaws',
                'slug': 'powerful-vastu-remedies-construction-flaws',
                'content': '''<h2>Correcting Vastu Doshas in Your Home</h2>
<p>Every home may have some Vastu defects (doshas), but don't worry! There are powerful remedies that can help neutralize negative effects and bring positive energy into your living space.</p>

<h3>1. Sea Salt for Negative Energy Removal</h3>
<p>Place a bowl of sea salt in the northeast corner of your home. Sea salt is an excellent energy purifier and absorbs negative energy. Replace it every week. You can also add sea salt to your mop water for regular cleaning.</p>

<h3>2. Crystal Pyramid for Energy Correction</h3>
<p>Install a crystal pyramid in the center of your home (Brahmasthan). Pyramids are powerful energy generators that help balance and distribute positive energy throughout the house. They're especially effective for correcting Vastu defects in the center of the structure.</p>

<h3>3. Wind Chimes for Energy Flow</h3>
<p>Hang metal wind chimes near the main entrance or windows. The soothing sound activates positive energy and helps it flow smoothly throughout your home. Use bamboo chimes for the east direction and metal for the west.</p>

<h3>4. Mirror Placement for Space Extension</h3>
<p>If your home has a cut or missing corner, place a mirror on that wall to visually extend the space. However, avoid placing mirrors directly opposite the main entrance or in bedrooms where they reflect the bed while sleeping.</p>

<h3>5. Tulsi (Holy Basil) Plant</h3>
<p>Plant a Tulsi in the northeast direction of your home or garden. Tulsi is considered sacred in Vastu and purifies the air while emitting positive energy. It's one of the most powerful natural remedies for Vastu correction.</p>

<p>These simple yet effective remedies can significantly improve the Vastu of your home without major structural changes. For serious Vastu issues, always consult a professional Vastu consultant.</p>''',
                'excerpt': 'Discover 5 powerful Vastu remedies to correct construction flaws and bring positive energy into your home without major renovations.',
                'category': 'Remedies',
                'tags': ['Vastu', 'Vastu Remedies', 'Vastu Tips'],
                'status': 'published',
                'published_at': timezone.now(),
            },
            {
                'title': 'Vastu for Different Rooms: Complete Room-by-Room Guide',
                'slug': 'vastu-different-rooms-complete-guide',
                'content': '''<h2>Room-by-Room Vastu Guide</h2>
<p>Each room in your home serves a different purpose, and Vastu Shastra provides specific guidelines for each space to maximize positive energy and functionality.</p>

<h3>Living Room Vastu</h3>
<p>The living room should be located in the north, east, or northeast direction. Place heavy furniture in the south or west. The owner should sit facing north or east when hosting guests. Use light, pleasant colors for walls.</p>

<h3>Bedroom Vastu</h3>
<p>Master bedrooms belong in the southwest for stability and better sleep. Children's bedrooms work best in the northwest or west. Avoid bedrooms in the northeast. Sleep with your head facing south or east for better health and rest.</p>

<h3>Kitchen Vastu</h3>
<p>The ideal kitchen location is the southeast corner. If that's not possible, northwest is the second-best option. The cooking platform should face east. Keep the cooking gas away from the sink to avoid fire and water clashes.</p>

<h3>Bathroom Vastu</h3>
<p>Bathrooms should be in the west, northwest, or south directions. Avoid northeast bathrooms at all costs. Ensure proper drainage and ventilation. Keep the door closed when not in use to prevent negative energy from spreading.</p>

<h3>Pooja Room Vastu</h3>
<p>The prayer room should be in the northeast corner, the most auspicious direction. Face east or north while praying. Keep the space clean, clutter-free, and use only religious items here. Never place a pooja room under a staircase.</p>

<h3>Study Room Vastu</h3>
<p>The study room should be in the west, northwest, or east. The study table should face east or north for better concentration. Bookshelves work well in the southwest or west walls of the room.</p>

<h3>Home Office Vastu</h3>
<p>For those working from home, place your office in the west or southwest. Sit facing north while working. Keep electronic equipment in the southeast corner. Avoid placing your desk directly under a beam.</p>

<p>Following these room-specific Vastu guidelines ensures each space serves its purpose while maintaining harmony and positive energy throughout your home.</p>''',
                'excerpt': 'Complete Vastu guide for every room in your home. Learn optimal placement and design principles for living rooms, bedrooms, kitchens, bathrooms, and more.',
                'category': 'Vastu Tips',
                'tags': ['Vastu', 'Vastu Tips', 'Home Design', 'Vastu Consultation'],
                'status': 'published',
                'published_at': timezone.now(),
            },
            {
                'title': 'Vastu Compliant Construction: Materials and Techniques',
                'slug': 'vastu-compliant-construction-materials-techniques',
                'content': '''<h2>Building with Vastu: Materials and Methods</h2>
<p>Constructing a Vastu-compliant home goes beyond just layout and orientation. The materials you choose and construction techniques you employ play a significant role in creating a harmonious living space.</p>

<h3>Foundation Construction</h3>
<p>Start excavation from the northeast corner and proceed clockwise. The foundation should be stronger and slightly higher in the south and west. Always begin foundation laying during an auspicious time after consulting Vastu calendar (muhurat).</p>

<h3>Building Materials</h3>
<p><strong>Bricks and Stones:</strong> Use consistent quality materials throughout. Avoid mixing old and new materials. Red bricks are considered auspicious in Vastu.</p>
<p><strong>Cement and Concrete:</strong> Use high-grade cement for durability. The concrete mix should be consistent throughout the construction.</p>
<p><strong>Wood:</strong> Teak and deodar are considered most auspicious. Avoid using old or reclaimed wood from demolished structures.</p>
<p><strong>Metal:</strong> Use quality steel reinforcement. Iron fixtures should be rust-resistant and durable.</p>

<h3>Wall Construction</h3>
<p>The south and west walls should be thicker and higher than north and east walls. This provides stability and protection. Maintain 90-degree angles where possible. Avoid irregular shapes or cuts in corners.</p>

<h3>Flooring Guidelines</h3>
<p><strong>Ground Floor:</strong> Use marble or granite for positive energy. The flooring should slope slightly toward the northeast for proper drainage.</p>
<p><strong>Upper Floors:</strong> Use lighter materials on upper floors. Avoid heavy stone flooring on higher levels.</p>

<h3>Door and Window Construction</h3>
<p>Main doors should be substantial and made of quality wood. Avoid doors with metal fixtures that make harsh sounds. Windows should be larger in north and east, smaller in south and west. Ensure all doors open clockwise.</p>

<h3>Roof Construction</h3>
<p>The roof should slope toward the north or east. Flat roofs with a slight north-east slope are ideal. Avoid domes or pyramids on residential structures unless specifically designed by a Vastu expert.</p>

<h3>Water and Electrical Systems</h3>
<p>Install water systems in the northeast. Electrical panels and main switches work best in the southeast. Underground tanks go in northeast, overhead tanks in southwest.</p>

<h3>Construction Timing</h3>
<p>Follow the Vastu calendar for auspicious dates (muhurat). Avoid construction during inauspicious periods. Perform ground-breaking ceremony (Bhoomi Pujan) before starting construction.</p>

<p>Using Vastu-compliant materials and techniques ensures your home not only looks beautiful but also promotes health, prosperity, and happiness for generations.</p>''',
                'excerpt': 'Learn about Vastu-compliant construction materials and techniques. From foundation to roofing, discover how to build using traditional Vastu principles.',
                'category': 'Construction',
                'tags': ['Vastu', 'Construction', 'Architecture', 'Building Design'],
                'status': 'published',
                'published_at': timezone.now(),
            },
            {
                'title': 'Common Vastu Mistakes in Modern Construction and How to Fix Them',
                'slug': 'common-vastu-mistakes-modern-construction-fix',
                'content': '''<h2>Avoiding Vastu Pitfalls in Modern Homes</h2>
<p>Modern construction often prioritizes aesthetics over Vastu principles, leading to spaces that may look beautiful but don't promote positive energy flow. Here are common Vastu mistakes and their solutions.</p>

<h3>Mistake 1: Main Entrance in Wrong Direction</h3>
<p><strong>Problem:</strong> Many modern homes have entrance gates in the south or southwest, which is considered inauspicious in Vastu.</p>
<p><strong>Solution:</strong> If moving the entrance isn't possible, create a smaller entrance in the north or east and use it as the main entry. Place a Swastik or Om symbol above the south entrance.</p>

<h3>Mistake 2: Kitchen in Northeast</h3>
<p><strong>Problem:</strong> Placing the kitchen in the northeast disturbs the energy zone and can affect health.</p>
<p><strong>Solution:</strong> If relocation isn't possible, paint the kitchen yellow. Place a green plant in the northeast corner of the kitchen. Use gas stove facing east to mitigate effects.</p>

<h3>Mistake 3: Bathroom in Northeast</h3>
<p><strong>Problem:</strong> Northeast bathrooms are among the most serious Vastu defects, affecting prosperity and health.</p>
<p><strong>Solution:</strong> Keep the bathroom door always closed. Place sea salt in a bowl here. Use lemon essential oil for cleaning. Consider converting it to a store room if possible.</p>

<h3>Mistake 4: Bedroom Under Beam</h3>
<p><strong>Problem:</strong> Sleeping under a concrete beam causes health issues and disturbed sleep.</p>
<p><strong>Solution:</strong> Hang two flutes tied with red thread on the beam. Alternatively, create a false ceiling to cover the beam. Move the bed if possible.</p>

<h3>Mistake 5: Cut or Extended Corners</h3>
<p><strong>Problem:</strong> Missing or extended corners disrupt the energy balance of the structure.</p>
<p><strong>Solution:</strong> For cut corners, place mirrors on the wall. For extended corners, use heavy furniture or plants to balance the energy. Install pyramids in affected areas.</p>

<h3>Mistake 6: Central Pillar or Column</h3>
<p><strong>Problem:</strong> A pillar in the center (Brahmasthan) blocks energy flow.</p>
<p><strong>Solution:</strong> Create a circular passage around the pillar. Hang a crystal at the top of the pillar. Use climbing plants around the base to soften the energy.</p>

<h3>Mistake 7: Wrong Staircase Placement</h3>
<p><strong>Problem:</strong> Staircases in the northeast block positive energy entry.</p>
<p><strong>Solution:</strong> The ideal staircase location is south or west. If relocation isn't possible, place a pyramids at the base and top of stairs. Ensure stairs don't touch the northeast wall.</p>

<h3>Mistake 8: Underground Tank in Southwest</h3>
<p><strong>Problem:</strong> Water in the southwest creates instability and financial problems.</p>
<p><strong>Solution:</strong> If moving isn't possible, install a heavy crystal pyramid. Paint the southwest area red. Avoid using this tank if alternative water source exists.</p>

<h3>Mistake 9: Paint Colors Not Vastu Compliant</h3>
<p><strong>Problem:</strong> Using dark or inappropriate colors creates negative energy.</p>
<p><strong>Solution:</strong> Use light, soothing colors. Blue and white for north, green for northeast, reds for southeast (kitchen), yellows for northeast.</p>

<h3>Mistake 10: Cluttered Spaces</h3>
<p><strong>Problem:</strong> Clutter, especially in the northeast, blocks positive energy.</p>
<p><strong>Solution:</strong> Keep the northeast clean and clutter-free. Remove unnecessary items regularly. Create organized storage systems throughout the house.</p>

<p>Understanding these common mistakes and implementing their solutions can significantly improve the Vastu of your modern home, creating a space that's both aesthetically pleasing and energetically balanced.</p>''',
                'excerpt': 'Identify and fix common Vastu mistakes in modern construction. Learn practical solutions for entrance placement, room locations, and structural issues.',
                'category': 'Vastu Shastra',
                'tags': ['Vastu', 'Construction', 'Vastu Remedies', 'Vastu Tips'],
                'status': 'published',
                'published_at': timezone.now(),
            },
        ]

        for post_data in posts_data:
            # Extract tags and remove from dict
            tag_names = post_data.pop('tags', [])
            category_name = post_data.pop('category', None)

            # Get or create post
            post, created = Post.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    **post_data,
                    'author': admin_user,
                    'category': categories.get(category_name),
                }
            )

            if created:
                # Add tags
                for tag_name in tag_names:
                    if tag_name in tags:
                        post.tags.add(tags[tag_name])
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Post already exists: {post.title}'))

        # ===== Create 5 Products =====
        products_data = [
            {
                'name': 'Vastu Crystal Pyramid Set',
                'slug': 'vastu-crystal-pyramid-set',
                'description': '''<h2>Premium Crystal Pyramid Set for Vastu Correction</h2>
<p>This beautiful set of 7 crystal pyramids is designed to correct Vastu defects and bring positive energy into your home or office. Each pyramid is crafted from high-quality clear crystal and energized according to traditional Vastu principles.</p>

<h3>Key Features:</h3>
<ul>
<li>7 pyramids of varying sizes (1 inch to 3 inches)</li>
<li>Premium clear crystal construction</li>
<li>Energized and blessed</li>
<li>Ideal for correcting Vastu doshas</li>
<li>Enhances positive energy flow</li>
<li>Perfect for home and office use</li>
</ul>

<h3>Benefits:</h3>
<ul>
<li>Neutralizes negative energy</li>
<li>Promotes prosperity and success</li>
<li>Improves health and well-being</li>
<li>Enhances concentration and focus</li>
<li>Creates harmonious environment</li>
</ul>

<h3>Placement Instructions:</h3>
<p>Place the largest pyramid in the center of your home (Brahmasthan). Distribute smaller pyramids to different rooms according to Vastu defects. The pyramids work best when placed on a clean, elevated surface.</p>''',
                'category': 'vastu_remedy',
                'featured': True,
                'sort_order': 1,
            },
            {
                'name': 'Vastu Compass with Direction Guide',
                'slug': 'vastu-compass-direction-guide',
                'description': '''<h2>Professional Vastu Compass</h2>
<p>This specially designed Vastu compass helps you determine the correct directions for constructing your Vastu-compliant home. Features a clear dial with markings for all 16 directions and comes with a comprehensive direction guide.</p>

<h3>Product Features:</h3>
<ul>
<li>Precision-engineered magnetic needle</li>
<li>Clear 16-direction markings</li>
<li>Compact and portable design</li>
<li>Includes comprehensive direction guide booklet</li>
<li>Weather-resistant construction</li>
<li>Ideal for architects, builders, and homeowners</li>
</ul>

<h3>What's Included:</h3>
<ul>
<li>Vastu Compass (2 inch diameter)</li>
<li>Direction Guide Booklet</li>
<li>Protective carrying case</li>
<li>Online access to detailed tutorials</li>
</ul>

<h3>Usage:</h3>
<p>Use this compass to determine the correct orientation for your home, rooms, kitchen, and other important areas. The guide booklet provides detailed instructions for optimal placement according to Vastu Shastra.</p>''',
                'category': 'vastu_product',
                'featured': True,
                'sort_order': 2,
            },
            {
                'name': 'Vastu Salt Remedy Kit',
                'slug': 'vastu-salt-remedy-kit',
                'description': '''<h2>Complete Vastu Salt Remedy Kit</h2>
<p>A powerful collection of salt-based remedies for removing negative energy and correcting Vastu defects. This kit includes various types of salt with detailed instructions for different Vastu corrections.</p>

<h3>Kit Contents:</h3>
<ul>
<li>Sea Salt (500g) - For general energy purification</li>
<li>Rock Salt (Himalayan Pink Salt - 300g) - For strong dosha correction</li>
<li>Black Salt (200g) - For removing evil eye</li>
<li>Lava Salt (150g) - For Vastu protection</li>
<li>Detailed instruction manual</li>
<li>Placement guide for different rooms</li>
</ul>

<h3>Benefits:</h3>
<ul>
<li>Removes negative energy</li>
<li>Purifies living spaces</li>
<li>Corrects Vastu doshas</li>
<li>Protects from evil eye</li>
<li>Promotes positivity and peace</li>
</ul>

<h3>How to Use:</h3>
<p>The included manual provides detailed instructions for using each type of salt for different Vastu corrections. Simple and effective remedies that anyone can implement.</p>''',
                'category': 'vastu_remedy',
                'featured': False,
                'sort_order': 3,
            },
            {
                'name': 'Complete Vastu Shastra Guide Book',
                'slug': 'complete-vastu-shastra-guide-book',
                'description': '''<h2>Comprehensive Vastu Shastra Guide Book</h2>
<p>This complete guide to Vastu Shastra covers everything from basic principles to advanced applications. Written by Vastu experts, this book is an essential resource for anyone interested in Vastu-compliant construction.</p>

<h3>Book Contents:</h3>
<ul>
<li>Introduction to Vastu Shastra</li>
<li>Five Elements Theory</li>
<li>Eight Directions and Their Significance</li>
<li>Vastu for Home Construction</li>
<li>Room-by-Room Vastu Guidelines</li>
<li>Vastu for Office and Business</li>
<li>Vastu Remedies and Corrections</li>
<li>Vastu for Different Professions</li>
<li>Case Studies and Examples</li>
<li>Practical Tips and Checklists</li>
</ul>

<h3>Features:</h3>
<ul>
<li>400+ pages of detailed content</li>
<li>100+ illustrations and diagrams</li>
<li>50+ case studies</li>
<li>Easy-to-follow guidelines</li>
<li>Practical remedies for common problems</li>
<li>Sanskrit shlokas with translations</li>
</ul>

<h3>Who Should Read:</h3>
<ul>
<li>Homeowners planning construction</li>
<li>Architects and interior designers</li>
<li>Builders and contractors</li>
<li>Vastu consultants and students</li>
<li>Anyone interested in Vastu Shastra</li>
</ul>''',
                'category': 'book',
                'featured': True,
                'sort_order': 4,
            },
            {
                'name': 'Professional Vastu Consultation',
                'slug': 'professional-vastu-consultation',
                'description': '''<h2>Expert Vastu Consultation Service</h2>
<p>Get personalized Vastu guidance from our certified Vastu consultants. Whether you're planning new construction, renovating, or simply want to improve the Vastu of your existing space, our experts provide comprehensive solutions.</p>

<h3>Consultation Includes:</h3>
<ul>
<li>Complete site analysis and evaluation</li>
<li>Detailed Vastu assessment report</li>
<li>Orientation and layout recommendations</li>
<li>Room placement and design guidance</li>
<li>Remedies for existing Vastu defects</li>
<li>Follow-up support</li>
</ul>

<h3>Consultation Types:</h3>
<ul>
<li><strong>New Construction:</strong> Complete guidance from planning to completion</li>
<li><strong>Existing Property:</strong> Assessment and remedies for current homes</li>
<li><strong>Commercial:</strong> Vastu for offices, shops, and businesses</li>
<li><strong>Industrial:</strong> Factory and industrial Vastu consultation</li>
<li><strong>Online:</strong> Remote consultation via video call</li>
</ul>

<h3>What You Get:</h3>
<ul>
<li>Detailed Vastu analysis (50+ pages)</li>
<li>Floor plan review and recommendations</li>
<li>Priority email and phone support</li>
<li>Remedy implementation guide</li>
<li>Follow-up session included</li>
</ul>

<h3>Process:</h3>
<ol>
<li>Book your consultation</li>
<li>Submit your floor plans and requirements</li>
<li>Schedule consultation session</li>
<li>Receive detailed Vastu report</li>
<li>Get support for implementation</li>
</ol>''',
                'category': 'consultation',
                'featured': True,
                'sort_order': 5,
            },
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'created_by': admin_user,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))

        # ===== Create 5 Galleries =====
        galleries_data = [
            {
                'name': 'Vastu Compliant Homes',
                'slug': 'vastu-compliant-homes',
                'description': 'Beautiful examples of Vastu-compliant homes that blend traditional principles with modern architecture.',
                'sort_order': 1,
            },
            {
                'name': 'Temple Architecture',
                'slug': 'temple-architecture',
                'description': 'Traditional temple architecture showcasing the finest examples of Vastu Shastra in religious structures.',
                'sort_order': 2,
            },
            {
                'name': 'Vastu Office Spaces',
                'slug': 'vastu-office-spaces',
                'description': 'Modern office and commercial spaces designed according to Vastu principles for prosperity and success.',
                'sort_order': 3,
            },
            {
                'name': 'Traditional Nepali Architecture',
                'slug': 'traditional-nepali-architecture',
                'description': 'Explore traditional Nepali architecture that naturally incorporates Vastu principles in its design.',
                'sort_order': 4,
            },
            {
                'name': 'Vastu Interior Design',
                'slug': 'vastu-interior-design',
                'description': 'Interior design ideas that follow Vastu guidelines for creating harmonious living spaces.',
                'sort_order': 5,
            },
        ]

        for gallery_data in galleries_data:
            gallery, created = Gallery.objects.get_or_create(
                slug=gallery_data['slug'],
                defaults={
                    **gallery_data,
                    'created_by': admin_user,
                    'status': 'active',
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created gallery: {gallery.name}'))

                # Add placeholder images for each gallery
                # In production, these would be real images
                for i in range(3):
                    GalleryImage.objects.create(
                        gallery=gallery,
                        title=f'{gallery.name} - Image {i+1}',
                        description=f'Sample image {i+1} for {gallery.name}',
                        image=f'galleries/samples/{gallery.slug}_{i+1}.jpg',  # Placeholder path
                        sort_order=i,
                    )
                self.stdout.write(self.style.SUCCESS(f'  Added 3 placeholder images to {gallery.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Gallery already exists: {gallery.name}'))

        self.stdout.write(self.style.SUCCESS('Content population complete!'))
        self.stdout.write(self.style.SUCCESS(f'Created: {len(posts_data)} posts, {len(products_data)} products, {len(galleries_data)} galleries'))
