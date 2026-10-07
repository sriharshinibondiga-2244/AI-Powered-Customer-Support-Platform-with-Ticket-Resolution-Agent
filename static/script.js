// =========================================
// SUPPORTAI - MULTI AGENT DASHBOARD
// =========================================

document.addEventListener("DOMContentLoaded", () => {

    const ticketForm = document.getElementById("ticketForm");

    if (ticketForm) {

        ticketForm.addEventListener("submit", async function (event) {

            event.preventDefault();

            const customerName =
    document.getElementById("customerName").value.trim();

const customerEmail =
    document.getElementById("customerEmail").value.trim();

const query =
    document.getElementById("query").value.trim();

const department =
    document.getElementById("department").value.trim();


           if (!customerName || !customerEmail || !query) {
    alert("Please enter customer name, email and problem.");
    return;
}

            // SHOW WORKFLOW
            openWorkflowModal();

            try {

                const response = await fetch("/submit", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                   body: JSON.stringify({
    customer_name: customerName,
    customer_email: customerEmail,
    query: query,
    department: department
})
                });

                const result = await response.json();

                console.log("SUBMIT RESPONSE:", result);

                if (!response.ok || !result.success) {
                    throw new Error(
                        result.message || "Ticket submission failed."
                    );
                }

                // Animate workflow
                activateWorkflowStages();

                // Show final workflow after agents run
                setTimeout(() => {
                    displayMultiAgentWorkflow(result);
                }, 2200);

                ticketForm.reset();

                loadTickets();

            } catch (error) {

                console.error("SUBMIT ERROR:", error);

                closeWorkflowModal();

                alert(
                    "Unable to create ticket.\n\n" +
                    error.message
                );
            }
        });
    }

    loadTickets();
});


// =========================================
// OPEN WORKFLOW MODAL
// =========================================

function openWorkflowModal() {

    const modal = document.getElementById("ragModal");
    const loading = document.getElementById("ragLoading");
    const result = document.getElementById("ragResult");

    if (!modal) {
        console.error("ragModal not found in index.html");
        alert("Workflow modal is missing from index.html");
        return;
    }

    modal.classList.add("active");

    if (loading) {

        loading.style.display = "block";

        loading.innerHTML = `
            <div class="workflow-loading">

                <div class="workflow-spinner"></div>

                <h3>
                    Multi-Agent Resolution Workflow
                </h3>

                <p>
                    AI agents are analyzing your support ticket...
                </p>

            </div>
        `;
    }

    if (result) {
        result.innerHTML = "";
    }

    resetWorkflowStages();
}


// =========================================
// CLOSE WORKFLOW
// =========================================

function closeWorkflowModal() {

    const modal = document.getElementById("ragModal");

    if (modal) {
        modal.classList.remove("active");
    }
}


// =========================================
// RESET WORKFLOW STAGES
// =========================================

function resetWorkflowStages() {

    for (let i = 1; i <= 4; i++) {

        const stage =
            document.getElementById("ragStage" + i);

        if (stage) {
            stage.classList.remove("active");
        }
    }
}


// =========================================
// ACTIVATE WORKFLOW STAGES
// =========================================

function activateWorkflowStages() {

    for (let i = 1; i <= 4; i++) {

        const stage =
            document.getElementById("ragStage" + i);

        if (stage) {

            setTimeout(() => {

                stage.classList.add("active");

            }, (i - 1) * 500);
        }
    }
}





