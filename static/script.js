
// const form = document.getElementById("question-form");
// const questionInput = document.getElementById("question");
// const askButton = form.querySelector("button");
// const statusText = document.getElementById("status");
// const answerSection = document.getElementById("answer-section");
// const answerText = document.getElementById("answer");
// const sourcesContainer = document.getElementById("sources");

// form.addEventListener("submit", async (event) => {
//     event.preventDefault();

//     const question = questionInput.value.trim();

//     if (!question) {
//         statusText.textContent = "Please enter a question.";
//         return;
//     }

//     askButton.disabled = true;
//     statusText.textContent =
//         "Searching the handbook and generating an answer...";
//     answerSection.hidden = true;
//     sourcesContainer.replaceChildren();

//     try {
//         const response = await fetch("/api/ask", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ question: question })
//         });

//         const result = await response.json();

//         if (!response.ok) {
//             throw new Error(
//                 result.error || "Unable to get an answer."
//             );
//         }

//         answerText.textContent = result.answer;
//         answerSection.hidden = false;

//         if (result.sources && result.sources.length > 0) {
//             result.sources.forEach((source) => {
//                 const sourceCard = document.createElement("div");
//                 sourceCard.className = "source";

//                 // Display the policy heading and page number.
//                 const pageTitle = document.createElement("strong");
//                 pageTitle.textContent =
//                     `${source.section || "Handbook section"} — Page ${source.page}`;

//                 // Display the source PDF filename.
//                 const fileName = document.createElement("p");
//                 const sourcePath = source.source || "Employee handbook";
//                 fileName.textContent =
//                     `Source: ${sourcePath.split(/[\\/]/).pop()}`;

//                 // Display the supporting handbook text.
//                 const sourceContent = document.createElement("p");
//                 sourceContent.textContent = source.text;

//                 sourceCard.append(
//                     pageTitle,
//                     fileName,
//                     sourceContent
//                 );

//                 sourcesContainer.appendChild(sourceCard);
//             });
//         } else {
//             sourcesContainer.textContent =
//                 "No sources were returned.";
//         }

//         statusText.textContent = "Answer generated successfully.";

//     } catch (error) {
//         statusText.textContent = error.message;
//     } finally {
//         askButton.disabled = false;
//     }
// });

const form = document.getElementById("question-form");
const questionInput = document.getElementById("question");
const askButton = form.querySelector("button");
const statusText = document.getElementById("status");
const answerSection = document.getElementById("answer-section");
const answerText = document.getElementById("answer");
const sourcesContainer = document.getElementById("sources");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) {
        statusText.textContent = "Please enter a question.";
        return;
    }

    askButton.disabled = true;
    statusText.textContent =
        "Searching the handbook and generating an answer...";
    answerSection.hidden = true;
    sourcesContainer.replaceChildren();

    try {
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.error || "Unable to get an answer."
            );
        }

        // Debug the actual response received from Flask.
        console.log("Full API response:", result);
        console.log("Answer received:", JSON.stringify(result.answer));
        console.log("Answer length:", result.answer?.length);

        // Display the complete answer returned by the backend.
        answerText.textContent =
            typeof result.answer === "string" && result.answer.trim()
                ? result.answer
                : "No answer was returned. Please try again.";

        answerSection.hidden = false;

        // Display supporting handbook sources.
        if (Array.isArray(result.sources) && result.sources.length > 0) {
            result.sources.forEach((source) => {
                const sourceCard = document.createElement("div");
                sourceCard.className = "source";

                const pageTitle = document.createElement("strong");
                pageTitle.textContent =
                    `${source.section || "Handbook section"} — Page ${source.page ?? "Unknown"}`;

                const fileName = document.createElement("p");
                const sourcePath =
                    source.source || "Employee handbook";

                fileName.textContent =
                    `Source: ${sourcePath.split(/[\\/]/).pop()}`;

                const sourceContent = document.createElement("p");
                sourceContent.textContent = source.text || "";

                sourceCard.append(
                    pageTitle,
                    fileName,
                    sourceContent
                );

                sourcesContainer.appendChild(sourceCard);
            });
        } else {
            sourcesContainer.textContent = "No sources were returned.";
        }

        statusText.textContent = "Answer generated successfully.";

    } catch (error) {
        console.error("Error asking handbook question:", error);
        statusText.textContent = error.message;
    } finally {
        askButton.disabled = false;
    }
});
