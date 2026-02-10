if (window.innerWidth > 768) {
  const canvas = document.createElement("canvas");
  document.body.prepend(canvas);

  canvas.style.position = "absolute";
  canvas.style.top = "0";
  canvas.style.left = "0";
  canvas.style.pointerEvents = "none";
  canvas.style.zIndex = "0";

  const ctx = canvas.getContext("2d");

  function getFullHeight() {
    return Math.max(
      document.body.scrollHeight,
      document.documentElement.scrollHeight,
      document.body.offsetHeight,
      document.documentElement.offsetHeight,
      document.documentElement.clientHeight
    );
  }

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = getFullHeight();
  }

  resize();
  window.addEventListener("resize", resize);

  /* ---------- STARS ---------- */
  let stars = [];

  function generateStars() {
    stars = Array.from({ length: 160 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.5 + 0.3,
      a: Math.random()
    }));
  }

  generateStars();

  /* ---------- WAVES ---------- */
  let waves = [];

  document.addEventListener("mousemove", e => {
    waves.push({
      x: e.clientX,
      y: e.clientY + window.scrollY,
      radius: 0,
      alpha: 0.25
    });
  });

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // stars
    stars.forEach(s => {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(147,197,253,${s.a})`;
      ctx.fill();
    });

    // waves
    waves.forEach(w => {
      w.radius += 1.5;
      w.alpha -= 0.003;

      ctx.beginPath();
      ctx.arc(w.x, w.y, w.radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(30,58,138,${w.alpha})`;
      ctx.lineWidth = 1.2;
      ctx.stroke();
    });

    waves = waves.filter(w => w.alpha > 0);
    requestAnimationFrame(animate);
  }

  animate();

  /* ---------- CRITICAL: RESIZE AFTER CONTENT LOAD ---------- */
  window.addEventListener("load", () => {
    resize();
    generateStars();
  });

  // ALSO re-run after dynamic content injection (result page)
  setTimeout(() => {
    resize();
    generateStars();
  }, 300);
}