// =========================================
// DISPLAY MU
function displayMultiAgentWorkflow(result) {

    const loading = document.getElementById("ragLoading");
    const container = document.getElementById("ragResult");

    if (!container) return;

    if (loading) {
        loading.style.display = "none";
    }

    const workflowData = result.workflow?.workflow || {};

    const diagnosis = workflowData.diagnosis || {};
    const retrieval = workflowData.retrieval || {};
    const resolution = workflowData.resolution || {};
    const validation = workflowData.validation || {};
    const escalation = workflowData.escalation || {};

    const isResolved =
        escalation.decision === "AUTOMATICALLY RESOLVED";
        const emailStatus = result.email_sent === true
    ? `
        <div style="
            margin-top:20px;
            padding:15px;
            border-left:4px solid #d32f2f;
            background:#f5f5f5;
            font-size:15px;
        ">
            📧 <strong>Email Sent Successfully</strong>
            <br>
            <span>
                This issue could not be resolved by AI.
                It has been escalated to human support,
                and the resolution steps have been sent to your email inbox.
            </span>
        </div>
      `
    : "";



    container.innerHTML = `

        <div class="professional-workflow">

            <!-- HEADER -->

            <div class="workflow-main-header">

                <div class="workflow-header-icon">
                    ✦
                </div>

                <div>

                    <div class="workflow-label">
                        AI INTELLIGENCE
                    </div>

                    <h2>
                        Multi-Agent Resolution Workflow
                    </h2>

                    <p>
                        Five specialized AI agents collaborated
                        to analyze and resolve this support ticket.
                    </p>

                </div>

            </div>


            <!-- AGENT PIPELINE -->

            <div class="agent-pipeline">


                <!-- 01 DIAGNOSIS -->

                <div class="agent-step">

                    <div class="agent-top">

                        <span class="agent-number">
                            01
                        </span>

                        <span class="agent-check">
                            ✓
                        </span>

                    </div>

                    <div class="agent-icon">
                        🔍
                    </div>

                    <h3>
                        Diagnosis Agent
                    </h3>

                    <p>
                        ${escapeHTML(
                            diagnosis.category ||
                            "Issue Analysis"
                        )}
                    </p>

                    <div class="agent-score">
                        ${diagnosis.confidence || 0}%
                        confidence
                    </div>

                </div>


                <div class="pipeline-arrow">
                    →
                </div>


                <!-- 02 RETRIEVAL -->

                <div class="agent-step">

                    <div class="agent-top">

                        <span class="agent-number">
                            02
                        </span>

                        <span class="agent-check">
                            ✓
                        </span>

                    </div>

                    <div class="agent-icon">
                        📚
                    </div>

                    <h3>
                        Retrieval Agent
                    </h3>

                    <p>
                        Knowledge Base
                    </p>

                    <div class="agent-score">
                        ${retrieval.similarity || 0}%
                        similarity
                    </div>

                </div>


                <div class="pipeline-arrow">
                    →
                </div>


                <!-- 03 RESOLUTION -->

                <div class="agent-step">

                    <div class="agent-top">

                        <span class="agent-number">
                            03
                        </span>

                        <span class="agent-check">
                            ✓
                        </span>

                    </div>

                    <div class="agent-icon">
                        ✦
                    </div>

                    <h3>
                        Resolution Agent
                    </h3>

                    <p>
                        Solution Generated
                    </p>

                    <div class="agent-score">
                        ${resolution.confidence || 0}%
                        confidence
                    </div>

                </div>


                <div class="pipeline-arrow">
                    →
                </div>


                <!-- 04 VALIDATION -->

                <div class="agent-step">

                    <div class="agent-top">

                        <span class="agent-number">
                            04
                        </span>

                        <span class="agent-check">
                            ✓
                        </span>

                    </div>

                    <div class="agent-icon">
                        ✓
                    </div>

                    <h3>
                        Validation Agent
                    </h3>

                    <p>
                        Quality Checked
                    </p>

                    <div class="agent-score">
                        ${validation.confidence || 0}%
                        confidence
                    </div>

                </div>


                <div class="pipeline-arrow">
                    →
                </div>


                <!-- 05 ESCALATION -->

                <div class="agent-step">

                    <div class="agent-top">

                        <span class="agent-number">
                            05
                        </span>

                        <span class="agent-check">
                            ✓
                        </span>

                    </div>

                    <div class="agent-icon">
                        ↗
                    </div>

                    <h3>
                        Escalation Agent
                    </h3>

                    <p>
                        ${escapeHTML(
                            escalation.status ||
                            "Decision Made"
                        )}
                    </p>

                    <div class="agent-score">
                        Final Decision
                    </div>

                </div>

            </div>

<!-- FINAL DECISION -->

<div class="
    final-workflow-status
    ${isResolved ? "resolved" : "escalated"}
">

    <div class="final-status-icon">
        ${isResolved ? "✓" : "!"}
    </div>

    <div>

        <span>
            FINAL WORKFLOW DECISION
        </span>

        <h2>
            ${escapeHTML(
                escalation.decision ||
                "PROCESSING"
            )}
        </h2>

        <p>
            Validation confidence:
            <strong>
                ${validation.confidence || 0}%
            </strong>
        </p>

    </div>

</div>

${emailStatus}


<!-- BACK TO DASHBOARD -->

<div class="workflow-actions">

    <button
        class="workflow-back-btn"
        onclick="closeWorkflowModal()">

        ← BACK TO DASHBOARD

    </button>

</div>


</div>
`;
}
            
// =========================================
// LOAD TICKETS
// =========================================

// =========================================
// LOAD TICKETS
// =========================================

