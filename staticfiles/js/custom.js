(function ($) {
	"use strict";
  
	// ===============================
	// Carruseles (Men, Women, Kids del template original)
	// ===============================
	$(".owl-men-item, .owl-women-item, .owl-kid-item").owlCarousel({
	  items: 4,
	  loop: true,
	  dots: true,
	  nav: true,
	  margin: 20,
	  autoplay: true,
	  autoplayTimeout: 4000,
	  responsive: {
		0: { items: 1 },
		576: { items: 2 },
		768: { items: 3 },
		992: { items: 4 }
	  }
	});

	// ===============================
	// Carruseles de productos destacados (NUEVO)
	// ===============================
	$(".men-item-carousel, .women-item-carousel, .kids-item-carousel, .accessories-item-carousel").owlCarousel({
	  items: 4,
	  loop: true,
	  dots: true,
	  nav: true,
	  margin: 20,
	  autoplay: true,
	  autoplayTimeout: 4000,
	  responsive: {
		0: { items: 1 },
		576: { items: 2 },
		768: { items: 3 },
		992: { items: 4 }
	  }
	});
  
	// === Color dinámico del header según el scroll ===
	// === Header color fix para páginas con y sin banner ===
	$(window).scroll(function () {
	var scroll = $(window).scrollTop();
	var topSection = $("#top");

	if (topSection.length) {
		var box = topSection.height();
		var header = $("header").height();

		if (scroll >= box - header) {
		$("header").addClass("background-header");
		} else {
		$("header").removeClass("background-header");
		}
	} else {
		$("header").addClass("background-header");
	}
	});  
	// ===============================
	// Menú responsive
	// ===============================
	if ($(".menu-trigger").length) {
	  $(".menu-trigger").on("click", function () {
		$(this).toggleClass("active");
		$(".header-area .nav").slideToggle(200);
	  });
	}
  
	// ===============================
	// Scroll suave SOLO para anclas internas (#)
	// ===============================
	$('a[href^="#"]').on("click", function (e) {
	  e.preventDefault();
	  var target = $($(this).attr("href"));
	  if (target.length) {
		$("html, body").animate(
		  { scrollTop: target.offset().top - 80 },
		  600
		);
	  }
	});
  
	// ===============================
	// Scroll animation init
	// ===============================
	if (typeof scrollReveal !== "undefined") {
	  window.sr = new scrollReveal();
	}
  
	// ===============================
	// Page loading animation
	// ===============================
	$(window).on("load", function () {
	  if ($(".cover").length) {
		$(".cover").parallax({
		  imageSrc: $(".cover").data("image"),
		  zIndex: "1"
		});
	  }
  
	  if ($("#preloader").length) {
		$("#preloader").animate({ opacity: "0" }, 600, function () {
		  setTimeout(function () {
			$("#preloader").css("visibility", "hidden").fadeOut();
		  }, 300);
		});
	  }
	});
  
	// ===============================
	// Submenú en dispositivos móviles
	// ===============================
	function mobileNav() {
	  var width = $(window).width();
	  $(".submenu").on("click", function () {
		if (width < 767) {
		  $(".submenu ul").removeClass("active");
		  $(this).find("ul").toggleClass("active");
		}
	  });
	}
	mobileNav();
  
	$(window).on("resize", function () {
	  mobileNav();
	});
  
})(window.jQuery);
// === BUSCADOR GLOBAL AJAX (navbar) ===
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("navbarSearch");
  const resultsDiv = document.getElementById("navbarSearchResults");
  let searchTimer;

  if (!searchInput) return;

  searchInput.addEventListener("input", function () {
    clearTimeout(searchTimer);
    const query = this.value.trim();

    if (query.length < 2) {
      resultsDiv.style.display = "none";
      return;
    }

    searchTimer = setTimeout(() => {
      fetch(`/productos/buscar-live/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          resultsDiv.innerHTML = data.html;
          resultsDiv.style.display = "block";
        });
    }, 250);
  });

  // Ocultar resultados al hacer clic fuera
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".search-bar")) {
      resultsDiv.style.display = "none";
    }
  });
});
