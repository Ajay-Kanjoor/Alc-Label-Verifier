import { useState } from 'react'
import './App.css'

import { submitLabel } from "./api";

function App() {
  const [brandName, setBrandName] = useState("");
  const [productType, setProductType] = useState("");
  const [abv, setAbv] = useState("");
  const [netContents, setNetContents] = useState("");
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append("brand_name", brandName);
    data.append("product_type", productType);
    data.append("alcohol_content", abv);
    data.append("net_contents", netContents);
    data.append("image", image);

    const res = await submitLabel(data);
    setResult(res);
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px" }}>
      <h1>Alcohol Label Verification</h1>

      <form onSubmit={handleSubmit}>
        <label>Brand Name </label>
        <input value={brandName} onChange={(e) => setBrandName(e.target.value)} /><br/><br/>

        <label>Product Type </label>
        <input value={productType} onChange={(e) => setProductType(e.target.value)} /><br/><br/>

        <label>Alcohol Content (ABV) </label>
        <input value={abv} onChange={(e) => setAbv(e.target.value)} /><br/><br/>

        <label>Net Contents </label>
        <input value={netContents} onChange={(e) => setNetContents(e.target.value)} /><br/><br/>

        <label>Upload Label Image </label>
        <input type="file" onChange={(e) => setImage(e.target.files[0])} /><br/><br/>

        <button type="submit">Verify</button>
      </form>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>{result.success ? "✔ Match" : "✖ Mismatch"}</h3>
          <pre>{JSON.stringify(result.details, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App
