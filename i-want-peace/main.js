document.addEventListener('DOMContentLoaded', () => {
    // Staggered Text Reveal Initialization
    const splitText = (el) => {
        const text = el.innerText;
        el.innerHTML = text.split('').map((char, i) => 
            `<span style="transition-delay: ${i * 40}ms">${char === ' ' ? '&nbsp;' : char}</span>`
        ).join('');
    };

    const heroTitle = document.querySelector('.hero h1');
    /* splitText call removed for image-based banner */

    // Parallax logic
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        // Background parallax
        const bg = document.querySelector('.parallax-bg');
        if (bg) {
            bg.style.transform = `translateY(${scrolled * 0.3}px) scale(1.1)`;
        }
        
        // Content parallax
        const heroContent = document.querySelector('.hero-content');
        if (heroContent) {
            const speed = heroContent.getAttribute('data-parallax-speed');
            heroContent.style.transform = `translateY(${scrolled * speed}px)`;
        }
    });

    // Race Showcase Logic
    const raceOptions = document.querySelectorAll('.race-option');
    const racePreview = document.getElementById('race-preview');
    const raceName = document.getElementById('race-name');
    const raceDescription = document.getElementById('race-description');
    const raceBg = document.querySelector('.race-bg-overlay');

    const raceData = {
        human: {
            name: "HUMAN",
            description: "Nobility and resilience. Humans are the cornerstone of the world's cities, mastering both diplomacy and steel.",
            img: "images/race_human.png",
            bg: "images/gallery_4.png"
        },
        druid: {
            name: "DRUID",
            description: "Guardians of the balance. Druids wield the raw power of nature, shifting between forms to protect the wild.",
            img: "images/race_druid.png",
            bg: "images/gallery_2.png"
        },
        ghost: {
            name: "GHOST",
            description: "Ethereal wanderers. Bound between realms, Ghosts use spectral abilities to phase through danger and haunt their foes.",
            img: "images/race_ghost.png",
            bg: "images/gallery_3.png"
        },
        goblin: {
            name: "GOBLIN",
            description: "Cunning inventors. Goblins thrive on ingenuity, using their small stature and mechanical brilliance to outsmart any threat.",
            img: "images/race_goblin.png",
            bg: "images/gallery_1.png"
        },
        elf: {
            name: "ELF",
            description: "Ethereal and timeless. Elves connect deeply with ancient magic and possess unmatched precision with the arcane.",
            img: "images/race_elf.png",
            bg: "images/gallery_2.png"
        },
        minotaur: {
            name: "MINOTAUR",
            description: "Unstoppable force. These massive warriors dominate the battlefield with sheer strength and unbreakable resolve.",
            img: "images/race_minotaur.png",
            bg: "images/gallery_1.png"
        },
        demon: {
            name: "DEMON",
            description: "Forged in shadow. Demons wield hellish fire and dark pacts to conquer those who stand in their way.",
            img: "images/race_demon.png",
            bg: "images/gallery_3.png"
        },
        angel: {
            name: "ANGEL",
            description: "Divine grace. Angels possess the wisdom of the skies and channel celestial light to heal or smite.",
            img: "images/race_angel.png",
            bg: "images/gallery_2.png"
        }
    };

    raceOptions.forEach(option => {
        option.addEventListener('mouseenter', () => {
            const race = option.getAttribute('data-race');
            updateRace(race);
            
            raceOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
        });
    });

    function updateRace(raceKey) {
        const data = raceData[raceKey];
        if (!data) return;

        // Visual Reset
        raceDisplay.style.opacity = '0';
        raceDisplay.style.transform = 'translateY(10px)';
        
        // Atmospheric shift
        const mood = document.querySelector('.atmospheric-mood');
        const colors = {
            human: 'rgba(212, 175, 55, 0.08)',
            druid: 'rgba(34, 197, 94, 0.12)',
            ghost: 'rgba(147, 197, 253, 0.12)',
            goblin: 'rgba(101, 163, 13, 0.15)',
            elf: 'rgba(129, 140, 248, 0.12)',
            minotaur: 'rgba(180, 83, 9, 0.15)',
            demon: 'rgba(239, 68, 68, 0.15)',
            angel: 'rgba(255, 255, 255, 0.12)'
        };

        setTimeout(() => {
            raceName.textContent = data.name;
            raceDescription.textContent = data.description;
            racePreview.src = data.img;
            
            if (mood) {
                mood.style.background = `radial-gradient(circle at 50% 50%, ${colors[raceKey] || colors.human} 0%, transparent 70%)`;
                document.body.style.setProperty('--accent-glow', colors[raceKey] || colors.human);
            }

            raceDisplay.style.opacity = '1';
            raceDisplay.style.transform = 'translateY(0)';
        }, 300);
    }

    // Initialize with Human
    updateRace('human');

    // Magnetic Effect Logic
    const magneticElements = document.querySelectorAll('.cta-btn, .path-card, .race-option');
    
    magneticElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            el.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px) scale(1.02)`;
            if (el.classList.contains('path-card')) {
                el.style.transform += ` translateY(-10px)`;
            }
        });

        el.addEventListener('mouseleave', () => {
            el.style.transform = '';
        });
    });

    // Particle Engine
    function createParticles(containerId, count, color) {
        const container = document.getElementById(containerId);
        if (!container) return;

        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Randomize properties
            const size = Math.random() * 5 + 2;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.background = color || 'white';
            particle.style.animationDuration = `${Math.random() * 5 + 5}s`;
            particle.style.animationDelay = `${Math.random() * 5}s`;
            
            container.appendChild(particle);
        }
    }

    createParticles('hero-particles', 30, 'var(--gold-bright)');

    // Intersection Observer for Reveal Animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // Simple mobile menu toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if (navLinks.style.display === 'flex') {
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.flexDirection = 'column';
                navLinks.style.background = 'rgba(10,10,10,0.95)';
                navLinks.style.padding = '2rem';
                navLinks.style.textAlign = 'center';
            }
        });
    }
});
