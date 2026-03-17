from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dashboard.models import Page, Menu, MenuItem

User = get_user_model()


class Command(BaseCommand):
    help = 'Create pages and set up top navigation menu structure'

    def handle(self, *args, **options):
        self.stdout.write('Setting up pages and navigation...')

        # Get or create a user
        user = User.objects.filter(is_staff=True).first()
        if not user:
            user = User.objects.first()

        # Define page structure
        pages_structure = {
            'Vastu Services': {
                'slug': 'vastu-services',
                'content': '''<h2>Vastu Services</h2>
<p>We offer comprehensive Vastu Shastra consultation services for residential, commercial, and industrial properties. Our expert Vastu consultants combine ancient wisdom with modern requirements to create harmonious living and working spaces.</p>

<h3>Our Vastu Services Include:</h3>
<ul>
<li><strong>Residential Vastu:</strong> Complete Vastu analysis for homes, apartments, villas, and townhouses</li>
<li><strong>Commercial Vastu:</strong> Vastu consultation for offices, shops, showrooms, and business complexes</li>
<li><strong>Industrial Vastu:</strong> Factory and industry-specific Vastu planning for optimal productivity</li>
<li><strong>Vastu Corrections:</strong> Remedies for existing properties without demolition</li>
<li><strong>Plot Selection:</strong> Guidance for selecting Vastu-compliant plots</li>
<li><strong>Interior Vastu:</strong> Room-wise Vastu arrangements and color therapy</li>
</ul>

<h3>Why Choose Our Vastu Services?</h3>
<ul>
<li>20+ years of experience in Vastu consultation</li>
<li>Certified Vastu consultants with deep knowledge of ancient texts</li>
<li>Practical and scientific approach to Vastu</li>
<li>Customized solutions for each client</li>
<li>Post-consultation support and guidance</li>
</ul>

<p>Contact us today for a detailed Vastu analysis of your property!</p>
''',
                'meta_title': 'Vastu Services - Professional Vastu Consultation',
                'meta_description': 'Expert Vastu Shastra consultation services for residential, commercial, and industrial properties. 20+ years experience.',
            },
            'Engineering Design': {
                'slug': 'engineering-design',
                'content': '''<h2>Engineering Design Services</h2>
<p>We provide complete engineering design services that blend modern engineering principles with Vastu Shastra. Our team of experienced engineers ensures your building is safe, functional, and harmoniously designed.</p>

<h3>Our Engineering Services:</h3>
<ul>
<li><strong>Structural Engineering:</strong> Detailed structural design and calculations for all types of buildings</li>
<li><strong>Architectural Design:</strong> Creative and functional architectural solutions</li>
<li><strong>Electrical Engineering:</strong> Complete electrical layout and design</li>
<li><strong>Plumbing Design:</strong> Efficient water supply and drainage systems</li>
<li><strong>HVAC Design:</strong> Climate control systems for comfort</li>
<li><strong>Fire Safety:</strong> Comprehensive fire protection systems</li>
<li><strong>Lift/Elevator Design:</strong> Vertical transportation solutions</li>
</ul>

<h3>Design Process:</h3>
<ol>
<li><strong>Site Analysis:</strong> Detailed survey and soil testing</li>
<li><strong>Concept Design:</strong> Initial layouts and 3D visualization</li>
<li><strong>Detailed Design:</strong> Complete working drawings</li>
<li><strong>Structural Design:</strong> Foundation and superstructure design</li>
<li><strong>MEP Design:</strong> Mechanical, electrical, and plumbing systems</li>
<li><strong>Approvals:</strong> Assistance with municipal approvals</li>
</ol>

<h4>Get in Touch</h4>
<p>Contact us for professional engineering design services that meet all building codes while incorporating Vastu principles.</p>
''',
                'meta_title': 'Engineering Design Services - Structural & Architectural',
                'meta_description': 'Complete engineering design services including structural, architectural, electrical, and plumbing design with Vastu compliance.',
            },
            'Vaastu Design': {
                'slug': 'vaastu-design',
                'content': '''<h2>Vaastu Design Consultation</h2>
<p>Specialized Vastu design services for creating spaces that harmonize with nature's elements and promote positive energy flow.</p>

<h3>What We Offer:</h3>
<ul>
<li>Complete Vastu-compliant floor plans</li>
<li>Room placement according to Vastu principles</li>
<li>Door and window positioning</li>
<li>Color recommendations based on Vastu</li>
<li>Placement of utilities (kitchen, bathrooms, stairs)</li>
<li>Foundation and ground-breaking Muhurat</li>
</ul>

<p>Our Vastu designs ensure that your space promotes health, prosperity, and happiness.</p>
''',
                'meta_title': 'Vaastu Design Consultation - Vastu-Compliant Floor Plans',
                'meta_description': 'Professional Vastu design consultation with complete floor plans and room placement according to Vastu Shastra principles.',
            },
            'Residential Design': {
                'slug': 'residential-design',
                'content': '''<h2>Residential Design Services</h2>
<p>Comprehensive residential design services combining Vastu principles with modern architectural design for your dream home.</p>

<h3>Residential Services Include:</h3>
<ul>
<li><strong>Custom Home Design:</strong> Unique designs tailored to your lifestyle and budget</li>
<li><strong>Vastu-Compliant Homes:</strong> Homes designed according to Vastu Shastra</li>
<li><strong>Apartment Design:</strong> Space-efficient apartment layouts</li>
<li><strong>Villa Design:</strong> Luxury villa designs with modern amenities</li>
<li><strong>Interior Design:</strong> Beautiful and functional interior spaces</li>
<li><strong>Landscape Design:</strong> Outdoor spaces that connect with nature</li>
</ul>

<h3>Design Features:</h3>
<ul>
<li>Earthquake-resistant structures</li>
<li>Energy-efficient designs</li>
<li>Natural ventilation and lighting</li>
<li>Modern amenities with traditional wisdom</li>
<li>Cost-effective construction methods</li>
</ul>

<p>Let us design your dream home that balances comfort, aesthetics, and Vastu principles.</p>
''',
                'meta_title': 'Residential Design Services - Custom Home Design',
                'meta_description': 'Custom residential design services with Vastu compliance. Home designs, apartments, villas with modern amenities.',
            },
            'Industrial/Commercial Design': {
                'slug': 'industrial-commercial-design',
                'content': '''<h2>Industrial & Commercial Design</h2>
<p>Specialized design services for industrial and commercial projects that optimize functionality while following Vastu principles.</p>

<h3>Commercial Design:</h3>
<ul>
<li>Office buildings and corporate parks</li>
<li>Shopping malls and retail spaces</li>
<li>Hotels and restaurants</li>
<li>Hospitals and clinics</li>
<li>Educational institutions</li>
</ul>

<h3>Industrial Design:</h3>
<ul>
<li>Factory buildings and warehouses</li>
<li>Industrial complexes</li>
<li>Manufacturing facilities</li>
<li>Processing plants</li>
</ul>

<h3>Key Features:</h3>
<ul>
<li>Optimal space utilization</li>
<li>Efficient workflow design</li>
<li>Employee productivity focus</li>
<li>Vastu for business prosperity</li>
<li>Sustainable and eco-friendly designs</li>
</ul>

<p>Enhance your business success with Vastu-compliant commercial and industrial designs.</p>
''',
                'meta_title': 'Industrial & Commercial Design Services',
                'meta_description': 'Industrial and commercial design services with Vastu compliance. Offices, malls, hotels, factories, warehouses.',
            },
            'Infrastructure Development': {
                'slug': 'infrastructure-development',
                'content': '''<h2>Infrastructure Development</h2>
<p>Comprehensive infrastructure development services for large-scale projects and township planning.</p>

<h3>Our Services:</h3>
<ul>
<li><strong>Township Planning:</strong> Complete township design with all amenities</li>
<li><strong>Road Planning:</strong> Internal and external road networks</li>
<li><strong>Water Supply:</strong> Complete water distribution systems</li>
<li><strong>Drainage Systems:</strong> Storm water and sewage drainage</li>
<li><strong>Electrical Infrastructure:</strong> Power distribution and street lighting</li>
<li><strong>Landscape Planning:</strong> Parks, gardens, and green spaces</li>
<li><strong>Community Facilities:</strong> Schools, hospitals, community centers</li>
</ul>

<h3>Infrastructure Features:</h3>
<ul>
<li>Sustainable development practices</li>
<li>Environment-friendly designs</li>
<li>Vastu-compliant layouts</li>
<li>Modern urban planning principles</li>
<li>Cost-effective solutions</li>
</ul>

<p>From concept to completion, we handle all aspects of infrastructure development.</p>
''',
                'meta_title': 'Infrastructure Development Services',
                'meta_description': 'Complete infrastructure development services including township planning, roads, water supply, drainage, and electrical systems.',
            },
            'Courses': {
                'slug': 'courses',
                'content': '''<h2>Professional Training Courses</h2>
<p>We offer comprehensive training programs in Vastu Shastra, Engineering, and Construction. Learn from experts with decades of experience.</p>

<h3>Why Choose Our Courses?</h3>
<ul>
<li>Learn from certified experts with 20+ years experience</li>
<li>Practical, hands-on training approach</li>
<li>Industry-recognized certifications</li>
<li>Flexible learning schedules</li>
<li>Online and in-person options available</li>
</ul>

<p>Explore our course offerings below and start your learning journey today.</p>
''',
                'meta_title': 'Training Courses - Vastu, Engineering & Construction',
                'meta_description': 'Professional training courses in Vastu Shastra, Engineering, and Construction. Learn from certified experts.',
            },
            'Vaastu Training': {
                'slug': 'vaastu-training',
                'content': '''<h2>Vaastu Training Programs</h2>
<p>Comprehensive Vastu Shastra training for all levels - from beginners to advanced practitioners.</p>

<p>Our Vastu training programs are designed to provide deep knowledge of this ancient science while making it practical for modern application.</p>

<h3>Program Levels:</h3>
<ul>
<li>Orientation programs for beginners</li>
<li>Advanced training for practitioners</li>
<li>Specialized courses in specific areas</li>
<li>Certification programs</li>
</ul>

<p>Choose the program that suits your needs and begin your journey into Vastu Shastra.</p>
''',
                'meta_title': 'Vaastu Training Programs - Learn Vastu Shastra',
                'meta_description': 'Comprehensive Vastu Shastra training programs for all levels. Beginner to advanced courses available.',
            },
            'Orientation Program for Owners': {
                'slug': 'orientation-program-owners',
                'content': '''<h2>Orientation Program for Property Owners</h2>
<p>A foundational course designed for property owners who want to understand Vastu principles for their properties.</p>

<h3>Course Contents:</h3>
<ul>
<li>Introduction to Vastu Shastra</li>
<li>Five elements and their significance</li>
<li>Eight directions and their effects</li>
<li>Basic Vastu principles for homes</li>
<li>Common Vastu defects and remedies</li>
<li>Simple remedies without demolition</li>
<li>Tips for existing properties</li>
</ul>

<h3>Duration:</h3>
<p>2 days (4 hours per day)</p>

<h3>Who Should Attend:</h3>
<ul>
<li>Homeowners</li>
<li>Prospective property buyers</li>
<li>Real estate investors</li>
<li>Anyone interested in Vastu basics</li>
</ul>

<h4>Fee: NPR 5,000</h4>
<p>Includes course materials and lunch.</p>
''',
                'meta_title': 'Orientation Program for Property Owners',
                'meta_description': '2-day foundational Vastu course for property owners. Learn basics, principles, and simple remedies.',
            },
            'Advance Vastu Training': {
                'slug': 'advance-vastu-training',
                'content': '''<h2>Advanced Vastu Training</h2>
<p>An intensive program for those who want to become professional Vastu consultants or deepen their Vastu knowledge.</p>

<h3>Course Contents:</h3>
<ul>
<li>Advanced Vastu principles</li>
<li>Vastu for multi-story buildings</li>
<li>Commercial and industrial Vastu</li>
<li>Vastu for town planning</li>
<li>Case studies and practical applications</li>
<li>Vastu calculations and measurements</li>
<li>Site visit and analysis techniques</li>
<li>Remedies and corrections</li>
<li>Client consultation skills</li>
</ul>

<h3>Duration:</h3>
<p>10 days (5 hours per day)</p>

<h3>Prerequisites:</h3>
<ul>
<li>Basic understanding of Vastu</li>
<li>Background in architecture/engineering (preferred)</li>
</ul>

<h4>Fee: NPR 25,000</h4>
<p>Includes comprehensive study materials, site visits, and certification.</p>
''',
                'meta_title': 'Advanced Vastu Training - Professional Consultant Course',
                'meta_description': 'Intensive 10-day advanced Vastu training for professional consultants. Certification program.',
            },
            'Yantra Designing': {
                'slug': 'yantra-designing',
                'content': '''<h2>Yantra Designing Course</h2>
<p>Learn the sacred art of designing Vastu Yantras for energy correction and enhancement.</p>

<h3>Course Contents:</h3>
<ul>
<li>Introduction to Yantras</li>
<li>Geometrical principles</li>
<li>Sacred geometry in Vastu</li>
<li>Designing Vastu Purush Yantra</li>
<li>Planetary Yantras</li>
<li>Numerical Yantras</li>
<li>Installation procedures</li>
<li>Activation rituals</li>
<li>Custom Yantra design</li>
</ul>

<h3>Duration:</h3>
<p>5 days (4 hours per day)</p>

<h3>What You'll Learn:</h3>
<ul>
<li>Design authentic Vastu Yantras</li>
<li>Calculate Yantra dimensions</li>
<li>Understand Yantra energy patterns</li>
<li>Create customized solutions</li>
</ul>

<h4>Fee: NPR 15,000</h4>
<p>Includes drawing materials and certification.</p>
''',
                'meta_title': 'Yantra Designing Course - Sacred Vastu Geometry',
                'meta_description': 'Learn to design Vastu Yantras for energy correction. 5-day intensive course with materials.',
            },
            'Vastu CAD': {
                'slug': 'vastu-cad',
                'content': '''<h2>Vastu CAD Course</h2>
<p>Learn to create Vastu-compliant designs using CAD software. Combine modern technology with ancient wisdom.</p>

<h3>Course Contents:</h3>
<ul>
<li>CAD basics for Vastu design</li>
<li>Vastu grid systems in CAD</li>
<li>Directional calculations</li>
<li>Room placement templates</li>
<li>Vastu floor plan creation</li>
<li>3D visualization</li>
<li>Plot analysis tools</li>
<li>Automated Vastu checks</li>
<li>Professional drawing standards</li>
</ul>

<h3>Duration:</h3>
<p>7 days (5 hours per day)</p>

<h3>Prerequisites:</h3>
<ul>
<li>Basic computer skills</li>
<li>Understanding of Vastu principles</li>
<li>AutoCAD knowledge (helpful but not required)</li>
</ul>

<h4>Fee: NPR 20,000</h4>
<p>Includes software training and templates.</p>
''',
                'meta_title': 'Vastu CAD Course - Computer-Aided Design',
                'meta_description': 'Learn Vastu-compliant CAD design. 7-day course with software training and templates.',
            },
            'Vedic Mantra (Diksha)': {
                'slug': 'vedic-mantra-diksha',
                'content': '''<h2>Vedic Mantra & Diksha Program</h2>
<p>Sacred Vedic mantra training for spiritual growth and Vastu space purification.</p>

<h3>Course Contents:</h3>
<ul>
<li>Introduction to Vedic mantras</li>
<li>Mantra for space purification</li>
<li>Vastu Puja procedures</li>
<li>Bhoomi Pujan (ground-breaking) rituals</li>
<li>Navagraha mantras</li>
<li>Vastu Purush mantra</li>
<li>Diksha (initiation) ceremony</li>
<li>Daily practices for harmony</li>
<li>Mantra for prosperity</li>
</ul>

<h3>Duration:</h3>
<p>3 days (3 hours per day)</p>

<h3>Includes:</h3>
<ul>
<li>Sacred mantra booklet</li>
<li>Diksha ceremony</li>
<li>Puja materials</li>
<li>Ongoing support</li>
</ul>

<h4>Fee: NPR 10,000</h4>
<p>Includes all materials and ceremony.</p>
''',
                'meta_title': 'Vedic Mantra & Diksha Program',
                'meta_description': 'Sacred Vedic mantra training for space purification. 3-day program with diksha ceremony.',
            },
            'Engineering Training': {
                'slug': 'engineering-training',
                'content': '''<h2>Engineering Training Programs</h2>
<p>Practical engineering training for construction professionals and aspiring engineers.</p>

<h3>Programs Offered:</h3>
<ul>
<li><strong>Structural Engineering:</strong> Design and analysis of building structures</li>
<li><strong>Construction Management:</strong> Project planning and execution</li>
<li><strong>Site Supervision:</strong> On-site quality control and management</li>
<li><strong>Estimation & Costing:</strong> Project budgeting and cost control</li>
<li><strong>Building Codes:</strong> NBC and municipal regulations</li>
</ul>

<h3>Training Methodology:</h3>
<ul>
<li>Theory + Practical approach</li>
<li>Site visits and live projects</li>
<li>Case studies from real projects</li>
<li>Hands-on software training</li>
<li>Industry expert interaction</li>
</ul>

<h4>Contact us for detailed curriculum and schedules.</h4>
''',
                'meta_title': 'Engineering Training Programs',
                'meta_description': 'Practical engineering training in structural design, construction management, and site supervision.',
            },
            'Mason Training': {
                'slug': 'mason-training',
                'content': '''<h2>Mason Training Program</h2>
<p>Skill development program for masons and construction workers focusing on quality construction techniques.</p>

<h3>Course Contents:</h3>
<ul>
<li>Basic construction techniques</li>
<li>Brick masonry and bonding</li>
<li>Concrete mixing and pouring</li>
<li>Plastering techniques</li>
<li>Flooring work</li>
<li>Waterproofing methods</li>
<li>Reading construction drawings</li>
<li>Safety practices</li>
<li>Quality control</li>
</ul>

<h3>Duration:</h3>
<p>15 days (6 hours per day)</p>

<h3>Who Should Attend:</h3>
<ul>
<li>Aspiring masons</li>
<li>Construction workers</li>
<li>Site supervisors</li>
<li>Contractors</li>
</ul>

<h3>Benefits:</h3>
<ul>
<li>Practical hands-on training</li>
li>Tool kit provided</li>
<li>Certificate of completion</li>
<li>Job placement assistance</li>
</ul>

<h4>Fee: NPR 8,000</h4>
<p>Includes tools, materials, and certification.</p>
''',
                'meta_title': 'Mason Training Program - Skill Development',
                'meta_description': 'Practical mason training program. 15-day skill development course with certification.',
            },
            'Videos': {
                'slug': 'videos',
                'content': '''<h2>Video Gallery</h2>
<p>Watch our collection of videos on Vastu Shastra, engineering design, construction techniques, and success stories.</p>

<h3>Video Categories:</h3>
<ul>
<li><strong>Vastu Tutorials:</strong> Learn Vastu principles through video lessons</li>
<li><strong>Project Tours:</strong> Virtual tours of our completed projects</li>
<li><strong>Expert Talks:</strong> Insights from our senior consultants</li>
<li><strong>Client Testimonials:</strong> Hear from our satisfied clients</li>
<li><strong>Construction Tips:</strong> Practical construction advice</li>
<li><strong>Course Previews:</strong> Sneak peeks into our training programs</li>
</ul>

<p>Subscribe to our YouTube channel for regular updates and new content.</p>

<h4>Visit Our Channel</h4>
<p>Stay updated with our latest videos by subscribing to our channel.</p>
''',
                'meta_title': 'Video Gallery - Vastu & Engineering Tutorials',
                'meta_description': 'Watch videos on Vastu Shastra, engineering, construction techniques, and client testimonials.',
            },
            'Contact': {
                'slug': 'contact',
                'content': '''<h2>Contact Us</h2>
<p>Get in touch with us for Vastu consultation, engineering design, or training courses. We're here to help!</p>

<h3>Contact Information</h3>
<ul>
<li><strong>Address:</strong> Kathmandu, Nepal</li>
<li><strong>Phone:</strong> +977-1-XXXXXXXX</li>
<li><strong>Email:</strong> info@himawatkhandavastu.com</li>
<li><strong>WhatsApp:</strong> +977-XXXXXXXXXX</li>
</ul>

<h3>Office Hours</h3>
<ul>
<li>Monday - Friday: 10:00 AM - 6:00 PM</li>
<li>Saturday: 10:00 AM - 2:00 PM</li>
<li>Sunday: Closed</li>
</ul>

<h3>Services Inquiries</h3>
<p>For consultation requests, course inquiries, or general information, please reach out to us.</p>

<h3>Location</h3>
<p>Visit our office for a detailed discussion about your requirements. We recommend scheduling an appointment in advance.</p>

<h4>Get a Free Consultation</h4>
<p>Fill out our consultation form or call us to schedule a free initial consultation.</p>
''',
                'meta_title': 'Contact Us - Vastu & Engineering Services',
                'meta_description': 'Contact us for Vastu consultation, engineering design, and training courses. Office hours and contact information.',
            },
            'Construction Services': {
                'slug': 'construction-services',
                'content': '''<h2>Construction Services</h2>
<p>We provide complete construction services that blend Vastu principles with modern construction techniques. From foundation to finishing, we ensure quality construction at every step.</p>

<h3>Our Construction Services:</h3>
<ul>
<li><strong>Residential Construction:</strong> Homes, apartments, villas</li>
<li><strong>Commercial Construction:</strong> Offices, malls, showrooms</li>
<li><strong>Industrial Construction:</strong> Factories, warehouses</li>
<li><strong>Infrastructure Projects:</strong> Roads, drainage, utilities</li>
<li><strong>Vastu-Compliant Construction:</strong> Building with Vastu from ground up</li>
<li><strong>Turnkey Projects:</strong> Complete end-to-end construction</li>
</ul>

<h3>Construction Process:</h3>
<ol>
<li><strong>Site Preparation:</strong> Clearing, excavation, leveling</li>
<li><strong>Foundation:</strong> Strong and stable foundation work</li>
<li><strong>Superstructure:</strong> Walls, columns, beams, slabs</li>
<li><strong>Roofing:</strong> Waterproof and durable roofing</li>
<li><strong>Finishing:</strong> Flooring, painting, electrical, plumbing</li>
<li><strong>Handover:</strong> Clean and ready for possession</li>
</ol>

<h3>Why Choose Us?</h3>
<ul>
<li>Experienced engineers and supervisors</li>
<li>Quality materials and workmanship</li>
<li>Timely project completion</li>
<li>Transparent pricing</li>
<li>Vastu compliance throughout</li>
<li>Regular site updates</li>
</ul>

<p>Build your dream property with us!</p>
''',
                'meta_title': 'Construction Services - Building with Vastu Principles',
                'meta_description': 'Complete construction services with Vastu compliance. Residential, commercial, and industrial construction.',
            },
            'Vaastu Construction': {
                'slug': 'vaastu-construction',
                'content': '''<h2>Vaastu Construction Services</h2>
<p>Specialized construction services that follow Vastu principles from foundation to finishing. We ensure your building is constructed according to Vastu guidelines.</p>

<h3>Vastu Construction Features:</h3>
<ul>
<li><strong>Site Orientation:</strong> Proper alignment with directions</li>
<li><strong>Foundation Muhurat:</strong> Auspicious timing for ground-breaking</li>
<li><strong>Directional Construction:</strong> Building sequence as per Vastu</li>
<li><strong>Vastu Measurements:</strong> Dimensions using Vastu calculations</li>
<li><strong>Room Placement:</strong> Correct positioning as per directions</li>
<li><strong>Entrance Design:</strong> Main door in auspicious direction</li>
<li><strong>Vastu Remedies:</strong> Built-in remedies during construction</li>
</ul>

<h3>Benefits of Vastu Construction:</h3>
<ul>
<li>Harmonious living spaces</li>
<li>Positive energy flow</li>
<li>Better health and prosperity</li>
<li>Reduced Vastu defects</li>
<li>Peaceful environment</li>
</ul>

<h4>Vastu from Foundation to Finishing</h4>
<p>We ensure every aspect of construction follows Vastu principles for maximum benefits.</p>
''',
                'meta_title': 'Vaastu Construction - Vastu-Compliant Building',
                'meta_description': 'Vastu-compliant construction services from foundation to finishing. Build according to Vastu principles.',
            },
            'Residential Construction': {
                'slug': 'residential-construction',
                'content': '''<h2>Residential Construction Services</h2>
<p>Build your dream home with our expert residential construction services. We deliver quality homes that combine comfort, aesthetics, and Vastu principles.</p>

<h3>Residential Projects We Build:</h3>
<ul>
<li><strong>Custom Homes:</strong> Unique designs tailored to your needs</li>
<li><strong>Apartments:</strong> Multi-story residential buildings</li>
<li><strong>Villas:</strong> Luxury villas with modern amenities</li>
<li><strong>Townhouses:</strong> Stylish townhouse complexes</li>
<li><strong>Row Houses:</strong> Connected yet independent units</li>
</ul>

<h3>Construction Quality:</h3>
<ul>
<li>Earthquake-resistant structures</li>
<li>High-quality materials</li>
<li>Modern construction techniques</li>
<li>Proper ventilation and lighting</li>
<li>Waterproofing and damp-proofing</li>
<li>Electrical and plumbing safety</li>
<li>Beautiful finishing work</li>
</ul>

<h3>Our Process:</h3>
<ol>
<li>Design and planning phase</li>
<li>Approval and permits</li>
<li>Construction phase</li>
<li>Quality checks at each stage</li>
<li>Finishing and handover</li>
</ol>

<p>Your dream home deserves the best construction quality!</p>
''',
                'meta_title': 'Residential Construction Services - Custom Homes',
                'meta_description': 'Quality residential construction services. Custom homes, apartments, villas with Vastu compliance.',
            },
            'Industrial/Commercial Construction': {
                'slug': 'industrial-commercial-construction',
                'content': '''<h2>Industrial & Commercial Construction</h2>
<p>Professional construction services for industrial and commercial projects. We build functional, durable, and Vastu-compliant business spaces.</p>

<h3>Commercial Construction:</h3>
<ul>
<li>Office buildings and corporate parks</li>
<li>Shopping malls and retail centers</li>
<li>Hotels and restaurants</li>
<li>Hospitals and clinics</li>
<li>Educational institutions</li>
<li>Banks and financial institutions</li>
</ul>

<h3>Industrial Construction:</h3>
<ul>
<li>Factory buildings and warehouses</li>
<li>Manufacturing facilities</li>
<li>Processing plants</li>
<li>Cold storage and godowns</li>
<li>Industrial sheds</li>
</ul>

<h3>Key Features:</h3>
<ul>
<li>Structural integrity and safety</li>
<li>Optimal space utilization</li>
<li>Efficient workflow design</li>
<li>Vastu for business prosperity</li>
<li>Fire safety compliance</li>
<li>Modern amenities</li>
<li>Energy efficiency</li>
</ul>

<h3>Construction Excellence:</h3>
<p>We ensure your commercial or industrial property is built to the highest standards while following Vastu principles for business success.</p>
''',
                'meta_title': 'Industrial & Commercial Construction',
                'meta_description': 'Industrial and commercial construction services. Offices, malls, factories, warehouses with Vastu.',
            },
        }

        # Create pages
        self.stdout.write('Creating pages...')
        created_pages = {}
        for title, data in pages_structure.items():
            page, created = Page.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'title': title,
                    'content': data['content'],
                    'excerpt': data.get('meta_description', ''),
                    'meta_title': data.get('meta_title', title),
                    'meta_description': data.get('meta_description', ''),
                    'status': 'active',
                    'template': 'default',
                }
            )
            if created:
                self.stdout.write(f'  Created page: {title}')
            created_pages[title] = page

        # Create top menu
        self.stdout.write('Creating top navigation menu...')
        top_menu, created = Menu.objects.get_or_create(
            slug='top-menu',
            defaults={
                'name': 'Top Navigation',
                'location': 'top-bar',
            }
        )
        if created:
            self.stdout.write('  Created menu: Top Navigation')

        # Clear existing menu items
        top_menu.items.all().delete()

        # Create menu structure
        menu_structure = [
            {
                'title': 'Vastu Services',
                'page': created_pages['Vastu Services'],
                'order': 1,
            },
            {
                'title': 'Engineering Design',
                'page': created_pages['Engineering Design'],
                'order': 2,
            },
            {
                'title': 'Construction',
                'order': 3,
                'children': [
                    {'title': 'Vaastu', 'page': created_pages['Vaastu Construction'], 'order': 1},
                    {'title': 'Residential Construction', 'page': created_pages['Residential Construction'], 'order': 2},
                    {'title': 'Industrial/Commercial', 'page': created_pages['Industrial/Commercial Construction'], 'order': 3},
                    {'title': 'Infrastructure Development', 'page': created_pages['Infrastructure Development'], 'order': 4},
                ]
            },
            {
                'title': 'Consultation',
                'order': 4,
                'children': [
                    {'title': 'Vaastu Design', 'page': created_pages['Vaastu Design'], 'order': 1},
                    {'title': 'Residential Design', 'page': created_pages['Residential Design'], 'order': 2},
                    {'title': 'Industrial/Commercial Design', 'page': created_pages['Industrial/Commercial Design'], 'order': 3},
                    {'title': 'Infrastructure Development', 'page': created_pages['Infrastructure Development'], 'order': 4},
                ]
            },
            {
                'title': 'Courses',
                'order': 5,
                'children': [
                    {
                        'title': 'Vaastu Training',
                        'page': created_pages['Vaastu Training'],
                        'order': 1,
                        'children': [
                            {'title': 'Orientation Program for Owners', 'page': created_pages['Orientation Program for Owners'], 'order': 1},
                            {'title': 'Advance Vastu Training', 'page': created_pages['Advance Vastu Training'], 'order': 2},
                            {'title': 'Yantra Designing', 'page': created_pages['Yantra Designing'], 'order': 3},
                            {'title': 'Vastu CAD', 'page': created_pages['Vastu CAD'], 'order': 4},
                            {'title': 'Vedic Mantra (Diksha)', 'page': created_pages['Vedic Mantra (Diksha)'], 'order': 5},
                        ]
                    },
                    {'title': 'Engineering Training', 'page': created_pages['Engineering Training'], 'order': 2},
                    {'title': 'Mason Training', 'page': created_pages['Mason Training'], 'order': 3},
                ]
            },
            {
                'title': 'Videos',
                'page': created_pages['Videos'],
                'order': 6,
            },
            {
                'title': 'Contact',
                'page': created_pages['Contact'],
                'order': 7,
            },
        ]

        # Helper function to create menu items recursively
        def create_menu_item(item_data, parent=None):
            item = MenuItem.objects.create(
                menu=top_menu,
                title=item_data['title'],
                page=item_data.get('page'),
                url=item_data.get('url', ''),
                parent=parent,
                order=item_data['order'],
                type='page' if item_data.get('page') else 'custom_link',
                is_active=True,
            )

            # Create children if any
            if 'children' in item_data:
                for child_data in item_data['children']:
                    create_menu_item(child_data, parent=item)

            return item

        # Create all menu items
        for item_data in menu_structure:
            create_menu_item(item_data)
            self.stdout.write(f'  Added menu item: {item_data["title"]}')

        self.stdout.write(self.style.SUCCESS('Navigation setup completed successfully!'))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  Pages created/updated: {len(created_pages)}')
        self.stdout.write(f'  Menu items created: {MenuItem.objects.filter(menu=top_menu).count()}')
        self.stdout.write(f'\nTop navigation menu is ready!')
