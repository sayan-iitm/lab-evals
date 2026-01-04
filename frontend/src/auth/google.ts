// Google Sign-In using Google Identity Services (ID token flow)
// Google renders the button and returns id_token via callback

type GoogleCredentialResponse = {
  credential: string
  select_by?: string
}

export function initGoogleSignIn(onSuccess: (idToken: string) => void) {
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

  // @ts-expect-error GIS global
  if (!globalThis.google?.accounts?.id) {
    throw new Error('Google Identity Services SDK not loaded')
  }

  // @ts-expect-error GIS global
  globalThis.google.accounts.id.initialize({
    client_id: clientId,
    auto_select: false,
    callback: (response: GoogleCredentialResponse) => {
      if (response.credential) {
        onSuccess(response.credential)
      }
    },
  })

  // @ts-expect-error GIS global
  globalThis.google.accounts.id.renderButton(document.getElementById('google-signin-btn'), {
    theme: 'outline',
    size: 'large',
    width: 280,
  })
}
