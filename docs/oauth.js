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

export function fetchWithErrorHandling(url, options, handleSuccess) {
  return fetch(url, options)
    .then((response) => {
      if (!response.ok) {
        throw new Error("HTTP status " + response.status);
      }
      return response.json();
    })
    .then(handleSuccess)
    .catch((error) => {
      console.error("Error:", error);
    });
}

export function parseCallbackParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");
  const [_nonce, ...passthruParams] = urlParams.get("state").split(",");

  return [code, ...passthruParams];
}

export function populateStateValue(...passthruParams) {
  return function () {
    const clientId = document.getElementById("client_id").value;
    const state = [generateRandomString(16), clientId, ...passthruParams];

    document.getElementById("state").value = state;
  };
}
