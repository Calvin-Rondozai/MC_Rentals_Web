(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var input = document.querySelector("[data-image-input]");
    var preview = document.querySelector("[data-image-preview]");
    var dropzone = document.querySelector("[data-dropzone]");

    if (input && preview) {
      input.addEventListener("change", function () {
        preview.innerHTML = "";
        Array.prototype.forEach.call(input.files, function (file) {
          if (!file.type.startsWith("image/")) return;
          var reader = new FileReader();
          reader.onload = function (e) {
            var wrap = document.createElement("div");
            wrap.className = "image-preview-thumb";
            var img = document.createElement("img");
            img.src = e.target.result;
            img.alt = file.name;
            wrap.appendChild(img);
            preview.appendChild(wrap);
          };
          reader.readAsDataURL(file);
        });
      });
    }

    if (dropzone && input) {
      ["dragenter", "dragover"].forEach(function (evt) {
        dropzone.addEventListener(evt, function (e) {
          e.preventDefault();
          dropzone.classList.add("is-dragover");
        });
      });
      ["dragleave", "drop"].forEach(function (evt) {
        dropzone.addEventListener(evt, function (e) {
          e.preventDefault();
          dropzone.classList.remove("is-dragover");
        });
      });
      dropzone.addEventListener("drop", function (e) {
        var files = e.dataTransfer.files;
        if (files && files.length) {
          input.files = files;
          input.dispatchEvent(new Event("change"));
        }
      });
      dropzone.addEventListener("click", function () {
        input.click();
      });
    }

    /* Range/number price filter sync on listings page, if present */
    var minPrice = document.querySelector("[data-min-price]");
    var maxPrice = document.querySelector("[data-max-price]");
    if (minPrice && maxPrice) {
      minPrice.addEventListener("change", function () {
        if (maxPrice.value && Number(minPrice.value) > Number(maxPrice.value)) {
          maxPrice.value = minPrice.value;
        }
      });
    }
  });
})();
