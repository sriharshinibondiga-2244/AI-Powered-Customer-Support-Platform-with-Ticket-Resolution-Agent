// =========================================
// SUPPORT AI DASHBOARD
// =========================================

document.addEventListener("DOMContentLoaded", () => {

    const ticketForm = document.getElementById("ticketForm");

    // Close RAG modal
    const closeButton = document.getElementById("closeRagModal");

    if (closeButton) {
        closeButton.addEventListener("click", closeRAGModal);
    }

    const overlay = document.querySelector(".rag-modal-overlay");

    if (overlay) {
        overlay.addEventListener("click", closeRAGModal);
    }

    // Ticket submission
    if (ticketForm) {

        ticketForm.addEventListener("submit", async function (event) {

            event.preventDefault();

            const customerName =
                document.getElementById("customerName").value.trim();

            const query =
                document.getElementById("query").value.trim();

            const department =
                document.getElementById("department").value.trim();


            if (!customerName || !query) {

                alert("Please enter customer name and problem.");

                return;
            }


            // -----------------------------------------
            // OPEN RAG MODAL
            // -----------------------------------------

            openRAGModal();


            try {

                // -----------------------------------------
                // SEND TICKET TO FLASK
                // -----------------------------------------

                const response = await fetch("/submit", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        customer_name: customerName,

                        query: query,

                        department: department

                    })

                });


                const result = await response.json();


                if (!response.ok || !result.success) {

                    throw new Error(
                        result.message ||
                        "Ticket submission failed."
                    );

                }


                // -----------------------------------------
                // ACTIVATE RAG PIPELINE
                // -----------------------------------------

                activateRAGStages();


                // -----------------------------------------
                // DISPLAY RAG RESULT
                // -----------------------------------------

                setTimeout(() => {

                    displayRAGResult(result);

                }, 2200);


                // -----------------------------------------
                // CLEAR FORM
                // -----------------------------------------

                ticketForm.reset();


                // -----------------------------------------
                // UPDATE TICKETS
                // -----------------------------------------

                loadTickets();


            } catch (error) {

                console.error(error);

                closeRAGModal();

                alert(
                    "Unable to create ticket. " +
                    error.message
                );

            }

        });

    }


    // Load existing tickets when dashboard opens
    loadTickets();

});


// =========================================
// OPEN RAG MODAL
// =========================================

function openRAGModal() {

    const modal =
        document.getElementById("ragModal");

    const loading =
        document.getElementById("ragLoading");

    const result =
        document.getElementById("ragResult");


    if (!modal) return;


    modal.classList.add("active");


    if (loading) {

        loading.style.display = "block";

    }


    if (result) {

        result.innerHTML = "";

    }


    resetRAGStages();

}


// =========================================
// CLOSE RAG MODAL
// =========================================

function closeRAGModal() {

    const modal =
        document.getElementById("ragModal");

    if (modal) {

        modal.classList.remove("active");

    }

}


// =========================================
// RESET RAG STAGES
// =========================================

function resetRAGStages() {

    for (let i = 1; i <= 4; i++) {

        const stage =
            document.getElementById(
                "ragStage" + i
            );

        if (stage) {

            stage.classList.remove("active");

        }

    }

}


// =========================================
// ACTIVATE RAG PIPELINE
// =========================================

function activateRAGStages() {

    for (let i = 1; i <= 4; i++) {

        const stage =
            document.getElementById(
                "ragStage" + i
            );

        if (stage) {

            setTimeout(() => {

                stage.classList.add("active");

            }, (i - 1) * 500);

        }

    }

}


// =========================================
// DISPLAY RAG RESULT
// =========================================

