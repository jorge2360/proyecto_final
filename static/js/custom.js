(function ($) {
	"use strict";
  
	// ===============================
	// Carruseles (Men, Women, Kids)
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
	// Cambiar color de header al hacer scroll
	// ===============================
	$(window).scroll(function () {
	  var scroll = $(window).scrollTop();
	  var box = $("#top").height();
	  var header = $("header").height();
  
	  if (scroll >= box - header) {
		$("header").addClass("background-header");
	  } else {
		$("header").removeClass("background-header");
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
  