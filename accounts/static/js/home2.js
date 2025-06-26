document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector(".navbar");
    const mobileNavToggle = document.querySelector(".mobile-nav-toggle");
    const overlay = document.querySelector(".overlay");
    const profileIcon = document.querySelector(".profile-icon");
    const profileInfo = document.querySelector(".profile-info");
    const dropdownMenu = document.querySelector(".dropdown-menu");
    const heading = document.querySelector(".main-heading");
    let isMenuOpen = false;

    // Scroll effect for navbar
    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    // Toggle mobile menu
    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
        mobileNavToggle.classList.toggle("active");
        overlay.classList.toggle("active");
        document.body.style.overflow = isMenuOpen ? "hidden" : "auto";
    }

    // Toggle dropdown menu
    profileInfo?.addEventListener("click", function (event) {
        event.stopPropagation();
        dropdownMenu?.classList.toggle("active");
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function (event) {
        if (!profileInfo?.contains(event.target) && !dropdownMenu?.contains(event.target)) {
            dropdownMenu?.classList.remove("active");
        }
    });

    // Event listeners
    mobileNavToggle?.addEventListener("click", toggleMenu);
    overlay?.addEventListener("click", toggleMenu);

    // Heading fade-in animation
    if (heading) {
        heading.style.opacity = "0";
        heading.style.transform = "translateY(10px)";
        
        setTimeout(() => {
            heading.style.transition = "opacity 0.8s ease-out, transform 0.8s ease-out";
            heading.style.opacity = "1";
            heading.style.transform = "translateY(0)";
        }, 300);
    }
});