var timer
const timeeout = 5 * 60 * 1000

module.exports = () => {
  document.addEventListener("mouseup", () => {
    clearInterval(timer)
    timer = setInterval(activateScreensaver, timeeout)
  })

  timer = setInterval(activateScreensaver, timeeout)
}

function activateScreensaver() {
  window.location.href = "http://localhost/screensaver"
}