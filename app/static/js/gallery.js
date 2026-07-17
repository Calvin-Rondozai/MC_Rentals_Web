(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var mainImage = document.querySelector("[data-gallery-main]");
    var thumbs = document.querySelectorAll("[data-gallery-thumb]");
    var lightbox = document.querySelector("[data-lightbox]");
    var lightboxImage = lightbox ? lightbox.querySelector("[data-lightbox-image]") : null;
    var lightboxClose = lightbox ? lightbox.querySelector("[data-lightbox-close]") : null;
    var lightboxPrev = lightbox ? lightbox.querySelector("[data-lightbox-prev]") : null;
    var lightboxNext = lightbox ? lightbox.querySelector("[data-lightbox-next]") : null;

    if (!mainImage || !thumbs.length) return;

    var images = Array.prototype.map.call(thumbs, function (thumb) {
      return thumb.getAttribute("data-full");
    });
    var currentIndex = 0;

    function setActive(index) {
      currentIndex = (index + images.length) % images.length;
      mainImage.src = images[currentIndex];
      thumbs.forEach(function (thumb, i) {
        thumb.classList.toggle("is-active", i === currentIndex);
      });
    }

    thumbs.forEach(function (thumb, index) {
      thumb.addEventListener("click", function () {
        setActive(index);
      });
    });

    mainImage.addEventListener("click", function () {
      openLightbox(currentIndex);
    });

    function openLightbox(index) {
      if (!lightbox) return;
      setActive(index);
      lightboxImage.src = images[currentIndex];
      lightbox.setAttribute("data-open", "true");
      document.body.style.overflow = "hidden";
    }

    function closeLightbox() {
      if (!lightbox) return;
      lightbox.setAttribute("data-open", "false");
      document.body.style.overflow = "";
    }

    function showRelative(delta) {
      setActive(currentIndex + delta);
      if (lightboxImage) lightboxImage.src = images[currentIndex];
    }

    if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
    if (lightbox) {
      lightbox.querySelector(".overlay-backdrop").addEventListener("click", closeLightbox);
    }
    if (lightboxPrev) lightboxPrev.addEventListener("click", function () { showRelative(-1); });
    if (lightboxNext) lightboxNext.addEventListener("click", function () { showRelative(1); });

    document.addEventListener("keydown", function (e) {
      if (!lightbox || lightbox.getAttribute("data-open") !== "true") return;
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowLeft") showRelative(-1);
      if (e.key === "ArrowRight") showRelative(1);
    });
  });
})();
