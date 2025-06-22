$(document).ready(function () {
    $(window).scroll(function () {
        // sticky navbar on scroll script
        if (this.scrollY > 20) {
            document.body.style.backgroundColor = "#f0945f";
            $('.navbar').addClass("sticky");
        } else {
            $('.navbar').removeClass("sticky");
            document.body.style.backgroundColor = "#f1f1f1";
        }

        // scroll-up button show/hide script
        if (this.scrollY > 500) {
            $('.scroll-up-btn').addClass("show");
        } else {
            $('.scroll-up-btn').removeClass("show");
        }
    });

    // slide-up script
    $('.scroll-up-btn').click(function () {
        $('html').animate({ scrollTop: 0 });
        // removing smooth scroll on slide-up button click
        $('html').css("scrollBehavior", "auto");
    });

    $('.navbar .menu li a').click(function () {
        // applying again smooth scroll on menu items click
        $('html').css("scrollBehavior", "smooth");
    });

    // toggle menu/navbar script
    $('.menu-btn').click(function () {
        $('.navbar .menu').toggleClass("active");
        $('.menu-btn i').toggleClass("active");
    });

    // Toggle night mode icon
    $('#night-mode-toggle').click(function (e) {
        e.preventDefault(); // Prevent the default link behavior
        const icon = $(this).find('i');
        icon.toggleClass('fa-moon fa-sun');
    });

    // Code to dynamically add the gallery images
    const galleryContainer = document.getElementById('gallery-images');
    if (galleryContainer && typeof images !== 'undefined') {
        images.forEach(image => {
            const cardItem = document.createElement('div');
            cardItem.className = 'card-item swiper-slide';

            const imgElement = document.createElement('img');
            imgElement.src = image.src;
            imgElement.alt = image.alt;
            imgElement.onerror = function() {
                console.error(`Failed to load image: ${image.src}`);
                this.src = '/static/core/images/placeholder.jpg';
            };

            cardItem.appendChild(imgElement);
            galleryContainer.appendChild(cardItem);
        });
    } else {
        console.error('Gallery container not found or images not defined');
    }
});