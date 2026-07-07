// 🛡️ Sentinel: Create a default Trusted Types policy to prevent DOM-based XSS when assigning to sinks like innerHTML.
// We use DOMPurify to sanitize the input before it's assigned to a sink.
if (window.trustedTypes && window.trustedTypes.createPolicy) {
  try {
    window.trustedTypes.createPolicy('default', {
      createHTML: (string) =>
        window.DOMPurify
          ? window.DOMPurify.sanitize(string, { RETURN_TRUSTED_TYPE: true })
          : string
    });
  } catch (e) {
    // Creating the default policy can throw (e.g. a 'default' policy already exists,
    // or CSP disallows it). Swallow the error so the page still loads.
    console.warn('Trusted Types default policy creation failed:', e);
  }
}
