
document.getElementById("loanForm").addEventListener("submit", async function(event) {
  event.preventDefault();
  await predictLoan();
});

async function predictLoan() {
  const data = {
    gender: document.getElementById("gender").value,
    married: document.getElementById("married").value,
    income: document.getElementById("income").value,
    coapplicant_income: document.getElementById("coapplicant_income").value,
    loan_amount: document.getElementById("loan_amount").value,
    loan_term: document.getElementById("loan_term").value,
    credit_history: document.getElementById("credit_history").value,
    property_area: document.getElementById("property_area").value
  };

  const resultBox = document.getElementById("result");
  resultBox.innerHTML = "⏳ Checking eligibility...";

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    resultBox.innerHTML = `
      ✅ <strong>${result.result}</strong><br>
      📊 Approval Probability: <strong>${result.approval_probability}%</strong>
    `;
  } catch (error) {
    resultBox.innerHTML = "⚠️ Error connecting to the server.";
    console.error(error);
  }
}
