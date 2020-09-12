const navSlide = () => {
    const resIcon = document.querySelector('.res-icon')
    const resOpt = document.querySelector('.res-links')
    const resLinks = document.querySelectorAll('.res-links li')

    resIcon.addEventListener('click', () => {

        // toggle view
    resOpt.classList.toggle('res-active')

    // link animations
    resLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = ''
      } else {
        link.style.animation = `resLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`
      }
    })

    // burger animation
    resIcon.classList.toggle('toggle')
  })
}

navSlide()

