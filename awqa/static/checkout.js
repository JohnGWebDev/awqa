// This is your test secret API key.
const stripe = Stripe("pk_live_51OLwZJEwHN2N88WYIHtuP0uTDTN2ncBrBc8xHe4kpXEIhLHJ4FvZg5oIPCIfbw71jf7BQ8Lf6apm3RS270ZlSCi200sT25Z4Zl");
const body = document.body;
const hxheaders = body.getAttribute('hx-headers');
const colonIndex = hxheaders.indexOf(':');
const afterColon = hxheaders.slice(colonIndex + 1).trim();
const regex = /"(.*?)"/;
const match = afterColon.match(regex);
const csrftoken = match ? match[1] : null;
console.log(String(csrftoken))
const pk = document.getElementById("purchaseObject").value;
initialize();

// Create a Checkout Session
async function initialize() {
  const fetchClientSecret = async () => {
    const response = await fetch("/payments/create-checkout-session/" + pk + "/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": String(csrftoken), // Include CSRF token
    },
    });
    const { clientSecret } = await response.json();
    return clientSecret;
  };

  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}