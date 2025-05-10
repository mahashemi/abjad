// Add this code to your existing JavaScript section
document.addEventListener("DOMContentLoaded", function () {
    // Define selectors for toggle switches
    const toggleSwitches = {
        "toggle-calculation": ".calculation",
        "toggle-translation-urdu":
            '.translations p:has(.translation-title:contains("اردو"))',
        "toggle-translation-farsi":
            '.translations p:has(.translation-title:contains("فارسی"))',
        "toggle-translation-english":
            '.translations p:has(.translation-title:contains("English"))',
        "toggle-translation-transliteration":
            '.translations p:has(.translation-title:contains("Transliteration"))',
        "toggle-totals": ".adad-row, .grand-total",
    };

    // Simple function to find elements with text content
    function findElementsWithText(containerSelector, textContent) {
        const containers = document.querySelectorAll(containerSelector);
        return Array.from(containers).filter((container) => {
            const titleElement = container.querySelector(".translation-title");
            return titleElement && titleElement.textContent.includes(textContent);
        });
    }

    // Set up change handlers for toggle switches
    for (const [switchId, selector] of Object.entries(toggleSwitches)) {
        const toggleSwitch = document.getElementById(switchId);
        if (toggleSwitch) {
            toggleSwitch.addEventListener("change", function () {
                const isVisible = this.checked;

                if (selector.includes(":has")) {
                    // For selectors using :has which might not be supported in all browsers
                    let elements;

                    if (selector.includes("اردو")) {
                        elements = findElementsWithText(".translations p", "اردو");
                    } else if (selector.includes("فارسی")) {
                        elements = findElementsWithText(".translations p", "فارسی");
                    } else if (selector.includes("English")) {
                        elements = findElementsWithText(".translations p", "English");
                    } else if (selector.includes("Transliteration")) {
                        elements = findElementsWithText(
                            ".translations p",
                            "Transliteration"
                        );
                    } else {
                        elements = [];
                    }

                    elements.forEach((element) => {
                        element.style.display = isVisible ? "" : "none";
                    });
                } else {
                    // For standard CSS selectors
                    const elements = document.querySelectorAll(selector);
                    elements.forEach((element) => {
                        element.style.display = isVisible ? "" : "none";
                    });
                }
            });
        }
    }

    // Settings panel toggle functionality
    const togglePanelButton = document.getElementById("toggle-panel-button");
    const settingsPanel = document.querySelector(".toggle-panel");
    const settingsContent = document.querySelector(".toggle-panel-content");

    // Initialize panel state (expanded on desktop, collapsed on mobile by default)
    let isPanelExpanded = window.innerWidth > 768;
    updatePanelState();

    // Toggle panel when button is clicked
    if (togglePanelButton) {
        togglePanelButton.addEventListener("click", function () {
            isPanelExpanded = !isPanelExpanded;
            updatePanelState();
        });
    }

    // Update panel state based on window resize
    window.addEventListener("resize", function () {
        updatePanelState();
    });

    function updatePanelState() {
        if (!settingsPanel || !settingsContent || !togglePanelButton) return;

        if (isPanelExpanded) {
            settingsContent.style.maxHeight = settingsContent.scrollHeight + "px";
            settingsContent.style.overflow = "visible";
            togglePanelButton.innerHTML =
                '<i class="fa fa-chevron-up"></i>Close Settings';
            togglePanelButton.classList.add("expanded");
        } else {
            settingsContent.style.maxHeight = "0px";
            settingsContent.style.overflow = "hidden";
            togglePanelButton.innerHTML =
                '<i class="fa fa-chevron-down"></i>Open Settings';
            togglePanelButton.classList.remove("expanded");
        }
    }
});