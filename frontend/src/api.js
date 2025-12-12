export async function submitLabel(formData) {
  const response = await fetch("https://alc-label-verifier.onrender.com", {
    method: "POST",
    body: formData
  });

  return await response.json();
}