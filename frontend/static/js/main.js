/**
 * HER CARE+ Main Script
 * Handles calendar calculation, dynamic interactions, AJAX reminders logging, and modern micro-animations.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Fade out Django messages automatically
    const messages = document.querySelectorAll('.alert-dismissible');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.6s ease';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 600);
        }, 5000);
    });

    // Initialize Reminders Logging Asynchronously
    initMedicineReminders();

    // Initialize Menstrual Cycle Interactive Calendar
    initCycleCalendar();

    // Initialize Theme Toggle
    initThemeToggle();
});

/**
 * Handle medicine logs clicking asynchronously
 */
function initMedicineReminders() {
    const reminderCheckboxes = document.querySelectorAll('.reminder-checkbox-btn');
    
    reminderCheckboxes.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const reminderId = btn.dataset.reminderId;
            const timeSlot = btn.dataset.timeSlot;
            const parentRow = document.getElementById(`reminder-${reminderId}-${timeSlot}`);
            
            if (!reminderId || !timeSlot) return;

            try {
                btn.style.transform = 'scale(0.8)';
                const response = await fetch(`/reminders/mark-taken/${reminderId}/${timeSlot}/`, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    btn.style.transform = 'scale(1)';
                    
                    if (data.status === 'marked') {
                        parentRow.classList.add('completed');
                        btn.innerHTML = '<i class="fas fa-check"></i>';
                        showNotification('success', data.message);
                    } else if (data.status === 'unmarked') {
                        parentRow.classList.remove('completed');
                        btn.innerHTML = '';
                        showNotification('info', data.message);
                    }
                }
            } catch (err) {
                console.error("Error updating medicine log:", err);
                btn.style.transform = 'scale(1)';
                showNotification('danger', 'Something went wrong. Please try again.');
            }
        });
    });
}

/**
 * Custom Simple Toast Notification System
 */
function showNotification(type, message) {
    const toast = document.createElement('div');
    toast.className = `glass-card p-3 shadow-lg border border-opacity-20 d-flex align-items-center gap-2 alert-${type}`;
    toast.style.position = 'fixed';
    toast.style.bottom = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.maxWidth = '350px';
    toast.style.background = 'rgba(26, 21, 44, 0.9)';
    toast.style.borderColor = type === 'success' ? '#2ec4b6' : type === 'info' ? '#9b7fd4' : '#e8536d';
    
    let icon = '<i class="fas fa-info-circle text-info"></i>';
    if (type === 'success') icon = '<i class="fas fa-check-circle text-success" style="color: #2ec4b6 !important;"></i>';
    if (type === 'danger') icon = '<i class="fas fa-exclamation-triangle text-danger" style="color: #e8536d !important;"></i>';
    
    toast.innerHTML = `
        ${icon}
        <div style="font-size: 0.9rem;">${message}</div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.transition = 'all 0.5s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

/**
 * Renders an interactive calendar on cycle tracker page
 */
function initCycleCalendar() {
    const calendarContainer = document.getElementById('cycle-calendar');
    if (!calendarContainer) return;

    const calendarData = JSON.parse(calendarContainer.dataset.calendar || '[]');
    const nextPeriodStr = calendarContainer.dataset.nextPeriod || '';
    
    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();
    
    const monthNames = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ];

    function renderCalendar(month, year) {
        calendarContainer.innerHTML = '';
        
        // Month and Year label
        const header = document.createElement('div');
        header.className = 'calendar-header w-100 d-flex justify-content-between align-items-center mb-3';
        header.innerHTML = `
            <button class="btn btn-sm btn-outline-light" id="prev-month"><i class="fas fa-chevron-left"></i></button>
            <h4 class="m-0">${monthNames[month]} ${year}</h4>
            <button class="btn btn-sm btn-outline-light" id="next-month"><i class="fas fa-chevron-right"></i></button>
        `;
        calendarContainer.appendChild(header);

        // Calendar Grid
        const grid = document.createElement('div');
        grid.className = 'calendar-grid';
        
        // Add Day Names Header
        const dayNames = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
        dayNames.forEach(d => {
            const el = document.createElement('div');
            el.className = 'calendar-day-name';
            el.textContent = d;
            grid.appendChild(el);
        });

        // Days calculation
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Empty slots before first day
        for (let i = 0; i < firstDay; i++) {
            const empty = document.createElement('div');
            grid.appendChild(empty);
        }

        // Render month days
        for (let day = 1; day <= daysInMonth; day++) {
            const dayEl = document.createElement('div');
            dayEl.className = 'calendar-day';
            dayEl.textContent = day;

            // Date comparisons
            const thisDate = new Date(year, month, day);
            const dateStr = thisDate.getFullYear() + '-' + 
                            String(thisDate.getMonth() + 1).padStart(2, '0') + '-' + 
                            String(thisDate.getDate()).padStart(2, '0');

            // Today marking
            if (thisDate.toDateString() === today.toDateString()) {
                dayEl.classList.add('today');
            }

            // Period log matching
            calendarData.forEach(period => {
                const start = new Date(period.start);
                const end = new Date(period.end);
                
                // Clear time info
                thisDate.setHours(0,0,0,0);
                start.setHours(0,0,0,0);
                end.setHours(0,0,0,0);

                if (thisDate >= start && thisDate <= end) {
                    dayEl.classList.add('period-active');
                    dayEl.setAttribute('title', `Flow: ${period.flow}`);
                }
            });

            // Predicted next period marking (approx. 5 days range)
            if (nextPeriodStr) {
                const nextPeriod = new Date(nextPeriodStr);
                nextPeriod.setHours(0,0,0,0);
                
                const predStart = new Date(nextPeriod);
                const predEnd = new Date(nextPeriod);
                predEnd.setDate(predEnd.getDate() + 4);

                if (thisDate >= predStart && thisDate <= predEnd) {
                    dayEl.classList.add('period-predicted');
                    dayEl.setAttribute('title', 'Predicted Period');
                }
            }

            grid.appendChild(dayEl);
        }

        calendarContainer.appendChild(grid);

        // Attach header button triggers
        document.getElementById('prev-month').addEventListener('click', () => {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            renderCalendar(currentMonth, currentYear);
        });

        document.getElementById('next-month').addEventListener('click', () => {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
            renderCalendar(currentMonth, currentYear);
        });
    }

    renderCalendar(currentMonth, currentYear);
}

/**
 * Handle Dark/Light Theme Toggling
 */
function initThemeToggle() {
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    if (!toggleBtns.length) return;

    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    
    function updateIcons(theme) {
        toggleBtns.forEach(btn => {
            if (theme === 'dark') {
                btn.innerHTML = '<i class="fas fa-sun text-warning"></i>';
                btn.title = 'Switch to Light Mode';
            } else {
                btn.innerHTML = '<i class="fas fa-moon"></i>';
                btn.title = 'Switch to Dark Mode';
            }
        });
    }
    
    updateIcons(currentTheme);

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            let theme = document.documentElement.getAttribute('data-theme') || 'light';
            let newTheme = theme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            updateIcons(newTheme);
        });
    });
}
