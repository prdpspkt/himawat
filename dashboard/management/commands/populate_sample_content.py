from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
import random

from dashboard.models import (
    Category, Tag, Post, Page, Download, Gallery, GalleryImage,
    Testimonial, Carousel, FAQ, Product, ProductImage, Video,
    Service, Training, Menu, MenuItem, CEOInfo, CompanyInfo
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample content (5 items per content type)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample content...'))

        # Get or create a default user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@himwatkhanda.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()

        # Create Categories
        self.stdout.write('Creating Categories...')
        categories_data = [
            {'name': 'Vastu Shastra', 'description': 'Principles of Vastu for home and office'},
            {'name': 'Engineering Design', 'description': 'Structural engineering and architectural design'},
            {'name': 'Construction Tips', 'description': 'Practical construction guidance'},
            {'name': 'Interior Design', 'description': 'Interior planning and decoration'},
            {'name': 'Case Studies', 'description': 'Real project examples and success stories'},
        ]
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'status': 'active'
                }
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'  [+] Created category: {cat.name}')

        # Create Tags
        self.stdout.write('\nCreating Tags...')
        tags_data = ['Vastu', 'Construction', 'Design', 'Engineering', 'Architecture']
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                slug=slugify(tag_name),
                defaults={'name': tag_name}
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'  [+] Created tag: {tag.name}')

        # Create Posts
        self.stdout.write('\nCreating Posts...')
        posts_data = [
            {
                'title': 'Introduction to Vastu Shastra Principles',
                'excerpt': 'Learn the fundamental principles of Vastu Shastra for harmonious living spaces.',
                'content': '<p>Vastu Shastra is an ancient Indian science of architecture and construction. It emphasizes the importance of direction, layout, and proportion in creating spaces that promote health, wealth, and happiness.</p><h2>Five Elements</h2><p>Vastu is based on the balance of five elements: Earth, Water, Air, Fire, and Space. Each direction is associated with specific elements and has unique characteristics.</p>',
                'status': 'published'
            },
            {
                'title': 'Modern Engineering Techniques for Home Construction',
                'excerpt': 'Explore the latest engineering methods for durable and sustainable home construction.',
                'content': '<p>Modern construction has evolved significantly with new materials and techniques. From reinforced concrete to sustainable building materials, homeowners now have more options than ever.</p><h2>Foundation Design</h2><p>A strong foundation is the key to any durable structure. Learn about different foundation types and when to use each one.</p>',
                'status': 'published'
            },
            {
                'title': 'Vastu Tips for Office Layout',
                'excerpt': 'Optimize your workspace productivity with these Vastu guidelines.',
                'content': '<p>The layout of your office can significantly impact productivity and success. According to Vastu, the placement of desks, cabins, and conference rooms matters.</p><h2>CEO Cabin Direction</h2><p>The CEO should face north or east while sitting in their cabin. This position is believed to enhance leadership and decision-making abilities.</p>',
                'status': 'published'
            },
            {
                'title': 'Sustainable Building Materials Guide',
                'excerpt': 'Discover eco-friendly materials for your next construction project.',
                'content': '<p>Sustainable building materials are becoming increasingly popular. They reduce environmental impact and often provide better insulation and durability.</p><h2>Bamboo Construction</h2><p>Bamboo is a versatile, renewable resource that is gaining popularity in modern construction. Learn about its applications and benefits.</p>',
                'status': 'published'
            },
            {
                'title': 'Common Vastu Mistakes to Avoid',
                'excerpt': 'Learn about frequent Vastu errors in home design and how to fix them.',
                'content': '<p>Many homeowners unknowingly violate Vastu principles when designing their homes. These mistakes can lead to various problems over time.</p><h2>Main Entrance Direction</h2><p>The main entrance should ideally face north or east. Avoid south-west entrances as they are considered inauspicious in Vastu Shastra.</p>',
                'status': 'published'
            },
        ]
        for i, post_data in enumerate(posts_data):
            post, created = Post.objects.get_or_create(
                slug=slugify(post_data['title']),
                defaults={
                    **post_data,
                    'author': user,
                    'featured_image': None,
                }
            )
            if created:
                post.category = random.choice(categories)
                post.save()
                post.tags.add(random.choice(tags))
                self.stdout.write(f'  [+] Created post: {post.title}')

        # Create Pages
        self.stdout.write('\nCreating Pages...')
        pages_data = [
            {
                'title': 'About Us',
                'slug': 'about-us',
                'excerpt': 'Learn about Himwatkhanda Vastu and our mission to promote traditional architectural wisdom.',
                'content': '<p>Welcome to Himwatkhanda Vastu. We are dedicated to preserving and promoting the ancient science of Vastu Shastra combined with modern engineering excellence.</p><h2>Our Mission</h2><p>To provide expert guidance on Vastu-compliant construction and design, helping people create spaces that bring prosperity and well-being.</p><h2>Our Team</h2><p>Our team consists of experienced Vastu consultants, structural engineers, and architects working together to deliver comprehensive solutions.</p>',
                'status': 'active'
            },
            {
                'title': 'Vastu Services',
                'slug': 'vastu-services',
                'excerpt': 'Comprehensive Vastu consultation services for residential and commercial properties.',
                'content': '<p>Our Vastu services cover every aspect of construction and design. From site selection to interior layout, we ensure Vastu compliance at every stage.</p><h2>Services Include:</h2><ul><li>Site Analysis and Selection</li><li>Building Layout Design</li><li>Interior Planning</li><li>Vastu Correction for Existing Structures</li><li>Consultation for Renovations</li></ul>',
                'status': 'active'
            },
            {
                'title': 'Engineering Solutions',
                'slug': 'engineering-solutions',
                'excerpt': 'Structural engineering and architectural design services for all types of projects.',
                'content': '<p>We provide complete engineering solutions tailored to your needs. Our team combines traditional wisdom with modern technology.</p><h2>Our Expertise:</h2><ul><li>Structural Design and Analysis</li><li>Architectural Planning</li><li>Project Management</li><li>Quality Supervision</li><li>Technical Consultations</li></ul>',
                'status': 'active'
            },
            {
                'title': 'Training Programs',
                'slug': 'training-programs',
                'excerpt': 'Professional training in Vastu Shastra and modern construction techniques.',
                'content': '<p>We offer comprehensive training programs for individuals and professionals interested in learning Vastu principles and modern construction methods.</p><h2>Course Offerings:</h2><ul><li>Basic Vastu Course</li><li>Advanced Vastu Certification</li><li>Construction Management</li><li>Architectural Design Workshop</li></ul>',
                'status': 'active'
            },
            {
                'title': 'Contact Us',
                'slug': 'contact-page',
                'excerpt': 'Get in touch with our expert team for consultation and services.',
                'content': '<p>We\'re here to help you create your dream space with Vastu compliance. Reach out to us for any queries or to schedule a consultation.</p><h2>Contact Information:</h2><p><strong>Email:</strong> info@himwatkhanda.com<br><strong>Phone:</strong> +91 9876543210<br><strong>Address:</strong> 123 Vastu Bhavan, New Delhi, India</p>',
                'status': 'active'
            },
        ]
        for page_data in pages_data:
            page, created = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults={**page_data}
            )
            if created:
                self.stdout.write(f'  [+] Created page: {page.title}')

        # Create Products
        self.stdout.write('\nCreating Products...')
        products_data = [
            {
                'name': 'Vastu Home Design Guide',
                'description': 'Complete guide for designing your dream home according to Vastu principles. This comprehensive guide covers everything you need to know about Vastu-compliant home design including room layouts, direction guidelines, and placement recommendations.',
                'status': 'active'
            },
            {
                'name': 'Vastu Office Layout Kit',
                'description': 'Professional office layout templates and guidelines for Vastu compliance. Create a productive workspace with our Vastu-compliant office layout templates and design principles.',
                'status': 'active'
            },
            {
                'name': 'Construction Materials Guide',
                'description': 'Essential guide to selecting the right materials for your construction project. Learn about sustainable and durable construction materials for your project with detailed specifications and supplier information.',
                'status': 'active'
            },
            {
                'name': 'Vastu Remedies Kit',
                'description': 'Effective remedies for common Vastu defects in existing structures. Fix Vastu issues in your home or office with these proven remedies and correction techniques.',
                'status': 'active'
            },
            {
                'name': 'Complete Vastu Course Bundle',
                'description': 'All-inclusive Vastu learning package with video tutorials and guides. Master Vastu Shastra with our complete course bundle including video lessons, detailed guides, and certification.',
                'status': 'active'
            },
        ]
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=slugify(product_data['name']),
                defaults={**product_data}
            )
            if created:
                self.stdout.write(f'  [+] Created product: {product.name}')

        # Create Services
        self.stdout.write('\nCreating Services...')
        services_data = [
            {
                'name': 'Vastu Consultation',
                'slug': 'vastu-consultation',
                'excerpt': 'Expert Vastu guidance for your property',
                'description': '<p>Our Vastu experts analyze your property and provide detailed recommendations for optimal layout and design.</p><h2>What We Offer:</h2><ul><li>Site Visit and Analysis</li><li>Detailed Report with Recommendations</li><li>3D Layout Suggestions</li><li>Remedies for Existing Structures</li></ul>',
                'status': 'active'
            },
            {
                'name': 'Structural Engineering',
                'slug': 'structural-engineering',
                'excerpt': 'Complete structural design and analysis',
                'description': '<p>We provide comprehensive structural engineering services ensuring safety and compliance with all building codes.</p><h2>Services:</h2><ul><li>Structural Design</li><li>Foundation Analysis</li><li>Seismic Design</li><li>Construction Supervision</li></ul>',
                'status': 'active'
            },
            {
                'name': 'Architectural Design',
                'slug': 'architectural-design',
                'excerpt': 'Creative and functional architectural solutions',
                'description': '<p>Our architects combine aesthetics with functionality, creating spaces that are both beautiful and practical.</p><h2>Deliverables:</h2><ul><li>3D Visualization</li><li>Complete Working Drawings</li><li>Interior Layout Plans</li><li>Material Specifications</li></ul>',
                'status': 'active'
            },
            {
                'name': 'Construction Supervision',
                'slug': 'construction-supervision',
                'excerpt': 'Quality assurance during construction',
                'description': '<p>Ensure quality and compliance with regular site supervision and quality checks.</p><h2>Our Role:</h2><ul><li>Regular Site Visits</li><li>Quality Control</li><li>Progress Reporting</li><li>Budget Management</li></ul>',
                'status': 'active'
            },
            {
                'name': 'Vastu Training',
                'slug': 'vastu-training',
                'excerpt': 'Learn Vastu Shastra from industry experts',
                'description': '<p>Join our comprehensive training programs to become a certified Vastu consultant.</p><h2>Programs Available:</h2><ul><li>Basic Certificate Course (3 months)</li><li>Advanced Diploma (6 months)</li><li>Professional Certification (1 year)</li></ul>',
                'status': 'active'
            },
        ]
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults={**service_data}
            )
            if created:
                self.stdout.write(f'  [+] Created service: {service.name}')

        # Create Trainings
        self.stdout.write('\nCreating Trainings...')
        trainings_data = [
            {
                'name': 'Basic Vastu Certificate Course',
                'short_description': 'Learn fundamentals of Vastu Shastra',
                'description': '<p>This comprehensive 3-month course covers all fundamental principles of Vastu Shastra.</p><h2>Course Content:</h2><ul><li>Introduction to Vastu</li><li>Five Elements Theory</li><li>Direction Science</li><li>Site Selection</li><li>Basic Layout Principles</li></ul>',
                'duration': '3 months',
                'price': 25000,
                'status': 'active'
            },
            {
                'name': 'Advanced Vastu Diploma',
                'short_description': 'Master advanced Vastu techniques',
                'description': '<p>Deepen your Vastu knowledge with this advanced 6-month diploma program.</p><h2>Advanced Topics:</h2><ul><li>Commercial Vastu</li><li>Industrial Layouts</li><li>Vastu Remedies</li><li>Astro-Vastu Integration</li><li>Case Studies</li></ul>',
                'duration': '6 months',
                'price': 50000,
                'status': 'active'
            },
            {
                'name': 'Construction Management Course',
                'short_description': 'Learn modern construction management',
                'description': '<p>Master the art of managing construction projects efficiently and effectively.</p><h2>Modules:</h2><ul><li>Project Planning</li><li>Resource Management</li><li>Quality Control</li><li>Cost Management</li><li>Safety Regulations</li></ul>',
                'duration': '4 months',
                'price': 35000,
                'status': 'active'
            },
            {
                'name': 'Architectural Design Workshop',
                'short_description': 'Hands-on architectural design training',
                'description': '<p>Practical workshop on designing buildings with modern tools and techniques.</p><h2>Workshop Highlights:</h2><ul><li>AutoCAD Training</li><li>3D Modeling</li><li>Design Principles</li><li>Building Codes</li><li>Portfolio Development</li></ul>',
                'duration': '2 months',
                'price': 20000,
                'status': 'active'
            },
            {
                'name': 'Professional Vastu Consultant Certification',
                'short_description': 'Become a certified Vastu consultant',
                'description': '<p>Complete certification program to start your career as a professional Vastu consultant.</p><h2>Certification Benefits:</h2><ul><li>Industry Recognition</li><li>Practice Support</li><li>Marketing Assistance</li><li>Continuing Education</li><li>Client Referrals</li></ul>',
                'duration': '12 months',
                'price': 100000,
                'status': 'active'
            },
        ]
        for training_data in trainings_data:
            training, created = Training.objects.get_or_create(
                slug=slugify(training_data['name']),
                defaults={**training_data}
            )
            if created:
                self.stdout.write(f'  [+] Created training: {training.name}')

        # Create Testimonials
        self.stdout.write('\nCreating Testimonials...')
        testimonials_data = [
            {
                'name': 'Rajesh Kumar',
                'position': 'Businessman',
                'company': 'Kumar Enterprises',
                'testimonial': 'The Vastu consultation transformed my office layout. Productivity increased by 40% within 3 months!',
                'rating': 5,
                'status': 'published'
            },
            {
                'name': 'Priya Sharma',
                'position': 'Homeowner',
                'company': 'Private',
                'testimonial': 'Excellent guidance on our new home construction. The team was professional and knowledgeable.',
                'rating': 5,
                'status': 'published'
            },
            {
                'name': 'Dr. Amit Verma',
                'position': 'Architect',
                'company': 'Design Studio',
                'testimonial': 'Their structural engineering services are top-notch. Highly recommend for any construction project.',
                'rating': 5,
                'status': 'published'
            },
            {
                'name': 'Sunita Gupta',
                'position': 'Interior Designer',
                'company': 'Creative Spaces',
                'testimonial': 'The Vastu training course was comprehensive and practical. Now I incorporate Vastu in all my designs.',
                'rating': 4,
                'status': 'published'
            },
            {
                'name': 'Vikram Singh',
                'position': 'Builder',
                'company': 'Singh Constructions',
                'testimonial': 'Their construction supervision ensured quality and timely completion. Very professional team.',
                'rating': 5,
                'status': 'published'
            },
        ]
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults={**testimonial_data}
            )
            if created:
                self.stdout.write(f'  [+] Created testimonial: {testimonial.name}')

        # Create Galleries
        self.stdout.write('\nCreating Galleries...')
        galleries_data = [
            {
                'name': 'Residential Projects',
                'description': 'Beautiful homes designed with Vastu principles'
            },
            {
                'name': 'Commercial Buildings',
                'description': 'Office and business complexes with optimal layouts'
            },
            {
                'name': 'Temple Architecture',
                'description': 'Traditional temple designs and constructions'
            },
            {
                'name': 'Interior Designs',
                'description': 'Stunning interior spaces following Vastu guidelines'
            },
            {
                'name': 'Before & After',
                'description': 'Vastu corrections and transformations'
            },
        ]
        for gallery_data in galleries_data:
            gallery, created = Gallery.objects.get_or_create(
                slug=slugify(gallery_data['name']),
                defaults={**gallery_data, 'status': 'active'}
            )
            if created:
                self.stdout.write(f'  [+] Created gallery: {gallery.name}')

        # Create Videos
        self.stdout.write('\nCreating Videos...')
        videos_data = [
            {
                'title': 'Vastu Basics for Beginners',
                'description': 'Learn the fundamental principles of Vastu Shastra in this introductory video.',
                'embed_code': '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
                'status': 'published'
            },
            {
                'title': 'Main Door Vastu Guidelines',
                'description': 'Essential tips for main door placement and design according to Vastu.',
                'embed_code': '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
                'status': 'published'
            },
            {
                'title': 'Kitchen Vastu Tips',
                'description': 'Design your kitchen following Vastu principles for health and prosperity.',
                'embed_code': '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
                'status': 'published'
            },
            {
                'title': 'Bedroom Direction Guide',
                'description': 'Optimal bedroom placement for better sleep and health.',
                'embed_code': '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
                'status': 'published'
            },
            {
                'title': 'Vastu for Office Setup',
                'description': 'Create a productive workspace with these Vastu guidelines.',
                'embed_code': '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
                'status': 'published'
            },
        ]
        for video_data in videos_data:
            video, created = Video.objects.get_or_create(
                slug=slugify(video_data['title']),
                defaults={**video_data}
            )
            if created:
                self.stdout.write(f'  [+] Created video: {video.title}')

        # Create Downloads
        self.stdout.write('\nCreating Downloads...')
        downloads_data = [
            {
                'title': 'Vastu Home Checklist',
                'description': 'Comprehensive checklist for Vastu-compliant home construction',
                'file_size': 2621440,
                'download_count': 0,
                'status': 'published'
            },
            {
                'title': 'Construction Material Guide PDF',
                'description': 'Detailed guide to selecting construction materials',
                'file_size': 6081740,
                'download_count': 0,
                'status': 'published'
            },
            {
                'title': 'Vastu Floor Plans Collection',
                'description': 'Ready-to-use Vastu-compliant floor plan templates',
                'file_size': 12897480,
                'download_count': 0,
                'status': 'published'
            },
            {
                'title': 'Vastu Remedies eBook',
                'description': 'Complete guide to Vastu remedies for common defects',
                'file_size': 8493460,
                'download_count': 0,
                'status': 'published'
            },
            {
                'title': 'Project Planning Templates',
                'description': 'Professional templates for construction project planning',
                'file_size': 4404020,
                'download_count': 0,
                'status': 'published'
            },
        ]
        for download_data in downloads_data:
            download, created = Download.objects.get_or_create(
                slug=slugify(download_data['title']),
                defaults={**download_data}
            )
            if created:
                self.stdout.write(f'  [+] Created download: {download.title}')

        # Create FAQs
        self.stdout.write('\nCreating FAQs...')
        faqs_data = [
            {
                'question': 'What is Vastu Shastra?',
                'answer': 'Vastu Shastra is an ancient Indian science of architecture that guides the design and construction of buildings to ensure harmony with natural forces.',
                'sort_order': 1,
                'status': 'active'
            },
            {
                'question': 'How long does a Vastu consultation take?',
                'answer': 'A typical Vastu consultation takes 2-4 hours for site visit and analysis, followed by a detailed report within 3-5 working days.',
                'sort_order': 2,
                'status': 'active'
            },
            {
                'question': 'Can Vastu be applied to existing buildings?',
                'answer': 'Yes, Vastu remedies can be applied to existing structures. We provide practical solutions to correct Vastu defects without major demolition.',
                'sort_order': 3,
                'status': 'active'
            },
            {
                'question': 'What are your consultation fees?',
                'answer': 'Our consultation fees start from ₹5,000 for residential properties and vary based on the scope and size of the project. Contact us for a detailed quote.',
                'sort_order': 4,
                'status': 'active'
            },
            {
                'question': 'Do you provide online consultations?',
                'answer': 'Yes, we offer online Vastu consultations via video call. You can share your floor plans and photos for detailed analysis and recommendations.',
                'sort_order': 5,
                'status': 'active'
            },
        ]
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={**faq_data}
            )
            if created:
                self.stdout.write(f'  [+] Created FAQ: {faq.question[:30]}...')

        # Note: Carousels require image files, so they should be created through the admin panel
        # Skipping carousel creation in this command
        self.stdout.write('\nSkipping Carousels (create through admin panel with images)...')

        # Create Menu
        self.stdout.write('\nCreating Menu...')
        menu, created = Menu.objects.get_or_create(
            name='Main Menu',
            slug='main-menu',
            defaults={
                'location': 'main',
                'description': 'Primary website navigation menu'
            }
        )
        if created:
            self.stdout.write(f'  [+] Created menu: {menu.name}')

            # Create Menu Items
            self.stdout.write('\nCreating Menu Items...')
            menu_items_data = [
                {'title': 'Home', 'url': '/', 'order': 1, 'type': 'custom_link'},
                {'title': 'About Us', 'url': '/about-us/', 'order': 2, 'type': 'custom_link'},
                {'title': 'Services', 'url': '/vastu-services/', 'order': 3, 'type': 'custom_link'},
                {'title': 'Blog', 'url': '/blog/', 'order': 4, 'type': 'custom_link'},
                {'title': 'Videos', 'url': '/videos/', 'order': 5, 'type': 'custom_link'},
                {'title': 'Contact', 'url': '/contact-page/', 'order': 6, 'type': 'custom_link'},
            ]
            for item_data in menu_items_data:
                menu_item, created = MenuItem.objects.get_or_create(
                    menu=menu,
                    title=item_data['title'],
                    defaults={**item_data}
                )
                if created:
                    self.stdout.write(f'    [+] Created menu item: {menu_item.title}')

        # Create CEO Info
        self.stdout.write('\nCreating CEO Info...')
        ceo_info, created = CEOInfo.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'Dr. Rajesh Kumar Sharma',
                'title': 'Founder & Vastu Consultant',
                'bio': 'Dr. Rajesh Kumar Sharma is a renowned Vastu consultant with over 20 years of experience in traditional Indian architecture and modern engineering. He has helped thousands of clients create Vastu-compliant spaces that bring prosperity and well-being.',
                'message': 'Welcome to Himwatkhanda Vastu. We are dedicated to preserving and promoting the ancient science of Vastu Shastra combined with modern engineering excellence. Our mission is to help you create spaces that harmonize with nature and bring positive energy into your life.',
                'email': 'ceo@himwatkhanda.com',
                'phone': '+91 9876543210',
                'social_linkedin': 'https://linkedin.com/in/ceo-himwatkhanda',
                'social_twitter': 'https://twitter.com/ceo_himwatkhanda',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'  [+] Created CEO info: {ceo_info.name}')
        else:
            self.stdout.write(f'  [*] CEO info already exists: {ceo_info.name}')

        # Create Company Info
        self.stdout.write('\nCreating Company Info...')
        company_info, created = CompanyInfo.objects.get_or_create(
            pk=1,
            defaults={
                'company_name': 'Himwatkhanda Vastu Pvt. Ltd.',
                'description': 'Leading Vastu consultation and engineering design services provider. We combine ancient Vastu wisdom with modern engineering principles to create harmonious living and working spaces.',
                'email': 'info@himwatkhanda.com',
                'phone': '+91 9876543210',
                'address': '123 Vastu Bhavan, Sector 15, New Delhi - 110001',
                'city': 'New Delhi',
                'state': 'Delhi',
                'country': 'India',
                'pincode': '110001',
                'gst_number': '07AAAAA0000A1Z5',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'  [+] Created company info: {company_info.company_name}')
        else:
            self.stdout.write(f'  [*] Company info already exists: {company_info.company_name}')

        self.stdout.write(self.style.SUCCESS('\n[+] Successfully populated sample content!'))
        self.stdout.write('\nSummary:')
        self.stdout.write(f'  - Categories: {Category.objects.count()}')
        self.stdout.write(f'  - Tags: {Tag.objects.count()}')
        self.stdout.write(f'  - Posts: {Post.objects.count()}')
        self.stdout.write(f'  - Pages: {Page.objects.count()}')
        self.stdout.write(f'  - Products: {Product.objects.count()}')
        self.stdout.write(f'  - Services: {Service.objects.count()}')
        self.stdout.write(f'  - Trainings: {Training.objects.count()}')
        self.stdout.write(f'  - Testimonials: {Testimonial.objects.count()}')
        self.stdout.write(f'  - Galleries: {Gallery.objects.count()}')
        self.stdout.write(f'  - Videos: {Video.objects.count()}')
        self.stdout.write(f'  - Downloads: {Download.objects.count()}')
        self.stdout.write(f'  - FAQs: {FAQ.objects.count()}')
        self.stdout.write(f'  - Carousels: {Carousel.objects.count()}')
        self.stdout.write(f'  - Menus: {Menu.objects.count()}')
        self.stdout.write(f'  - CEO Info: {CEOInfo.objects.count()}')
        self.stdout.write(f'  - Company Info: {CompanyInfo.objects.count()}')
