// Phone menu: the hamburger in the floating nav opens and closes the links.
document.querySelectorAll(".menu-btn").forEach((btn) => {
  const bar = btn.closest(".pillbar");
  const setOpen = (open) => {
    bar.classList.toggle("is-open", open);
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "Close menu" : "Menu");
  };
  btn.addEventListener("click", () => setOpen(!bar.classList.contains("is-open")));
  bar.querySelectorAll(".pill-menu a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
  document.addEventListener("click", (e) => { if (!bar.contains(e.target)) setOpen(false); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { setOpen(false); btn.focus(); } });
});
