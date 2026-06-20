document.addEventListener("DOMContentLoaded", function () {
    // --- SIDEBAR TOGGLE ---
    const sidebar = document.getElementById("sidebar");
    const sidebarCollapse = document.getElementById("sidebarCollapse");
    
    if (sidebar && sidebarCollapse) {
        sidebarCollapse.addEventListener("click", function () {
            sidebar.classList.toggle("active");
        });
    }

    // --- AUTO-CLOSE NOTIFICATIONS ---
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Check if bootstrap is defined and has Alert module
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Fallback direct DOM deletion
                alert.style.transition = "opacity 0.5s ease";
                alert.style.opacity = "0";
                setTimeout(function() {
                    alert.remove();
                }, 500);
            }
        }, 5000);
    });
});
