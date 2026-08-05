const form = document.getElementById("chatForm");
const responseArea = document.getElementById("responseArea");
const button = document.getElementById("generateBtn");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const model = document.getElementById("model").value;
    const prompt = document.getElementById("prompt").value;

    if (prompt.trim() === "") {
        alert("Please enter a prompt.");
        return;
    }

    button.disabled = true;
    button.innerHTML = "⏳ Generating...";

    responseArea.innerHTML = `
        <div class="alert alert-info">
            Generating response...
        </div>
    `;

    const formData = new FormData();

    formData.append("model", model);
    formData.append("prompt", prompt);

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            body: formData

        });

        const data = await response.json();
        console.log(data);
        if (data.error) {

          responseArea.innerHTML = `
                <div class="alert alert-danger">
                   ${data.error}
                </div>
        `;

        } else {

            responseArea.innerHTML = `

            <div class="card mt-3 shadow">

                <div class="card-body">

                    <h5>🤖 Model</h5>

                    <p>${data.model}</p>

                    <hr>

                    <h5 class="d-flex justify-content-between align-items-center">

    💬 Response

    <button
        class="btn btn-sm btn-success"
        onclick="copyResponse()">

        📋 Copy

    </button>

</h5>

<div class="border rounded p-3 bg-light">

    <pre
        id="aiResponse"
        style="white-space: pre-wrap;">${data.response}</pre>

</div>

                    <br>

                    <div class="row">

                        <div class="col-md-4">

                            <strong>📥 Input Tokens</strong>

                            <p>${data.input_tokens}</p>

                        </div>

                        <div class="col-md-4">

                            <strong>📤 Output Tokens</strong>

                            <p>${data.output_tokens}</p>

                        </div>

                        <div class="col-md-4">

                            <strong>🧠 Thinking Tokens</strong>

                            <p>${data.thinking_tokens}</p>

                        </div>

                    </div>

                    <div class="row mt-3">

                        <div class="col-md-6">

                            <strong>Total Tokens</strong>

                            <p>${data.total_tokens}</p>

                        </div>

                        <div class="col-md-6">

                            <strong>Estimated Cost</strong>

                            <p>${data.estimated_cost}</p>

                        </div>

                    </div>

                </div>

            </div>

            `;
        }

    } catch (error) {

        responseArea.innerHTML = `
            <div class="alert alert-danger">
                Something went wrong.
            </div>
        `;

    }

    button.disabled = false;
    button.innerHTML = "Generate";

});
function copyResponse() {

    const text = document.getElementById("aiResponse").innerText;

    navigator.clipboard.writeText(text);

    alert("✅ Response copied successfully!");

}