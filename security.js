// 🛡️ Sentinel: Create a default Trusted Types policy to prevent DOM-based XSS when assigning to sinks like innerHTML.
// We use DOMPurify to sanitize the input before it's assigned to a sink.
if (window.trustedTypes && window.trustedTypes.createPolicy) {
  try {
    window.trustedTypes.createPolicy('default', {
      createHTML: (string) => {
        if (window.DOMPurify) {
          return window.DOMPurify.sanitize(string, { RETURN_TRUSTED_TYPE: true });
        }
        return '';
      }
    });
  } catch (e) {
    // Fail securely: ignore if policy already exists or if CSP restricts policy creation
  }
}
