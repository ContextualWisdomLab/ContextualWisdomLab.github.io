// 🛡️ Sentinel: Create a default Trusted Types policy to prevent DOM-based XSS when assigning to sinks like innerHTML.
// We use DOMPurify to sanitize the input before it's assigned to a sink.
if (window.trustedTypes && trustedTypes.createPolicy) {
  trustedTypes.createPolicy('default', {
    createHTML: (string) => DOMPurify.sanitize(string, {RETURN_TRUSTED_TYPE: true})
  });
}
