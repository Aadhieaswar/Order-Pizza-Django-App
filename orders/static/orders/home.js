var slideIndex = 0;
showSlides();

function showSlides() {
  var slides = document.getElementsByClassName('slides');
  var dots = document.getElementsByClassName('dot');
  for (var i = 0; i < slides.length; i++) {
    slides[i].style.display = 'none';
    const arr = [...dots[i].classList]
    if (arr.includes('active')) {
      dots[i].classList.toggle('active');
    }
  }
  slideIndex++;
  if (slideIndex > slides.length) {
    slideIndex = 1
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].classList.toggle('active')
  setTimeout(showSlides, 2000); // Change image every 2 seconds
}
