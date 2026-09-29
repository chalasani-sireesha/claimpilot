function getCookie(name) {

    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {

        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {

            return decodeURIComponent(
                cookie.substring(name.length + 1)
            );

        }
    }

    return null;
}

const claimForm = document.getElementById("claimForm");

const statusMessage = document.getElementById("status");

const resultsSection = document.getElementById("results");

const recommendedRoute =
    document.getElementById("recommendedRoute");

const claimClassification =
    document.getElementById("claimClassification");

const investigationFlag =
    document.getElementById("investigationFlag");

const extractedFields =
    document.getElementById("extractedFields");

const missingFields =
    document.getElementById("missingFields");

const inconsistencies =
    document.getElementById("inconsistencies");

const reasoning =
    document.getElementById("reasoning");

const jsonResult =
    document.getElementById("jsonResult");


claimForm.addEventListener("submit", async function(event) {

    event.preventDefault();


    const fileInput =
        document.getElementById("document");

    const file = fileInput.files[0];


    if (!file) {

        statusMessage.textContent =
            "Please select a document.";

        return;
    }


    const formData = new FormData();

    formData.append(
        "document",
        file
    );


    statusMessage.textContent =
        "Processing claim...";


    resultsSection.style.display = "none";


    try {

        const csrftoken = getCookie("csrftoken");

const response = await fetch(
    "/api/process-claim/",
    {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: formData
    }
);


        const data = await response.json();

        console.log("STATUS:", response.status);
        console.log("RESPONSE:", data);


        if (!response.ok) {

            throw new Error(
                data.error || "Failed to process claim."
            );
        }


        displayResults(data);


        statusMessage.textContent =
            "Claim processed successfully.";


    } catch (error) {

        statusMessage.textContent =
            "Error: " + error.message;

    }

});


function displayResults(data) {

    resultsSection.style.display = "block";


    /*
     * Recommended Route
     */

    const route =
    data.recommendedRoute || "Not available";

recommendedRoute.textContent = route;

recommendedRoute.className = "route-value";

if (route === "Fast-track") {

    recommendedRoute.classList.add("fast-track");

}
else if (route === "Manual Review") {

    recommendedRoute.classList.add("manual-review");

}
else if (route === "Investigation Flag") {

    recommendedRoute.classList.add("investigation");

}
else if (route === "Specialist Queue") {

    recommendedRoute.classList.add("specialist");

}


    /*
     * Claim Classification
     */

    claimClassification.textContent =
        data.claimClassification || "Not available";


    /*
     * Investigation Flag
     */

    if (data.investigationFlag) {

    investigationFlag.textContent = "YES";

    investigationFlag.className =
        "flag-yes";

} else {

    investigationFlag.textContent = "NO";

    investigationFlag.className =
        "flag-no";

}


    /*
     * Extracted Fields
     */

    extractedFields.textContent =
        JSON.stringify(
            data.extractedFields || {},
            null,
            2
        );


    /*
     * Missing Fields
     */

    missingFields.innerHTML = "";


    if (
        data.missingFields &&
        data.missingFields.length > 0
    ) {

        data.missingFields.forEach(function(field) {

            const li =
                document.createElement("li");

            li.textContent = field;

            missingFields.appendChild(li);

        });

    } else {

        const li =
            document.createElement("li");

        li.textContent =
            "No mandatory fields are missing.";

        missingFields.appendChild(li);

    }


    /*
     * Inconsistencies
     */

    inconsistencies.innerHTML = "";


    if (
        data.inconsistencies &&
        data.inconsistencies.length > 0
    ) {

        data.inconsistencies.forEach(function(item) {

            const li =
                document.createElement("li");

            li.textContent = item;

            inconsistencies.appendChild(li);

        });

    } else {

        const li =
            document.createElement("li");

        li.textContent =
            "No inconsistencies detected.";

        inconsistencies.appendChild(li);

    }


    /*
     * Reasoning
     */

    reasoning.textContent =
        data.reasoning || "No reasoning available.";


    /*
     * Full JSON
     */

    jsonResult.textContent =
        JSON.stringify(
            data,
            null,
            2
        );
    loadClaimHistory();
    loadClaimStatistics();

}

// =========================================
// CLAIM HISTORY
// =========================================

const claimHistory =
    document.getElementById("claimHistory");


const refreshHistory =
    document.getElementById("refreshHistory");


async function loadClaimHistory() {

    try {

        const response = await fetch(
            "/api/claims/"
        );


        if (!response.ok) {

            throw new Error(
                "Unable to load claim history."
            );

        }


        const claims =
            await response.json();


        claimHistory.innerHTML = "";


        if (claims.length === 0) {

            claimHistory.innerHTML = `
                <tr>
                    <td colspan="6">
                        No claims processed yet.
                    </td>
                </tr>
            `;

            return;
        }


        claims.forEach(function(claim) {

            const row =
                document.createElement("tr");


            row.innerHTML = `

                <td>
                    ${claim.id}
                </td>

                <td>
                    ${claim.policy_number || "-"}
                </td>

                <td>
                    ${claim.claim_type || "-"}
                </td>

                <td>
                    ₹${claim.estimated_damage || "0"}
                </td>

                <td>
                    ${claim.recommended_route || "-"}
                </td>

                <td>
                    ${claim.investigation_flag ? "YES" : "NO"}
                </td>

            `;


            claimHistory.appendChild(row);

        });


    } catch (error) {

        claimHistory.innerHTML = `
            <tr>
                <td colspan="6">
                    ${error.message}
                </td>
            </tr>
        `;

    }

}


refreshHistory.addEventListener(
    "click",
    loadClaimHistory
);


// Load history when page opens

loadClaimHistory();



// =========================================
// CLAIM STATISTICS
// =========================================

async function loadClaimStatistics() {

    try {

        const response = await fetch(
            "/api/statistics/"
        );

        if (!response.ok) {

            throw new Error(
                "Unable to load statistics."
            );

        }

        const data =
            await response.json();


        document.getElementById(
            "totalClaims"
        ).textContent =
            data.totalClaims;


        document.getElementById(
            "fastTrack"
        ).textContent =
            data.fastTrack;


        document.getElementById(
            "manualReview"
        ).textContent =
            data.manualReview;


        document.getElementById(
            "investigation"
        ).textContent =
            data.investigation;


        document.getElementById(
            "specialist"
        ).textContent =
            data.specialist;


    } catch (error) {

        console.error(
            error.message
        );

    }

}


// Load statistics when page opens
loadClaimStatistics();