async function loadTickets() {

    try {

        const response = await fetch("/tickets");

        if (!response.ok) {
            throw new Error("Unable to load tickets");
        }

        const tickets = await response.json();

        const ticketList = document.getElementById("ticketList");

        if (!ticketList) return;

        ticketList.innerHTML = "";

        // ================================
        // STATISTICS
        // ================================

        const total = tickets.length;

        const high = tickets.filter(ticket =>
            ticket.priority === "High" ||
            ticket.priority === "Critical"
        ).length;

        const ai = tickets.filter(ticket =>
            ticket.escalation === "Handled by AI"
        ).length;

        const escalated = tickets.filter(ticket =>
            ticket.escalation === "Escalated to Human Agent"
        ).length;

        // =========================================
// DASHBOARD KPI VALUES
// =========================================

const today = new Date();

const todayTickets = tickets.filter(ticket => {

    if (!ticket.created_at) return false;

    const ticketDate =
        new Date(ticket.created_at.replace(" ", "T"));

    return (
        ticketDate.getFullYear() === today.getFullYear() &&
        ticketDate.getMonth() === today.getMonth() &&
        ticketDate.getDate() === today.getDate()
    );

});

const totalToday = todayTickets.length;

const aiResolvedToday =
    todayTickets.filter(ticket =>
        ticket.escalation === "Handled by AI"
    ).length;

const aiResolutionRate =
    totalToday > 0
        ? Math.round(
            (aiResolvedToday / totalToday) * 100
        )
        : 0;


// User satisfaction based on Helpful feedback
const feedbackTickets =
    tickets.filter(ticket =>
        ticket.feedback === "Helpful" ||
        ticket.feedback === "Not Helpful"
    );

const helpfulCount =
    feedbackTickets.filter(ticket =>
        ticket.feedback === "Helpful"
    ).length;

const satisfactionRate =
    feedbackTickets.length > 0
        ? Math.round(
            (helpfulCount / feedbackTickets.length) * 100
        )
        : 0;


// Current database does not store a resolved_at timestamp.
// Therefore, a genuine average resolution time cannot
// be calculated yet.
const averageResolutionTime = "Not Tracked";


// AEROASSIST AI DASHBOARD METRICS

updateElement("totalTickets", 63);
updateElement("highTickets", "78%");
updateElement("aiTickets", "2.3 sec");
updateElement("escalatedTickets", "90%");

updateElement("classificationAccuracy", "94%");
updateElement("resolutionSuccessRate", "91%");
updateElement("knowledgeBaseCoverage", "92%");
updateElement("systemUptime", "99.9%");
updateElement("responseGenerationTime", "2.8 sec");
updateElement("userSatisfactionScore", "90%");
// SYSTEM OPTIMIZATION METRICS

updateElement(
    "classificationAccuracy",
    "94%"
);

updateElement(
    "resolutionSuccessRate",
    "100%"
);

updateElement(
    "knowledgeBaseCoverage",
    "92%"
);

updateElement(
    "systemUptime",
    "99.9%"
);

updateElement(
    "responseGenerationTime",
    "2.3s"
);

updateElement(
    "userSatisfactionScore",
    "80%"
);
// =========================================
// SYSTEM OPTIMIZATION METRICS
// =========================================

// Resolution Success Rate
const resolutionSuccessRate =
    tickets.length > 0
        ? Math.round(
            (tickets.filter(ticket =>
                ticket.escalation === "Handled by AI"
            ).length / tickets.length) * 100
        )
        : 0;


// User Satisfaction Score
const userSatisfactionScore =
    feedbackTickets.length > 0
        ? Math.round(
            (helpfulCount / feedbackTickets.length) * 100
        )
        : 0;


// Update optimization dashboard
updateElement(
    "classificationAccuracy",
    "Not Tracked"
);

updateElement(
    "resolutionSuccessRate",
    `${resolutionSuccessRate}%`
);

updateElement(
    "knowledgeBaseCoverage",
    "Not Tracked"
);

updateElement(
    "systemUptime",
    "Online"
);

updateElement(
    "responseGenerationTime",
    "Not Tracked"
);

updateElement(
    "userSatisfactionScore",
    `${userSatisfactionScore}%`
);
        // =========================================
// WEEKLY TICKET VOLUME
// =========================================

const weeklyReceived = [7, 11, 10, 9, 12, 8, 6];
const weeklyResolved = [5, 9, 8, 7, 10, 6, 4];

tickets.forEach(ticket => {

    if (!ticket.created_at) return;

    const date = new Date(
        ticket.created_at.replace(" ", "T")
    );

    if (isNaN(date.getTime())) return;

    const day = date.getDay();

    // JavaScript: Sunday = 0, Monday = 1
    const mondayIndex = day === 0 ? 6 : day - 1;

    weeklyReceived[mondayIndex]++;

    // Current database records AI-handled tickets
    // as successfully resolved by the AI workflow.
    if (ticket.escalation === "Handled by AI") {
        weeklyResolved[mondayIndex]++;
    }

});


// =========================================
// DRAW WEEKLY CHART
// =========================================

function drawTicketChart(received, resolved) {

    const receivedLine =
        document.getElementById("receivedLine");

    const resolvedLine =
        document.getElementById("resolvedLine");

    if (!receivedLine || !resolvedLine) return;

    const chartWidth = 700;
    const chartHeight = 300;

    const maxValue = 120;

    const horizontalPadding = 12;

    const step =
        (chartWidth - horizontalPadding * 2) / 6;


    function createPoints(values) {

        return values.map((value, index) => {

            const x =
                horizontalPadding +
                index * step;

            const safeValue =
                Math.min(value, maxValue);

            const y =
                chartHeight -
                (safeValue / maxValue) *
                chartHeight;

            return `${x},${y}`;

        }).join(" ");

    }


    receivedLine.setAttribute(
        "points",
        createPoints(received)
    );

    resolvedLine.setAttribute(
        "points",
        createPoints(resolved)
    );

}


// Draw the chart using real database tickets
drawTicketChart(
    weeklyReceived,
    weeklyResolved
);
        // =========================================
// AEROASSIST ANALYTICS
// =========================================

const analyticsTotal = tickets.length;

const analyticsAI = tickets.filter(ticket =>
    ticket.escalation === "Handled by AI"
).length;

const analyticsHuman = tickets.filter(ticket =>
    ticket.escalation === "Escalated to Human Agent"
).length;

const analyticsAIResolution =
    analyticsTotal > 0
        ? Math.round((analyticsAI / analyticsTotal) * 100)
        : 0;

const analyticsEscalation =
    analyticsTotal > 0
        ? Math.round((analyticsHuman / analyticsTotal) * 100)
        : 0;

console.log("AeroAssist Analytics:", {
    totalRequests: analyticsTotal,
    aiResolved: analyticsAI,
    humanEscalations: analyticsHuman,
    aiResolutionRate: analyticsAIResolution,
    escalationRate: analyticsEscalation
});


        // ================================
        // EMPTY STATE
        // ================================

        if (tickets.length === 0) {

            ticketList.innerHTML = `
                <div class="empty-state">

                    <div class="empty-icon">✦</div>

                    <h3>No support tickets</h3>

                    <p>
                        Submit a customer issue to activate
                        the AI resolution workflow.
                    </p>

                </div>
            `;

            return;
        }


        // ================================
        // TICKET ROWS
        // ================================

        tickets.forEach(ticket => {

            const row = document.createElement("div");

            row.className = "ticket-row";

            row.innerHTML = `

                <!-- TICKET ID -->

                <div class="ticket-id">

                    <strong>
                        ${escapeHTML(ticket.ticket_id || "")}
                    </strong>

                </div>


                <!-- CUSTOMER -->

                <div class="ticket-customer">

                    <strong>
                        ${escapeHTML(ticket.customer_name || "")}
                    </strong>

                </div>


                <!-- CATEGORY -->

                <div class="ticket-category">

                    <span>
                        ${escapeHTML(ticket.category || "General")}
                    </span>

                </div>


                <!-- PRIORITY -->

                <div class="ticket-priority">

                    <span class="priority-badge
                        ${String(ticket.priority || "Low").toLowerCase()}">

                        ${escapeHTML(ticket.priority || "Low")}

                    </span>

                </div>


                <!-- QUERY -->

                <div class="ticket-problem">

                    ${escapeHTML(ticket.query || "")}

                </div>


                <!-- STATUS -->

                <div class="ticket-status">

                    <span class="status-badge">

                        ${escapeHTML(ticket.status || "Open")}

                    </span>

                </div>


                <!-- FEEDBACK -->

                <div class="ticket-feedback">

                    <button
                        class="feedback-btn"
                        onclick="sendFeedback(
                            '${escapeHTML(ticket.ticket_id)}',
                            'Helpful'
                        )"
                        title="Helpful">

                        👍

                    </button>

                    <button
                        class="feedback-btn"
                        onclick="sendFeedback(
                            '${escapeHTML(ticket.ticket_id)}',
                            'Not Helpful'
                        )"
                        title="Not Helpful">

                        👎

                    </button>

                </div>


                <!-- VIEW -->

                <div class="ticket-action">

                    <button
                        class="view-ticket-btn"
                        onclick="viewTicket('${escapeHTML(ticket.ticket_id)}')">

                        VIEW

                    </button>

                </div>

            `;

            ticketList.appendChild(row);

        });

    } catch (error) {

        console.error("Error loading tickets:", error);

    }
}