function displayRAGResult(result) {

    const loading =
        document.getElementById("ragLoading");

    const container =
        document.getElementById("ragResult");


    const rag =
        result.rag || {};


    const documents =
        rag.retrieved_documents || [];


    // Hide loading animation

    if (loading) {

        loading.style.display = "none";

    }


    // -----------------------------------------
    // KNOWLEDGE ARTICLES
    // -----------------------------------------

    let knowledgeHTML = "";


    if (documents.length === 0) {

        knowledgeHTML = `
            <p>
                No relevant knowledge articles found.
            </p>
        `;

    } else {

        documents.forEach((doc, index) => {

            knowledgeHTML += `

                <div class="knowledge-item">

                    <strong>

                        ${index + 1}.
                        ${escapeHTML(
                            doc.title ||
                            "Knowledge Article"
                        )}

                    </strong>

                    <small>

                        ${escapeHTML(
                            doc.category ||
                            "Support"
                        )}

                    </small>

                </div>

            `;

        });

    }


    // -----------------------------------------
    // RESULT HTML
    // -----------------------------------------

    container.innerHTML = `

        <div class="rag-analysis">

            <div class="rag-metric">

                <label>
                    TICKET ID
                </label>

                <strong>
                    ${escapeHTML(
                        result.ticket_id || ""
                    )}
                </strong>

            </div>


            <div class="rag-metric">

                <label>
                    CATEGORY
                </label>

                <strong>
                    ${escapeHTML(
                        result.category || ""
                    )}
                </strong>

            </div>


            <div class="rag-metric">

                <label>
                    PRIORITY
                </label>

                <strong>
                    ${escapeHTML(
                        result.priority || ""
                    )}
                </strong>

            </div>


            <div class="rag-metric">

                <label>
                    AI CONFIDENCE
                </label>

                <strong>
                    ${rag.confidence || 0}%
                </strong>

            </div>

        </div>


        <div class="rag-content-grid">


            <!-- KNOWLEDGE RETRIEVAL -->

            <div class="rag-box">

                <h4>
                    KNOWLEDGE BASE RETRIEVAL
                </h4>

                ${knowledgeHTML}

            </div>


            <!-- CONTEXT -->

            <div class="rag-box">

                <h4>
                    CONTEXT AUGMENTATION
                </h4>

                <p>

                    ${escapeHTML(
                        rag.context ||
                        "No context available."
                    )}

                </p>

            </div>

        </div>


        <!-- FINAL RESOLUTION -->

        <div class="final-resolution">

            <h4>
                ✦ FINAL AI RESOLUTION
            </h4>


            <p>

                ${escapeHTML(
                    result.resolution ||
                    "No resolution generated."
                )}

            </p>


            <p style="margin-top:15px;">

                <strong>
                    Escalation:
                </strong>

                ${escapeHTML(
                    result.escalation ||
                    "Handled by AI"
                )}

            </p>

        </div>

    `;

}


// =========================================
// LOAD TICKETS
// =========================================

async function loadTickets() {

    try {

        const response =
            await fetch("/tickets");


        const tickets =
            await response.json();


        const ticketList =
            document.getElementById(
                "ticketList"
            );


        if (!ticketList) return;


        ticketList.innerHTML = "";


        // Update statistics

        const total =
            tickets.length;


        const high =
            tickets.filter(ticket =>
                ticket.priority === "High" ||
                ticket.priority === "Critical"
            ).length;


        const ai =
            tickets.filter(ticket =>
                ticket.escalation === "Handled by AI"
            ).length;


        const escalated =
            tickets.filter(ticket =>
                ticket.escalation ===
                "Escalated to Human Agent"
            ).length;


        updateElement(
            "totalTickets",
            total
        );


        updateElement(
            "highTickets",
            high
        );


        updateElement(
            "aiTickets",
            ai
        );


        updateElement(
            "escalatedTickets",
            escalated
        );


        // -----------------------------------------
        // DISPLAY TICKETS
        // -----------------------------------------

        tickets.forEach(ticket => {

            const card =
                document.createElement("div");


            card.className =
                "ticket-card";


            card.innerHTML = `

                <div>

                    <strong>
                        ${escapeHTML(
                            ticket.ticket_id || ""
                        )}
                    </strong>

                    <p>
                        ${escapeHTML(
                            ticket.customer_name || ""
                        )}
                    </p>

                </div>


                <div>

                    <span>
                        ${escapeHTML(
                            ticket.category || ""
                        )}
                    </span>

                </div>


                <div>

                    <strong>
                        ${escapeHTML(
                            ticket.priority || ""
                        )}
                    </strong>

                </div>


                <div>

                    <p>
                        ${escapeHTML(
                            ticket.query || ""
                        )}
                    </p>

                </div>


                <div>

                    <button
                        onclick="sendFeedback(
                            '${escapeHTML(
                                ticket.ticket_id
                            )}',
                            'Helpful'
                        )">

                        👍

                    </button>


                    <button
                        onclick="sendFeedback(
                            '${escapeHTML(
                                ticket.ticket_id
                            )}',
                            'Not Helpful'
                        )">

                        👎

                    </button>

                </div>

            `;


            ticketList.appendChild(card);

        });


    } catch (error) {

        console.error(
            "Error loading tickets:",
            error
        );

    }

}


// =========================================
// FEEDBACK
// =========================================

async function sendFeedback(
    ticketId,
    feedback
) {

    try {

        const response =
            await fetch(
                `/feedback/${ticketId}`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        feedback: feedback

                    })

                }
            );


        const result =
            await response.json();


        if (result.success) {

            alert(
                "Thank you for your feedback!"
            );

        }

    } catch (error) {

        console.error(error);

    }

}


// =========================================
// UPDATE ELEMENT
// =========================================

function updateElement(
    id,
    value
) {

    const element =
        document.getElementById(id);


    if (element) {

        element.textContent =
            value;

    }

}


// =========================================
// SECURITY
// =========================================

function escapeHTML(value) {

    if (value === null ||
        value === undefined) {

        return "";

    }


    return String(value)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");

}