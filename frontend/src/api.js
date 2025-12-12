export async function submitLabel(formData) {
  const response = await fetch("http://localhost:8000/verify", {
    method: "POST",
    body: formData
  });

  return await response.json();
}