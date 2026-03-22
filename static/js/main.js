/**
 * Main JavaScript for Himwatkhanda Vastu
 * Handles UI interactions, accessibility features, and progressive enhancement
 */

(function() {
    'use strict';

    // =================================================================================
    // Mobile Menu Handling
    // =================================================================================
    
    function initMobileMenu() {
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', function() {
                const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
                mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
                mobileMenu.classList.toggle('hidden');
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', function(e) {
                if (mobileMenu && !mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                    mobileMenu.classList.add('hidden');
                    mobileMenuBtn.setAttribute('aria-expanded', 'false');
                }
            });
            
            // Close menu on escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                    mobileMenuBtn.setAttribute('aria-expanded', 'false');
                    mobileMenuBtn.focus();
                }
            });
        }
    }

    // =================================================================================
    // Form Validation & Confirmation
    // =================================================================================
    
    function initDeleteConfirmations() {
        const deleteForms = document.querySelectorAll('form[data-confirm]');
        
        deleteForms.forEach(function(form) {
            form.addEventListener('submit', function(e) {
                const message = this.getAttribute('data-confirm') || 'Are you sure you want to delete this item?';
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    }

    // =================================================================================
    // Auto-Dismiss Alerts
    // =================================================================================
    
    function initAutoDismissAlerts() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        
        alerts.forEach(function(alert) {
            // Don't auto-dismiss error alerts
            if (alert.classList.contains('alert-danger')) return;
            
            setTimeout(function() {
                if (alert.parentNode) {
                    alert.style.opacity = '0';
                    alert.style.transition = 'opacity 0.5s ease';
                    setTimeout(function() {
                        if (alert.parentNode) {
                            const bsAlert = bootstrap.Alert.getInstance(alert);
                            if (bsAlert) {
                                bsAlert.close();
                            } else {
                                alert.remove();
                            }
                        }
                    }, 500);
                }
            }, 5000);
        });
    }

    // =================================================================================
    // Smooth Scroll for Anchor Links
    // =================================================================================
    
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Set focus for accessibility
                    target.setAttribute('tabindex', '-1');
                    target.focus({ preventScroll: true });
                }
            });
        });
    }

    // =================================================================================
    // Lazy Loading Images
    // =================================================================================
    
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const lazyImages = document.querySelectorAll('img[data-src]');
            
            const imageObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        
                        // Add fade-in effect
                        img.style.opacity = '0';
                        img.style.transition = 'opacity 0.3s ease';
                        img.onload = function() {
                            img.style.opacity = '1';
                        };
                        
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });
            
            lazyImages.forEach(function(img) {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for browsers without IntersectionObserver
            document.querySelectorAll('img[data-src]').forEach(function(img) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        }
    }

    // =================================================================================
    // Utility Functions
    // =================================================================================
    
    // Format file size for display
    window.formatFileSize = function(bytes) {
        if (bytes === 0) return '0 Bytes';
        if (!bytes || isNaN(bytes)) return 'Unknown';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    // Create URL-friendly slug
    window.slugify = function(text) {
        if (!text) return '';
        
        return text
            .toString()
            .toLowerCase()
            .trim()
            .replace(/\s+/g, '-')
            .replace(/[^\w\-]+/g, '')
            .replace(/\-\-+/g, '-');
    };

    // Copy to clipboard with feedback
    window.copyToClipboard = function(text) {
        if (!navigator.clipboard) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                showToast('Copied to clipboard!', 'success');
            } catch (err) {
                showToast('Failed to copy', 'error');
            }
            
            document.body.removeChild(textArea);
            return;
        }
        
        navigator.clipboard.writeText(text).then(function() {
            showToast('Copied to clipboard!', 'success');
        }).catch(function() {
            showToast('Failed to copy', 'error');
        });
    };

    // Show toast notification
    function showToast(message, type) {
        const toast = document.createElement('div');
        const bgClass = type === 'error' ? 'bg-danger' : 'bg-success';
        
        toast.className = 'position-fixed bottom-0 end-0 m-3 ' + bgClass + ' text-white px-4 py-2 rounded shadow-lg';
        toast.style.cssText = 'z-index: 9999; animation: slideIn 0.3s ease;';
        toast.textContent = message;
        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');
        
        // Add animation styles if not present
        if (!document.getElementById('toast-styles')) {
            const style = document.createElement('style');
            style.id = 'toast-styles';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(toast);
        
        setTimeout(function() {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(function() {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 300);
        }, 2000);
    }

    // =================================================================================
    // Print Helper
    // =================================================================================
    
    function initPrintHelper() {
        // Add print button functionality for any element with data-print attribute
        document.querySelectorAll('[data-print]').forEach(function(el) {
            el.addEventListener('click', function(e) {
                e.preventDefault();
                window.print();
            });
        });
    }

    // =================================================================================
    // Initialize Everything on DOM Ready
    // =================================================================================
    
    function init() {
        initMobileMenu();
        initDeleteConfirmations();
        initAutoDismissAlerts();
        initSmoothScroll();
        initLazyLoading();
        initPrintHelper();
    }

    // Run initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
