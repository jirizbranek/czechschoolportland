// Czech School Portland - Custom Analytics Tracking
// This file adds enhanced tracking for school-specific events

// Wait for Google Analytics to load
window.addEventListener('load', function () {
    if (typeof gtag !== 'undefined') {
        initSchoolAnalytics();
    }
});

function initSchoolAnalytics() {
    console.log('🎯 School Analytics initialized');

    // Track mailing list signups
    trackMailingListSignups();

    // Track event calendar interactions
    trackCalendarEvents();

    // Track file downloads
    trackFileDownloads();

    // Track external link clicks
    trackExternalLinks();

    // Track admin page access
    trackAdminAccess();

    // Track class page engagement
    trackClassEngagement();
}

// Track mailing list form submissions
function trackMailingListSignups() {
    const mailingForms = document.querySelectorAll('form[action*="mailing"]');
    mailingForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const email = form.querySelector('input[type="email"]')?.value;

            gtag('event', 'newsletter_signup', {
                event_category: 'engagement',
                event_label: 'mailing_list_subscription',
                value: 1
            });

            console.log('📧 Mailing list signup tracked');
        });
    });
}

// Track calendar and event interactions
function trackCalendarEvents() {
    // Track calendar page visits
    if (window.location.pathname.includes('/calendar')) {
        gtag('event', 'page_view', {
            event_category: 'calendar',
            event_label: 'calendar_page_view',
            page_title: document.title
        });
    }

    // Track event detail clicks
    const eventLinks = document.querySelectorAll('a[href*="event"], .event-link');
    eventLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const eventTitle = this.textContent || this.getAttribute('title') || 'unknown_event';

            gtag('event', 'event_click', {
                event_category: 'events',
                event_label: eventTitle.substring(0, 50), // Limit length
                value: 1
            });

            console.log('📅 Event click tracked:', eventTitle);
        });
    });
}

// Track file downloads (PDFs, images, documents)
function trackFileDownloads() {
    const downloadableFiles = document.querySelectorAll('a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href$=".jpg"], a[href$=".png"]');

    downloadableFiles.forEach(link => {
        link.addEventListener('click', function (e) {
            const fileName = this.href.split('/').pop();
            const fileType = fileName.split('.').pop();

            gtag('event', 'file_download', {
                event_category: 'downloads',
                event_label: fileName,
                file_extension: fileType
            });

            console.log('📁 File download tracked:', fileName);
        });
    });
}

// Track external link clicks
function trackExternalLinks() {
    const externalLinks = document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])');

    externalLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const destination = new URL(this.href).hostname;

            gtag('event', 'click', {
                event_category: 'outbound',
                event_label: destination,
                transport_type: 'beacon'
            });

            console.log('🔗 External link tracked:', destination);
        });
    });
}

// Track admin page access (for security monitoring)
function trackAdminAccess() {
    if (window.location.pathname.includes('/admin')) {
        gtag('event', 'admin_access', {
            event_category: 'security',
            event_label: 'admin_page_view',
            page_path: window.location.pathname
        });

        console.log('🔐 Admin access tracked');
    }
}

// Track class page engagement
function trackClassEngagement() {
    if (window.location.pathname.includes('/classes')) {
        // Track time spent on classes page
        let startTime = Date.now();

        window.addEventListener('beforeunload', function () {
            let timeSpent = Math.round((Date.now() - startTime) / 1000);

            if (timeSpent > 5) { // Only track if spent more than 5 seconds
                gtag('event', 'timing_complete', {
                    name: 'classes_page_engagement',
                    value: timeSpent,
                    event_category: 'engagement'
                });
            }
        });

        // Track specific class interest
        const classLinks = document.querySelectorAll('a[href*="class"], .class-link');
        classLinks.forEach(link => {
            link.addEventListener('click', function (e) {
                const className = this.textContent || 'unknown_class';

                gtag('event', 'class_interest', {
                    event_category: 'classes',
                    event_label: className.substring(0, 50),
                    value: 1
                });
            });
        });
    }
}

// Track form errors and success
function trackFormInteractions() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const formName = this.getAttribute('name') || this.getAttribute('id') || 'unnamed_form';

            gtag('event', 'form_submit', {
                event_category: 'forms',
                event_label: formName
            });
        });
    });
}

// Track scroll depth (to measure content engagement)
function trackScrollDepth() {
    let maxScroll = 0;
    let trackedPercentages = [];

    window.addEventListener('scroll', function () {
        const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);

        if (scrollPercent > maxScroll) {
            maxScroll = scrollPercent;

            // Track at 25%, 50%, 75%, 100%
            [25, 50, 75, 100].forEach(percentage => {
                if (scrollPercent >= percentage && !trackedPercentages.includes(percentage)) {
                    trackedPercentages.push(percentage);

                    gtag('event', 'scroll', {
                        event_category: 'engagement',
                        event_label: percentage + '%',
                        value: percentage
                    });
                }
            });
        }
    });
}

// Initialize scroll tracking on content pages
if (!window.location.pathname.includes('/admin')) {
    trackScrollDepth();
}

// Initialize form tracking
trackFormInteractions();