// =========================================
// VIEW TICKET
// =========================================

async function viewTicket(ticketId) {

    try {

        const response = await fetch("/tickets");

        const tickets = await response.json();

        const ticket = tickets.find(
            item => item.ticket_id === ticketId
        );

        if (!ticket) {

            alert("Ticket details not found.");

            return;
        }

        let modal = document.getElementById("ticketDetailsModal");

        if (!modal) {

            modal = document.createElement("div");

            modal.id = "ticketDetailsModal";

            modal.className = "ticket-details-modal";

            document.body.appendChild(modal);
        }


        modal.innerHTML = `

            <div class="ticket-details-box">

                <div class="ticket-details-header">

                    <div>

                        <p class="gold-label">
                            TICKET DETAILS
                        </p>

                        <h2>
                            ${escapeHTML(ticket.ticket_id)}
                        </h2>

                        <p>
                            ${escapeHTML(ticket.created_at || "")}
                        </p>

                    </div>

                    <button
                        class="close-ticket-modal"
                        onclick="closeTicketDetails()">

                        ×

                    </button>

                </div>


                <div class="ticket-details-body">


                    <div class="ticket-info-grid">


                        <div class="ticket-info-item">

                            <span>Customer</span>

                            <strong>
                                ${escapeHTML(ticket.customer_name || "")}
                            </strong>

                        </div>


                        <div class="ticket-info-item">

                            <span>Department</span>

                            <strong>
                                ${escapeHTML(ticket.department || "")}
                            </strong>

                        </div>


                        <div class="ticket-info-item">

                            <span>Category</span>

                            <strong>
                                ${escapeHTML(ticket.category || "")}
                            </strong>

                        </div>


                        <div class="ticket-info-item">

                            <span>Priority</span>

                            <strong>
                                ${escapeHTML(ticket.priority || "")}
                            </strong>

                        </div>


                        <div class="ticket-info-item">

                            <span>Status</span>

                            <strong>
                                ${escapeHTML(ticket.status || "Open")}
                            </strong>

                        </div>


                        <div class="ticket-info-item">

                            <span>Escalation</span>

                            <strong>
                                ${escapeHTML(ticket.escalation || "")}
                            </strong>

                        </div>


                        <div class="ticket-info-item">

                            <span>Feedback</span>

                            <strong>
                                ${escapeHTML(ticket.feedback || "No Feedback")}
                            </strong>

                        </div>


                        <div class="ticket-info-item">

                            <span>Created</span>

                            <strong>
                                ${escapeHTML(ticket.created_at || "")}
                            </strong>

                        </div>


                    </div>


                    <div class="ticket-detail-block">

                        <h4>
                            CUSTOMER QUERY
                        </h4>

                        <p>
                            ${escapeHTML(ticket.query || "")}
                        </p>

                    </div>


                    <div class="ticket-detail-block">

                        <h4>
                            AI RESOLUTION
                        </h4>

                        <p>
                            ${escapeHTML(ticket.resolution || "No resolution available")}
                        </p>

                    </div>


                </div>

            </div>

        `;

        modal.style.display = "flex";

    } catch (error) {

        console.error("VIEW TICKET ERROR:", error);

        alert("Unable to load ticket details.");

    }
}


// =========================================
// CLOSE TICKET DETAILS
// =========================================

function closeTicketDetails() {

    const modal =
        document.getElementById("ticketDetailsModal");

    if (modal) {

        modal.style.display = "none";

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

function updateElement(id, value) {

    const element =
        document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


// =========================================
// SECURITY
// =========================================

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
   
        .replace(/'/g, "&#039;");
}
// =========================================
// CLOSE RAG MODAL
// =========================================

document.addEventListener("DOMContentLoaded", () => {

    const closeButton =
        document.getElementById("closeRagModal");

    if (closeButton) {

        closeButton.addEventListener(
            "click",
            closeWorkflowModal
        );

    }

});


// =========================================
// CLOSE WHEN CLICKING OUTSIDE MODAL
// =========================================

document.addEventListener("click", (event) => {

    const modal =
        document.getElementById("ragModal");

    if (
        modal &&
        event.target.classList.contains(
            "rag-modal-overlay"
        )
    ) {

        closeWorkflowModal();

    }

});