export function generateRandomString(length) {
  let text = "";
  let possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
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
  let code = urlParams.get("code");
  let [, clientId, redirectUri] = urlParams.get("state").split(",");

  return {
    code,
    clientId,
    redirectUri,
  };
}

export function populateStateValue(redirectUri) {
  return function () {
    const clientId = document.getElementById("client_id").value;
    const state = [generateRandomString(16), clientId, redirectUri];

    document.getElementById("state").value = state;
  };
}
