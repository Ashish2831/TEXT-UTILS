anime
  .timeline({ loop: true })
  .add({
    targets: ".ml8 .circle-white",
    scale: [0, 3],
    opacity: [1, 0],
    easing: "easeInOutExpo",
    rotateZ: 360,
    duration: 1500,
  })
  .add({
    targets: ".ml8 .circle-container",
    scale: [0, 1],
    duration: 1500,
    easing: "easeInOutExpo",
    offset: "-=1000",
  })
  .add({
    targets: ".ml8 .circle-dark",
    scale: [0, 1],
    duration: 1500,
    easing: "easeOutExpo",
    offset: "-=600",
  })
  .add({
    targets: ".ml8 .letters-left",
    scale: [0, 1],
    duration: 1600,
    offset: "-=550",
  })
  .add({
    targets: ".ml8 .bang",
    scale: [0, 1],
    duration: 1600,
    offset: "-=1000",
  })
  .add({
    targets: ".ml8",
    opacity: 0,
    duration: 1400,
    easing: "easeOutExpo",
    delay: 1400,
  });

anime({
  targets: ".ml8 .circle-dark-dashed",
  rotateZ: 360,
  duration: 8000,
  easing: "linear",
  loop: true,
});
SourceTHU;
