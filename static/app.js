const form = document.getElementById("shorten-form");
const input = document.getElementById("target-url");
const result = document.getElementById("shorten-result");
const button = form.querySelector('button[type="submit"]');

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (button.disabled) return;

  button.disabled = true;
  result.textContent = "Creating your short link…";

  try {
    const response = await fetch("/links", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_url: input.value.trim() }),
    });

    if (response.status === 422) {
      result.textContent = "Enter a valid URL starting with http:// or https://.";
      return;
    }

    if (!response.ok) {
      result.textContent = "Could not create the short link. Please try again.";
      return;
    }

    const { code } = await response.json();
    const link = document.createElement("a");
    link.href = new URL(`/${encodeURIComponent(code)}`, window.location.origin).href;
    link.textContent = link.href;
    result.replaceChildren("Your short link: ", link);
  } catch {
    result.textContent = "Could not reach the server. Please try again.";
  } finally {
    button.disabled = false;
  }
});