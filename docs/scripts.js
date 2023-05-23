// https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow

function generateRandomString(length) {
  let text = "";
  let possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

async function generateCodeChallenge(codeVerifier) {
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

export function redirectToLogin(clientId, redirectUri, scope) {
  let codeVerifier = generateRandomString(128);

  generateCodeChallenge(codeVerifier).then((codeChallenge) => {
    let state = [generateRandomString(16), clientId, redirectUri];

    localStorage.setItem("code_verifier", codeVerifier);

    let args = new URLSearchParams({
      response_type: "code",
      client_id: clientId,
      scope: scope,
      redirect_uri: redirectUri,
      state: state,
      code_challenge_method: "S256",
      code_challenge: codeChallenge,
    });

    window.location.assign("https://accounts.spotify.com/authorize?" + args);
  });
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

export function fetchToken(handleSuccess) {
  const urlParams = new URLSearchParams(window.location.search);
  let code = urlParams.get("code");
  let [, clientId, redirectUri] = urlParams.get("state").split(",");

  let codeVerifier = localStorage.getItem("code_verifier");

  let body = new URLSearchParams({
    grant_type: "authorization_code",
    code: code,
    redirect_uri: redirectUri,
    client_id: clientId,
    code_verifier: codeVerifier,
  });

  return fetchWithErrorHandling(
    "https://accounts.spotify.com/api/token",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: body,
    },
    handleSuccess
  );
}
