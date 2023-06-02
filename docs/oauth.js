export function generateRandomString(length) {
  let text = "";
  let possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

export async function generateCodeChallenge(codeVerifier) {
  function base64encode(string) {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(string)))
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=+$/, "");
  }

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

export function parseCallbackParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");
  const state = urlParams.get("state");
  const { _nonce, ...passThruParams } = JSON.parse(atob(state));

  return {
    code,
    ...passThruParams,
  };
}

export function populateStateValue(passthruParams) {
  const clientId = document.getElementById("client_id").value;
  const state = {
    _nonce: generateRandomString(16),
    clientId,
    ...passthruParams,
  };

  document.getElementById("state").value = btoa(JSON.stringify(state));
}
