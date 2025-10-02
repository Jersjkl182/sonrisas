/* Partículas de fondo utilizando tsParticles */

tsParticles.load("particles-js", {
  fpsLimit: 60,
  background: { color: "transparent" },
  particles: {
    number: { value: 60, density: { enable: true, area: 800 } },
    color: { value: ["#ffffff", "#a777e3", "#6e8efb"] },
    shape: { type: "circle" },
    opacity: { value: 0.3, random: true },
    size: { value: 3, random: { enable: true, minimumValue: 1 } },
    links: { enable: true, distance: 150, color: "#ffffff", opacity: 0.1, width: 1 },
    move: { enable: true, speed: 1, direction: "none", outModes: { default: "out" } }
  },
  detectRetina: true
});
