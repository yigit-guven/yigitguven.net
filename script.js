// Theme switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeSwitcher = document.getElementById('themeSwitcher');
    if (themeSwitcher) {
        const themeIcon = themeSwitcher.querySelector('i');
        
        // Check for saved theme preference or respect OS preference
        if (localStorage.getItem('theme') === 'light' || 
            (window.matchMedia('(prefers-color-scheme: light)').matches && !localStorage.getItem('theme'))) {
            document.body.classList.add('light-theme');
            if (themeIcon) {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            }
        }
        
        themeSwitcher.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            
            if (document.body.classList.contains('light-theme')) {
                localStorage.setItem('theme', 'light');
                if (themeIcon) {
                    themeIcon.classList.remove('fa-moon');
                    themeIcon.classList.add('fa-sun');
                }
            } else {
                localStorage.setItem('theme', 'dark');
                if (themeIcon) {
                    themeIcon.classList.remove('fa-sun');
                    themeIcon.classList.add('fa-moon');
                }
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '#!') return;
            
            e.preventDefault();
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Additional JavaScript for the interactive element (404 page)
    const funButton = document.getElementById('fun-button');
    if (funButton) {
        const jokeContainer = document.getElementById('joke-container');
        
        // Array of developer jokes
        const jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why do Java developers wear glasses? Because they can't C#!",
            "A SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?'",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25!",
            "There are only 10 types of people in the world: those who understand binary and those who don't.",
            "Why did the developer go broke? Because he used up all his cache!",
            "What do you call a programmer from Finland? Nerdic.",
            "How do you comfort a JavaScript bug? You console it!",
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "What do cats and programmers have in common? When they're happy, they push things off tables."
        ];
        
        funButton.addEventListener('click', function() {
            // Select a random joke
            const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
            
            // Display the joke
            jokeContainer.innerHTML = `<p>${randomJoke}</p>`;
            jokeContainer.style.display = 'block';
            
            // Change button text
            funButton.textContent = 'Another Joke!';
        });
        
        // Add floating animation to the 404 text with slight variations
        const giant404 = document.querySelector('.giant-404');
        if (giant404) {
            setInterval(() => {
                giant404.classList.toggle('floating');
            }, 6000);
        }
    }
});// Theme switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeSwitcher = document.getElementById('themeSwitcher');
    if (themeSwitcher) {
        const themeIcon = themeSwitcher.querySelector('i');
        
        // Check for saved theme preference or respect OS preference
        if (localStorage.getItem('theme') === 'light' || 
            (window.matchMedia('(prefers-color-scheme: light)').matches && !localStorage.getItem('theme'))) {
            document.body.classList.add('light-theme');
            if (themeIcon) {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            }
        }
        
        themeSwitcher.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            
            if (document.body.classList.contains('light-theme')) {
                localStorage.setItem('theme', 'light');
                if (themeIcon) {
                    themeIcon.classList.remove('fa-moon');
                    themeIcon.classList.add('fa-sun');
                }
            } else {
                localStorage.setItem('theme', 'dark');
                if (themeIcon) {
                    themeIcon.classList.remove('fa-sun');
                    themeIcon.classList.add('fa-moon');
                }
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '#!') return;
            
            e.preventDefault();
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Additional JavaScript for the interactive element (404 page)
    const funButton = document.getElementById('fun-button');
    if (funButton) {
        const jokeContainer = document.getElementById('joke-container');
        
        // Array of developer jokes
        const jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why do Java developers wear glasses? Because they can't C#!",
            "A SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?'",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25!",
            "There are only 10 types of people in the world: those who understand binary and those who don't.",
            "Why did the developer go broke? Because he used up all his cache!",
            "What do you call a programmer from Finland? Nerdic.",
            "How do you comfort a JavaScript bug? You console it!",
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "What do cats and programmers have in common? When they're happy, they push things off tables."
        ];
        
        funButton.addEventListener('click', function() {
            // Select a random joke
            const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
            
            // Display the joke
            jokeContainer.innerHTML = `<p>${randomJoke}</p>`;
            jokeContainer.style.display = 'block';
            
            // Change button text
            funButton.textContent = 'Another Joke!';
        });
        
        // Add floating animation to the 404 text with slight variations
        const giant404 = document.querySelector('.giant-404');
        if (giant404) {
            setInterval(() => {
                giant404.classList.toggle('floating');
            }, 6000);
        }
    }
});