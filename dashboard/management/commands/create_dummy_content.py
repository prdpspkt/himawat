from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from dashboard.models import (
    Post, Page, Category, Tag, Download, Gallery, GalleryImage,
    Testimonial, Carousel, FAQ, Product, ProductImage, Video
)
import random
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Create dummy content for development and testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy content...')

        # Get or create a user
        try:
            user = User.objects.filter(is_staff=True).first()
            if not user:
                user = User.objects.create_user(
                    username='admin',
                    email='admin@himawat.com',
                    first_name='Admin',
                    last_name='User',
                    password='admin123',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True,
                    role='admin',
                    status='active',
                )
                self.stdout.write('Created admin user: admin@himawat.com / admin123')
            else:
                self.stdout.write(f'Using existing user: {user.email}')
        except Exception as e:
            self.stdout.write(f'Error creating user: {e}')
            # Try to get any user
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR('No users in database. Please create a user first.'))
                return

        # Create Categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Vastu Shastra', 'description': 'Ancient Indian science of architecture'},
            {'name': 'Construction', 'description': 'Building and construction techniques'},
            {'name': 'Interior Design', 'description': 'Interior design principles'},
            {'name': 'Vastu Remedies', 'description': 'Remedies for Vastu defects'},
            {'name': 'Case Studies', 'description': 'Real-world Vastu implementations'},
        ]
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['name'].lower().replace(' ', '-'),
                defaults={**cat_data, 'status': 'active'}
            )
            categories.append(cat)

        # Create Tags
        self.stdout.write('Creating tags...')
        tags_data = [
            'vastu', 'construction', 'architecture', 'design', 'remedies',
            'tips', 'guidelines', 'residential', 'commercial', 'interior'
        ]
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                slug=tag_name,
                defaults={'name': tag_name, 'status': 'active'}
            )
            tags.append(tag)

        # Create Posts
        self.stdout.write('Creating blog posts...')
        posts_data = [
            {
                'title': 'Introduction to Vastu Shastra for Modern Homes',
                'excerpt': 'Learn the fundamental principles of Vastu Shastra and how to apply them to modern home design.',
                'content': '''<h2>Understanding Vastu Shastra</h2>
<p>Vastu Shastra is an ancient Indian science of architecture that harmonizes nature with human dwellings. The principles focus on directions, elements, and energy flow to create peaceful living spaces.</p>

<h3>Five Elements of Vastu</h3>
<ul>
<li><strong>Earth (Prithvi)</strong> - Stability and strength</li>
<li><strong>Water (Jal)</strong> - Fluidity and emotional balance</li>
<li><strong>Fire (Agni)</strong> - Energy and transformation</li>
<li><strong>Air (Vayu)</strong> - Movement and freshness</li>
<li><strong>Space (Akasha)</strong> - Openness and expansion</li>
</ul>

<h3>Key Principles</h3>
<p>The main entrance should face north or east for positive energy. The kitchen should be in the southeast corner, while bedrooms work best in the southwest. These guidelines help create harmonious environments.</p>''',
                'category': categories[0],
                'status': 'published',
            },
            {
                'title': '10 Essential Vastu Tips for New Construction',
                'excerpt': 'Before you start building your dream home, consider these vital Vastu principles.',
                'content': '''<h2>Pre-Construction Vastu Planning</h2>
<p>Building a new home is the perfect opportunity to incorporate Vastu principles from the ground up. Here are essential tips:</p>

<h3>1. Site Selection</h3>
<p>Choose a plot with a regular shape. Avoid irregular or cut-corner plots. The soil should be firm and fertile.</p>

<h3>2. Orientation Matters</h3>
<p>The main entrance is crucial. East and north-facing entrances are considered most auspicious. Avoid south-facing main doors.</p>

<h3>3. Room Placement</h3>
<ul>
<li>Living Room: North or East</li>
<li>Kitchen: Southeast corner</li>
<li>Master Bedroom: Southwest</li>
<li>Bathrooms: Northwest or Southeast</li>
<li>Prayer Room: Northeast</li>
</ul>

<h3>4. Ventilation and Light</h3>
<p>Ensure cross-ventilation with windows on opposite walls. Maximum windows should be on the north and east walls.</p>''',
                'category': categories[1],
                'status': 'published',
            },
            {
                'title': 'Vastu Remedies for Existing Homes',
                'excerpt': 'Already have a home? Learn simple remedies to correct Vastu defects without major renovations.',
                'content': '''<h2>Correcting Vastu Defects</h2>
<p>Don't worry if your home has Vastu defects. There are simple remedies that can help balance the energy without demolition.</p>

<h3>Common Remedies</h3>

<h4>Entrance Problems</h4>
<p>If your main entrance is in an inauspicious direction, place a pyramid or crystal above the door. Use a nameplate with bright colors.</p>

<h4>Missing Corners</h4>
<p>For missing corners in your plot, install mirrors on the walls to visually extend the space. Use crystal balls or pyramids.</p>

<h4>Bathroom Location</h4>
<p>If a bathroom is in the northeast, keep the door closed at all times. Use sea salt in bowls and replace weekly.</p>

<h4>Kitchen Issues</h4>
<p>Place a small mirror on the east wall of the kitchen if it's not in the southeast. Keep the stove clean and in working order.</p>

<h3>Simple Techniques</h3>
<ul>
<li>Use wind chimes at entrances</li>
<li>Place crystals in strategic locations</li>
<li>Grow plants in the northeast</li>
<li>Use essential oils and aromatherapy</li>
<li>Display happy family photos</li>
</ul>''',
                'category': categories[3],
                'status': 'published',
            },
            {
                'title': 'Vastu for Home Offices: Boost Productivity',
                'excerpt': 'Create a workspace that enhances focus, creativity, and prosperity using Vastu principles.',
                'content': '''<h2>Optimizing Your Home Office</h2>
<p>With more people working from home, creating a Vastu-compliant home office is essential for productivity and success.</p>

<h3>Ideal Location</h3>
<p>The best location for a home office is the west or northwest zone. This governs business, career, and prosperity. Avoid the northeast as this is for meditation and spiritual activities.</p>

<h3>Desk Position</h3>
<ul>
<li>Face east or north while working</li>
<li>Keep a solid wall behind your chair</li>
<li>Avoid sitting under a beam</li>
<li>Ensure there's space in front of the desk</li>
</ul>

<h3>Lighting and Colors</h3>
<p>Use bright, natural light. Add blue or green elements for calmness. Yellow and white promote clarity and focus.</p>

<h3>What to Include</h3>
<ul>
<li>A crystal paperweight</li>
<li>Healthy plants (money plant, bamboo)</li>
<li>Inspirational quotes or art</li>
<li>Adequate storage for organization</li>
</ul>''',
                'category': categories[2],
                'status': 'published',
            },
            {
                'title': 'Case Study: Vastu Transformation of a Commercial Complex',
                'excerpt': 'See how proper Vastu implementation transformed a struggling commercial building into a thriving business hub.',
                'content': '''<h2>Project Overview</h2>
<p>This case study examines a commercial complex in Kathmandu that was experiencing high vacancy rates and business failures.</p>

<h3>Initial Assessment</h3>
<p><strong>Issues Identified:</strong></p>
<ul>
<li>Main entrance facing south</li>
<li>Toilets in the northeast corner</li>
<li>Irregular-shaped shops</li>
<li>Poor ventilation and natural light</li>
</ul>

<h3>Vastu Recommendations</h3>
<p>We implemented several remedies:</p>
<ol>
<li>Entrance enhancement with pyramids and crystals</li>
<li>Color therapy using appropriate shades</li>
<li>Relocated toilets where possible</li>
<li>Installed mirrors and lights for correction</li>
<li>Added plants and water features</li>
</ol>

<h3>Results</h3>
<p>Within six months, occupancy increased from 40% to 85%. Business owners reported improved customer flow and sales. The overall energy of the complex transformed noticeably.</p>

<h3>Key Takeaways</h3>
<p>Even existing structures can benefit from Vastu corrections. Simple, non-destructive remedies can significantly improve outcomes.</p>''',
                'category': categories[4],
                'status': 'published',
            },
        ]

        for post_data in posts_data:
            post, created = Post.objects.get_or_create(
                slug=post_data['title'].lower().replace(' ', '-').replace(':', ''),
                defaults={
                    **post_data,
                    'author': user,
                    'keywords': 'vastu, construction, design',
                    'view_count': random.randint(100, 5000),
                }
            )
            if created:
                # Add random tags
                post.tags.set(random.sample(tags, 3))
                self.stdout.write(f'  Created post: {post.title}')

        # Create Pages
        self.stdout.write('Creating pages...')
        pages_data = [
            {
                'title': 'About Us',
                'slug': 'about',
                'template': 'about',
                'content': '''<h2>Welcome to Himwatkhanda Vastu</h2>
<p>We are dedicated to bringing the ancient wisdom of Vastu Shastra to modern construction and design. Our team of experts combines traditional knowledge with contemporary architectural practices.</p>

<h3>Our Mission</h3>
<p>To help individuals and businesses create harmonious living and working spaces that promote health, prosperity, and happiness through Vastu principles.</p>

<h3>Why Choose Us</h3>
<ul>
<li>20+ years of experience in Vastu consultation</li>
<li>Certified Vastu consultants</li>
<li>Proven track record with 500+ projects</li>
<li>Comprehensive solutions for residential and commercial properties</li>
</ul>

<h3>Our Approach</h3>
<p>We believe in practical, implementable solutions. Whether you're planning new construction or looking to remedy existing structures, we provide customized guidance that works for your specific situation.</p>''',
                'status': 'active',
                'order': 1,
            },
            {
                'title': 'Contact Us',
                'slug': 'contact',
                'template': 'contact',
                'content': '''<h2>Get in Touch</h2>
<p>Have questions about Vastu for your property? We're here to help!</p>

<h3>Contact Information</h3>
<ul>
<li><strong>Address:</strong> Kathmandu, Nepal</li>
<li><strong>Email:</strong> info@himawatkhandavastu.com</li>
<li><strong>Phone:</strong> +977-1-XXXXXXX</li>
</ul>

<h3>Services We Offer</h3>
<ul>
<li>Residential Vastu Consultation</li>
<li>Commercial Property Analysis</li>
<li>Construction Planning</li>
<li>Vastu Remedies</li>
<li>Interior Design Guidance</li>
</ul>

<h3>Consultation Hours</h3>
<p>Monday - Saturday: 10:00 AM - 6:00 PM</p>''',
                'status': 'active',
                'order': 2,
            },
            {
                'title': 'Services',
                'slug': 'services',
                'content': '''<h2>Our Services</h2>
<p>Comprehensive Vastu solutions for all your needs.</p>

<h3>Residential Consultation</h3>
<p>Complete Vastu analysis for homes, apartments, and villas. We provide detailed reports with practical recommendations.</p>

<h3>Commercial Projects</h3>
<p>Vastu planning for offices, shops, factories, and commercial complexes to enhance business success.</p>

<h3>Construction Guidance</h3>
<p>End-to-end Vastu consultation for new construction projects, from site selection to final layout planning.</p>

<h3>Remedies & Corrections</h3>
<p>Simple yet effective remedies for existing properties without structural changes.</p>''',
                'status': 'active',
                'order': 3,
            },
        ]

        for page_data in pages_data:
            page, created = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults={**page_data, 'meta_title': page_data['title']}
            )
            if created:
                self.stdout.write(f'  Created page: {page.title}')

        # Create Products
        self.stdout.write('Creating products...')
        products_data = [
            {
                'name': 'Vastu Crystal Pyramid Set',
                'category': 'vastu_remedy',
                'description': '''<h3>Premium Crystal Pyramid Set</h3>
<p>A set of 7 crystal pyramids for Vastu correction. Each pyramid is energized and ready to use.</p>

<h4>Includes:</h4>
<ul>
<li>7 different colored crystal pyramids</li>
<li>Placement guide</li>
<li>Energization instructions</li>
</ul>

<h4>Benefits:</h4>
<ul>
<li>Corrects Vastu defects</li>
<li>Enhances positive energy</li>
<li>Improves concentration</li>
<li>Promotes prosperity</li>
</ul>''',
                'status': 'active',
                'featured': True,
                'sort_order': 1,
            },
            {
                'name': 'Vastu Compass',
                'category': 'vastu_product',
                'description': '''<h3>Professional Vastu Compass</h3>
<p>High-quality brass compass for accurate direction reading. Essential for Vastu analysis.</p>

<h4>Features:</h4>
<ul>
<li>Pure brass construction</li>
<li>Accurate needle</li>
<li>Detailed degree markings</li>
<li>Protective case included</li>
</ul>

<h4>Use:</h4>
<p>Determine exact directions for rooms, entrances, and furniture placement.</p>''',
                'status': 'active',
                'featured': True,
                'sort_order': 2,
            },
            {
                'name': 'Vastu for Beginners - Book',
                'category': 'book',
                'description': '''<h3>Complete Guide to Vastu Shastra</h3>
<p>Comprehensive book covering all aspects of Vastu for beginners and practitioners alike.</p>

<h4>Contents:</h4>
<ul>
<li>History and principles</li>
<li>Step-by-step guidelines</li>
<li>Case studies</li>
<li>Remedies and solutions</li>
<li>Illustrations and diagrams</li>
</ul>

<h4>272 pages | Paperback | English/Nepali</h4>''',
                'status': 'active',
                'featured': False,
                'sort_order': 3,
            },
            {
                'name': 'Vastu Consultation - Residential',
                'category': 'consultation',
                'description': '''<h3>Complete Home Vastu Analysis</h3>
<p>Professional Vastu consultation for your home. Includes detailed report and remedies.</p>

<h4>What's Included:</h4>
<ul>
<li>Site visit and analysis</li>
<li>Detailed Vastu report (50+ pages)</li>
<li>3D energy mapping</li>
<li>Remedies and recommendations</li>
<li>Follow-up support</li>
</ul>

<h4>Process:</h4>
<ol>
<li>Schedule appointment</li>
<li>Site visit (2-3 hours)</li>
<li>Report delivery within 7 days</li>
<li>Implementation guidance</li>
</ol>''',
                'status': 'active',
                'featured': True,
                'sort_order': 4,
            },
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['name'].lower().replace(' ', '-').replace(' - ', '-'),
                defaults={**product_data, 'created_by': user}
            )
            if created:
                self.stdout.write(f'  Created product: {product.name}')

        # Create FAQs
        self.stdout.write('Creating FAQs...')
        faqs_data = [
            {
                'question': 'What is Vastu Shastra?',
                'answer': 'Vastu Shastra is an ancient Indian science of architecture that describes principles of design, layout, measurements, ground preparation, space arrangement, and spatial geometry. It helps create harmonious living spaces by balancing the five elements of nature.',
                'category': 'vastu',
                'status': 'active',
                'sort_order': 1,
            },
            {
                'question': 'How long does a Vastu consultation take?',
                'answer': 'A typical residential consultation takes 2-3 hours for the site visit. The complete report is delivered within 7 days. For larger commercial projects, the timeline may vary based on the size and complexity.',
                'category': 'vastu',
                'status': 'active',
                'sort_order': 2,
            },
            {
                'question': 'Can Vastu be applied to existing buildings?',
                'answer': 'Yes! There are many simple remedies that can correct Vastu defects without demolition or major structural changes. These include using crystals, mirrors, colors, plants, and other correction techniques.',
                'category': 'vastu',
                'status': 'active',
                'sort_order': 3,
            },
            {
                'question': 'What are the benefits of following Vastu principles?',
                'answer': 'Vastu-compliant spaces promote health, prosperity, peace, and happiness. Benefits include better health, improved relationships, enhanced career growth, financial stability, and overall wellbeing.',
                'category': 'vastu',
                'status': 'active',
                'sort_order': 4,
            },
            {
                'question': 'Do you provide online consultations?',
                'answer': 'Yes, we offer online consultations for clients who cannot have an in-person visit. You can share your floor plan and photos, and we provide a detailed Vastu analysis report with recommendations.',
                'category': 'vastu',
                'status': 'active',
                'sort_order': 5,
            },
            {
                'question': 'What should I look for when buying a plot?',
                'answer': 'Key considerations include: plot shape (regular is best), direction of the plot, surrounding environment, soil quality, road access, and proximity to positive features like temples, parks, or water bodies while avoiding negative influences.',
                'category': 'engineering',
                'status': 'active',
                'sort_order': 1,
            },
            {
                'question': 'How do you ensure construction quality?',
                'answer': 'We focus on: using quality materials, following proper construction techniques, regular site supervision, soil testing, structural engineering compliance, and adherence to building codes while incorporating Vastu principles.',
                'category': 'engineering',
                'status': 'active',
                'sort_order': 2,
            },
            {
                'question': 'What is the typical timeline for a residential construction project?',
                'answer': 'The timeline depends on the size and complexity of the project. A typical 2-3 story residential building takes 12-18 months for completion. This includes: foundation work (2-3 months), superstructure (3-4 months), finishing (4-6 months), and final touches (1-2 months). Weather and material availability can affect the timeline.',
                'category': 'engineering',
                'status': 'active',
                'sort_order': 3,
            },
            {
                'question': 'Do you provide structural engineering services?',
                'answer': 'Yes, we have a team of experienced structural engineers who ensure your building is safe, durable, and compliant with all building codes. We provide detailed structural drawings, calculations, and on-site supervision for all types of residential and commercial projects.',
                'category': 'engineering',
                'status': 'active',
                'sort_order': 4,
            },
            {
                'question': 'What construction materials do you recommend for Nepal\'s climate?',
                'answer': 'For Nepal\'s diverse climate, we recommend: reinforced concrete frames for earthquake safety, high-quality bricks with proper mortar ratio, weather-proof exterior paints, proper insulation for temperature control, and moisture-resistant materials in areas with high rainfall. We also suggest using locally-sourced materials that are sustainable and cost-effective.',
                'category': 'engineering',
                'status': 'active',
                'sort_order': 5,
            },
        ]

        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'  Created FAQ: {faq.question[:50]}...')

        # Create Testimonials
        self.stdout.write('Creating testimonials...')
        testimonials_data = [
            {
                'name': 'Ram Bahadur',
                'company': 'Kathmandu',
                'position': 'Homeowner',
                'testimonial': 'The Vastu consultation transformed our home. We noticed positive changes within weeks. Highly recommended!',
                'rating': 5.0,
                'status': 'published',
                'featured': True,
                'order': 1,
            },
            {
                'name': 'Sita Sharma',
                'company': 'Pokhara',
                'position': 'Business Owner',
                'testimonial': 'After implementing Vastu remedies in my shop, sales increased significantly. The experts really know their stuff.',
                'rating': 5.0,
                'status': 'published',
                'featured': True,
                'order': 2,
            },
            {
                'name': 'Krishna Prasad',
                'company': 'Lalitpur',
                'position': 'Architect',
                'testimonial': 'As an architect, I was skeptical. But the Vastu integration was seamless and the results speak for themselves.',
                'rating': 4.5,
                'status': 'published',
                'featured': True,
                'order': 3,
            },
            {
                'name': 'Maya Devi',
                'company': 'Chitwan',
                'position': 'Homeowner',
                'testimonial': 'Simple remedies made a big difference. My family feels more peaceful and harmonious at home now.',
                'rating': 5.0,
                'status': 'published',
                'featured': False,
                'order': 4,
            },
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults={**testimonial_data, 'created_by': user}
            )
            if created:
                self.stdout.write(f'  Created testimonial: {testimonial.name}')

        # Create Carousels
        self.stdout.write('Creating carousel slides...')
        carousels_data = [
            {
                'title': 'Transform Your Home with Vastu',
                'caption': 'Ancient wisdom for modern living. Create harmony and prosperity in your space.',
                'link_url': '/services/',
                'status': 'active',
                'sort_order': 1,
            },
            {
                'title': 'Professional Vastu Consultation',
                'caption': 'Expert guidance for residential and commercial properties. 20+ years of experience.',
                'link_url': '/contact/',
                'status': 'active',
                'sort_order': 2,
            },
            {
                'title': 'Vastu Products & Remedies',
                'caption': 'Authentic Vastu remedies and products for your home and office.',
                'link_url': '/products/',
                'status': 'active',
                'sort_order': 3,
            },
        ]

        for carousel_data in carousels_data:
            carousel, created = Carousel.objects.get_or_create(
                title=carousel_data['title'],
                defaults=carousel_data
            )
            if created:
                self.stdout.write(f'  Created carousel: {carousel.title}')

        # Create Galleries
        self.stdout.write('Creating galleries...')
        galleries_data = [
            {
                'name': 'Residential Projects',
                'slug': 'residential-projects',
                'description': 'Vastu-compliant homes and residential projects.',
                'status': 'active',
                'sort_order': 1,
            },
            {
                'name': 'Commercial Projects',
                'slug': 'commercial-projects',
                'description': 'Commercial complexes and offices designed with Vastu principles.',
                'status': 'active',
                'sort_order': 2,
            },
            {
                'name': 'Vastu Remedies',
                'slug': 'vastu-remedies',
                'description': 'Before and after examples of Vastu corrections.',
                'status': 'active',
                'sort_order': 3,
            },
        ]

        for gallery_data in galleries_data:
            gallery, created = Gallery.objects.get_or_create(
                slug=gallery_data['slug'],
                defaults={**gallery_data, 'created_by': user}
            )
            if created:
                self.stdout.write(f'  Created gallery: {gallery.name}')

        # Create Videos
        self.stdout.write('Creating videos...')
        videos_data = [
            {
                'title': 'Introduction to Vastu Shastra',
                'slug': 'intro-to-vastu',
                'description': 'Learn the basics of Vastu Shastra in this comprehensive introduction video.',
                'embed_code': '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
                'status': 'published',
                'sort_order': 1,
            },
            {
                'title': 'Vastu Tips for Bedrooms',
                'slug': 'vastu-tips-bedrooms',
                'description': 'Essential Vastu guidelines for designing your bedroom for better sleep and harmony.',
                'embed_code': '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
                'status': 'published',
                'sort_order': 2,
            },
        ]

        for video_data in videos_data:
            video, created = Video.objects.get_or_create(
                slug=video_data['slug'],
                defaults={**video_data, 'created_by': user}
            )
            if created:
                self.stdout.write(f'  Created video: {video.title}')

        self.stdout.write(self.style.SUCCESS('Dummy content created successfully!'))
        self.stdout.write('\nSummary:')
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Tags: {Tag.objects.count()}')
        self.stdout.write(f'  Posts: {Post.objects.count()}')
        self.stdout.write(f'  Pages: {Page.objects.count()}')
        self.stdout.write(f'  Products: {Product.objects.count()}')
        self.stdout.write(f'  FAQs: {FAQ.objects.count()}')
        self.stdout.write(f'  Testimonials: {Testimonial.objects.count()}')
        self.stdout.write(f'  Carousels: {Carousel.objects.count()}')
        self.stdout.write(f'  Galleries: {Gallery.objects.count()}')
        self.stdout.write(f'  Videos: {Video.objects.count()}')
