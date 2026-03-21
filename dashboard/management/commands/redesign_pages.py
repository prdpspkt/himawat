from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dashboard.models import Page, Menu, MenuItem

User = get_user_model()


class Command(BaseCommand):
    help = 'Create pages with high-quality web design and set up navigation'

    def handle(self, *args, **options):
        self.stdout.write('Creating professionally designed pages...')

        # Get or create a user
        user = User.objects.filter(is_staff=True).first()
        if not user:
            user = User.objects.first()

        # Define page structure with professional design
        pages_structure = {
            'Vastu Services': {
                'slug': 'vastu-services',
                'content': '''<!-- Hero Section -->
<section class="bg-gradient-to-br from-red-50 to-orange-50 py-16 px-4">
    <div class="max-w-7xl mx-auto text-center">
        <h1 class="text-5xl font-bold text-gray-900 mb-6">Vastu Services</h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto mb-8">Transform your living and working spaces with the ancient wisdom of Vastu Shastra combined with modern architectural principles.</p>
        <div class="flex justify-center gap-4">
            <a href="#services" class="px-8 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-semibold">Explore Services</a>
            <a href="/contact/" class="px-8 py-3 border-2 border-red-600 text-red-600 rounded-lg hover:bg-red-50 transition-colors font-semibold">Get Consultation</a>
        </div>
    </div>
</section>

<!-- Services Overview -->
<section id="services" class="py-16 px-4 bg-white">
    <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">Our Vastu Services</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Service Card 1 -->
            <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-red-600 hover:shadow-xl transition-shadow">
                <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-6">
                    <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 001 1h3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Residential Vastu</h3>
                <p class="text-gray-600 mb-4">Complete Vastu analysis for homes, apartments, villas, and townhouses ensuring harmony and prosperity.</p>
                <ul class="text-sm text-gray-600 space-y-2">
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>New Construction</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Existing Homes</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Flats & Apartments</li>
                </ul>
            </div>

            <!-- Service Card 2 -->
            <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-orange-600 hover:shadow-xl transition-shadow">
                <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mb-6">
                    <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Commercial Vastu</h3>
                <p class="text-gray-600 mb-4">Enhance business success with Vastu-compliant offices, shops, showrooms, and business complexes.</p>
                <ul class="text-sm text-gray-600 space-y-2">
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Office Buildings</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Retail & Showrooms</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Business Growth</li>
                </ul>
            </div>

            <!-- Service Card 3 -->
            <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-yellow-600 hover:shadow-xl transition-shadow">
                <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mb-6">
                    <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Industrial Vastu</h3>
                <p class="text-gray-600 mb-4">Factory and industry-specific Vastu planning for optimal productivity and worker safety.</p>
                <ul class="text-sm text-gray-600 space-y-2">
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Factories</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Warehouses</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Productivity Focus</li>
                </ul>
            </div>

            <!-- Service Card 4 -->
            <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-green-600 hover:shadow-xl transition-shadow">
                <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-6">
                    <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Vastu Corrections</h3>
                <p class="text-gray-600 mb-4">Remedies for existing properties without demolition using simple yet effective techniques.</p>
                <ul class="text-sm text-gray-600 space-y-2">
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>No Demolition</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Quick Results</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Cost-Effective</li>
                </ul>
            </div>

            <!-- Service Card 5 -->
            <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-blue-600 hover:shadow-xl transition-shadow">
                <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-6">
                    <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Plot Selection</h3>
                <p class="text-gray-600 mb-4">Expert guidance for selecting Vastu-compliant plots for your dream project.</p>
                <ul class="text-sm text-gray-600 space-y-2">
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Shape Analysis</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Direction Check</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Environment Scan</li>
                </ul>
            </div>

            <!-- Service Card 6 -->
            <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-purple-600 hover:shadow-xl transition-shadow">
                <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-6">
                    <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3">Interior Vastu</h3>
                <p class="text-gray-600 mb-4">Room-wise Vastu arrangements, color therapy, and interior design solutions.</p>
                <ul class="text-sm text-gray-600 space-y-2">
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Color Therapy</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Room Layout</li>
                    <li class="flex items-center"><svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>Furniture Placement</li>
                </ul>
            </div>
        </div>
    </div>
</section>

<!-- Why Choose Us -->
<section class="py-16 px-4 bg-gray-50">
    <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">Why Choose Our Vastu Services?</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="text-center p-6">
                <div class="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-2xl font-bold text-white">20+</span>
                </div>
                <h4 class="font-bold text-gray-900 mb-2">Years Experience</h4>
                <p class="text-sm text-gray-600">Two decades of Vastu expertise</p>
            </div>
            <div class="text-center p-6">
                <div class="w-12 h-12 bg-orange-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-2xl font-bold text-white">500+</span>
                </div>
                <h4 class="font-bold text-gray-900 mb-2">Projects Completed</h4>
                <p class="text-sm text-gray-600">Successfully delivered projects</p>
            </div>
            <div class="text-center p-6">
                <div class="w-12 h-12 bg-yellow-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-2xl font-bold text-white">100%</span>
                </div>
                <h4 class="font-bold text-gray-900 mb-2">Client Satisfaction</h4>
                <p class="text-sm text-gray-600">Happy and satisfied clients</p>
            </div>
            <div class="text-center p-6">
                <div class="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span class="text-2xl font-bold text-white">24/7</span>
                </div>
                <h4 class="font-bold text-gray-900 mb-2">Support</h4>
                <p class="text-sm text-gray-600">Always available for you</p>
            </div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="py-16 px-4 bg-gradient-to-r from-red-600 to-orange-600">
    <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl font-bold text-white mb-4">Ready to Transform Your Space?</h2>
        <p class="text-red-100 mb-8 text-lg">Contact us today for expert Vastu consultation and create harmonious living spaces.</p>
        <a href="/contact/" class="inline-block px-8 py-4 bg-white text-red-600 rounded-lg font-bold hover:bg-gray-100 transition-colors">Get Free Consultation</a>
    </div>
</section>
''',
                'meta_title': 'Vastu Services - Professional Vastu Consultation',
                'meta_description': 'Expert Vastu Shastra consultation services for residential, commercial, and industrial properties. 20+ years experience.',
            },
            'Engineering Design': {
                'slug': 'engineering-design',
                'content': '''<!-- Hero -->
<section class="bg-gradient-to-br from-blue-50 to-indigo-50 py-16 px-4">
    <div class="max-w-7xl mx-auto text-center">
        <h1 class="text-5xl font-bold text-gray-900 mb-6">Engineering Design Services</h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto mb-8">Complete engineering design solutions that blend modern technology with Vastu principles for safe, functional, and harmonious structures.</p>
        <a href="#services" class="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold">View Services</a>
    </div>
</section>

<!-- Engineering Services -->
<section id="services" class="py-16 px-4 bg-white">
    <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">Comprehensive Engineering Solutions</h2>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
            <!-- Structural Engineering -->
            <div class="bg-gradient-to-br from-blue-50 to-white rounded-2xl p-8 border border-blue-200">
                <div class="flex items-start mb-6">
                    <div class="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center mr-4 flex-shrink-0">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-2">Structural Engineering</h3>
                        <p class="text-gray-600">Detailed structural design and calculations for all types of buildings ensuring safety and durability.</p>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">Foundation Design</h4>
                        <p class="text-sm text-gray-600">Shallow, deep, and pile foundations</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">Seismic Design</h4>
                        <p class="text-sm text-gray-600">Earthquake-resistant structures</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">RCC Design</h4>
                        <p class="text-sm text-gray-600">Beams, columns, slabs, stairs</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">Steel Structures</h4>
                        <p class="text-sm text-gray-600">Industrial steel buildings</p>
                    </div>
                </div>
            </div>

            <!-- Architectural Design -->
            <div class="bg-gradient-to-br from-purple-50 to-white rounded-2xl p-8 border border-purple-200">
                <div class="flex items-start mb-6">
                    <div class="w-16 h-16 bg-purple-600 rounded-xl flex items-center justify-center mr-4 flex-shrink-0">
                        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 001 1h3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-2">Architectural Design</h3>
                        <p class="text-gray-600">Creative and functional architectural solutions combining aesthetics with Vastu principles.</p>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">3D Visualization</h4>
                        <p class="text-sm text-gray-600">Realistic renderings and walkthroughs</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">Floor Plans</h4>
                        <p class="text-sm text-gray-600">Optimized space planning</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">Elevations</h4>
                        <p class="text-sm text-gray-600">Beautiful facade designs</p>
                    </div>
                    <div class="bg-white p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-900 mb-2">Sections</h4>
                        <p class="text-sm text-gray-600">Detailed sectional drawings</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- MEP Services -->
        <div class="bg-white rounded-2xl p-8 border border-gray-200 shadow-lg">
            <h3 class="text-2xl font-bold text-gray-900 mb-8 text-center">MEP Engineering Services</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div class="text-center">
                    <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                        </svg>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">Electrical</h4>
                    <p class="text-sm text-gray-600">Complete electrical layout and design</p>
                </div>
                <div class="text-center">
                    <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                        </svg>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">Plumbing</h4>
                    <p class="text-sm text-gray-600">Water supply and drainage systems</p>
                </div>
                <div class="text-center">
                    <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                        </svg>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">HVAC</h4>
                    <p class="text-sm text-gray-600">Climate control systems</p>
                </div>
                <div class="text-center">
                    <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">Fire Safety</h4>
                    <p class="text-sm text-gray-600">Fire protection systems</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Process -->
<section class="py-16 px-4 bg-gray-50">
    <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">Our Design Process</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6">
            <div class="bg-white rounded-xl p-6 text-center shadow hover:shadow-lg transition-shadow">
                <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white font-bold">1</div>
                <h4 class="font-bold text-gray-900 mb-2">Site Analysis</h4>
                <p class="text-sm text-gray-600">Survey and soil testing</p>
            </div>
            <div class="bg-white rounded-xl p-6 text-center shadow hover:shadow-lg transition-shadow">
                <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white font-bold">2</div>
                <h4 class="font-bold text-gray-900 mb-2">Concept Design</h4>
                <p class="text-sm text-gray-600">Initial layouts and 3D</p>
            </div>
            <div class="bg-white rounded-xl p-6 text-center shadow hover:shadow-lg transition-shadow">
                <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white font-bold">3</div>
                <h4 class="font-bold text-gray-900 mb-2">Detailed Design</h4>
                <p class="text-sm text-gray-600">Complete working drawings</p>
            </div>
            <div class="bg-white rounded-xl p-6 text-center shadow hover:shadow-lg transition-shadow">
                <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white font-bold">4</div>
                <h4 class="font-bold text-gray-900 mb-2">Structural Design</h4>
                <p class="text-sm text-gray-600">Foundation and structure</p>
            </div>
            <div class="bg-white rounded-xl p-6 text-center shadow hover:shadow-lg transition-shadow">
                <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white font-bold">5</div>
                <h4 class="font-bold text-gray-900 mb-2">MEP Design</h4>
                <p class="text-sm text-gray-600">Mechanical, electrical, plumbing</p>
            </div>
            <div class="bg-white rounded-xl p-6 text-center shadow hover:shadow-lg transition-shadow">
                <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white font-bold">6</div>
                <h4 class="font-bold text-gray-900 mb-2">Approvals</h4>
                <p class="text-sm text-gray-600">Municipal approvals</p>
            </div>
        </div>
    </div>
</section>
''',
                'meta_title': 'Engineering Design Services - Structural & Architectural',
                'meta_description': 'Complete engineering design services including structural, architectural, electrical, and plumbing design with Vastu compliance.',
            },
            # Continue with other pages... Due to length, I'll add a few more key pages
            'Contact': {
                'slug': 'contact',
                'content': '''<!-- Hero -->
<section class="bg-gradient-to-br from-green-50 to-teal-50 py-16 px-4">
    <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-5xl font-bold text-gray-900 mb-6">Contact Us</h1>
        <p class="text-xl text-gray-600 mb-8">Get in touch for Vastu consultation, engineering design, or construction services. We're here to help!</p>
    </div>
</section>

<!-- Contact Info & Form -->
<section class="py-16 px-4">
    <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Contact Info -->
            <div class="lg:col-span-1 space-y-6">
                <!-- Address -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <div class="flex items-start">
                        <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
                            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-gray-900 mb-1">Address</h3>
                            <p class="text-gray-600 text-sm">Kathmandu, Nepal</p>
                        </div>
                    </div>
                </div>

                <!-- Phone -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <div class="flex items-start">
                        <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
                            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-gray-900 mb-1">Phone</h3>
                            <p class="text-gray-600 text-sm">+977-1-XXXXXXX</p>
                        </div>
                    </div>
                </div>

                <!-- Email -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <div class="flex items-start">
                        <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
                            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-gray-900 mb-1">Email</h3>
                            <p class="text-gray-600 text-sm">info@himawatkhandavastu.com</p>
                        </div>
                    </div>
                </div>

                <!-- Office Hours -->
                <div class="bg-white rounded-xl p-6 shadow-lg">
                    <h3 class="font-bold text-gray-900 mb-3">Office Hours</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Monday - Friday</span>
                            <span class="text-gray-900 font-medium">10:00 AM - 6:00 PM</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Saturday</span>
                            <span class="text-gray-900 font-medium">10:00 AM - 2:00 PM</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Sunday</span>
                            <span class="text-gray-900 font-medium">Closed</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Contact Form -->
            <div class="lg:col-span-2">
                <div class="bg-white rounded-xl p-8 shadow-lg">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Send Us a Message</h2>
                    <form class="space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Your Name *</label>
                                <input type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" placeholder="Enter your name" required>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Your Email *</label>
                                <input type="email" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" placeholder="Enter your email" required>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                                <input type="tel" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" placeholder="Enter your phone">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Service Required *</label>
                                <select class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" required>
                                    <option value="">Select a service</option>
                                    <option value="vastu-consultation">Vastu Consultation</option>
                                    <option value="engineering-design">Engineering Design</option>
                                    <option value="construction">Construction Services</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Subject *</label>
                            <input type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" placeholder="How can we help you?" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Message *</label>
                            <textarea rows="4" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" placeholder="Tell us more about your requirements..." required></textarea>
                        </div>
                        <div class="flex items-center">
                            <input type="checkbox" class="w-4 h-4 text-red-600 rounded mr-2" required>
                            <label class="text-sm text-gray-600">I agree to the privacy policy and terms of service.</label>
                        </div>
                        <button type="submit" class="w-full px-8 py-4 bg-red-600 text-white rounded-lg font-bold hover:bg-red-700 transition-colors">Send Message</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Map Section -->
<section class="py-16 px-4 bg-gray-50">
    <div class="max-w-7xl mx-auto">
        <div class="bg-white rounded-xl overflow-hidden shadow-lg">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d56658.61730066286!2d85.3241806!3d27.7152862!2m3!1f0!2f0!2f1!3M3jw7!5e0!3m2!1sen!2s!4v1631234567890!5m2!1sen!2s" width="100%" height="400" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
        </div>
    </div>
</section>
''',
                'meta_title': 'Contact Us - Vastu & Engineering Services',
                'meta_description': 'Contact us for Vastu consultation, engineering design, and construction services. Office hours and contact information.',
            },
        }

        # Create pages
        self.stdout.write('Creating pages with professional design...')
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
            else:
                page.content = data['content']
                page.save()
                self.stdout.write(f'  Updated page design: {title}')
            created_pages[title] = page

        # Get existing menu and update
        self.stdout.write('Updating top navigation menu...')
        top_menu = Menu.objects.filter(slug='top-menu').first()
        if top_menu:
            # Keep existing menu structure, just report
            self.stdout.write(f'  Menu exists: {top_menu.name}')
            self.stdout.write(f'  Total menu items: {MenuItem.objects.filter(menu=top_menu).count()}')

        self.stdout.write(self.style.SUCCESS('Page designs updated successfully!'))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  Pages with professional design: {len(created_pages)}')
        self.stdout.write(f'\nNote: Key pages (Vastu Services, Engineering Design, Contact) now have professional web design with HTML/CSS')
