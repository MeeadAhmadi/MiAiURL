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
    let targetUrl = input.value.trim();

    if (/^www\./i.test(targetUrl)) {
      targetUrl = `https://${targetUrl}`;
    }

    const response = await fetch("/links", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_url: targetUrl }),
    });

    if (response.status === 422) {
      result.textContent =
        "Enter a valid URL starting with www., http:// or https://.";
      return;
    }

    if (!response.ok) {
      result.textContent =
        "Could not create the short link. Please try again.";
      return;
    }

    const { code } = await response.json();
    const shortUrl = new URL(
      `/${encodeURIComponent(code)}`,
      window.location.origin
    ).href;

    const link = document.createElement("a");
    link.href = shortUrl;
    link.textContent = shortUrl;

    const copyButton = document.createElement("button");
    copyButton.type = "button";
    copyButton.textContent = "Copy";
    copyButton.setAttribute("aria-label", "Copy short link");
    copyButton.style.marginInlineStart = "12px";

    const copyStatus = document.createElement("span");

    copyButton.addEventListener("click", async () => {
      copyButton.disabled = true;
      copyStatus.textContent = "";

      try {
        await navigator.clipboard.writeText(shortUrl);
        copyButton.textContent = "Copied!";
      } catch {
        copyButton.textContent = "Copy";
        copyStatus.textContent =
          " Copy failed. Select the link and copy it manually.";
      } finally {
        copyButton.disabled = false;
      }
    });

    result.replaceChildren(
      "Your short link: ",
      link,
      copyButton,
      copyStatus
    );
  } catch (error) {
    console.error("Shorten request failed:", error);
    result.textContent =
      "Could not create the short link. Check your connection and try again.";
  } finally {
    button.disabled = false;
  }
});