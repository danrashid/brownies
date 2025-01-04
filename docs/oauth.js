export function generateRandomString(length) {
  let text = "";
  let possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

function base64encode(string) {
  return btoa(String.fromCharCode.apply(null, new Uint8Array(string)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

export async function generateCodeChallenge(codeVerifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await window.crypto.subtle.digest("SHA-256", data);

  return base64encode(digest);
}

export async function fetchWithErrorHandling(url, options) {
  try {
    const response = await fetch(url, options);
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("HTTP status " + response.status);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function setElementValue(id, value) {
  const el = document.getElementById(id);

  if (el !== null) {
    el.value = value;
  }
}

export function handleQueryStringParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const ret = {};

  if (urlParams.size > 0) {
    for (const [key, value] of urlParams.entries()) {
      if (key === "state") {
        const state = JSON.parse(atob(value));

        Object.entries(state)
          .filter(([key]) => key !== "_nonce")
          .forEach(([key, value]) => {
            setElementValue(key, value);
            ret[key] = value;
          });
      } else {
        setElementValue(key, value);
        ret[key] = value;
      }
    }
  }

  return ret;
}

export function encodeStateValue(passthruParams) {
  return btoa(
    JSON.stringify({
      _nonce: generateRandomString(16),
      ...passthruParams,
    })
  );
}
