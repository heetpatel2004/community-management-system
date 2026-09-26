/* ══ app.js — Saraswati Sanman Samaroh ══ */

document.addEventListener('DOMContentLoaded', function () {

    // ── Sidebar Toggle (Mobile) ──
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
            if (overlay) overlay.classList.toggle('show');
        });

        if (overlay) {
            overlay.addEventListener('click', function () {
                sidebar.classList.remove('show');
                overlay.classList.remove('show');
            });
        }
    }

    // ── Dynamic Student Name Inputs ──
    const addStudentBtn = document.getElementById('addStudentField');
    const studentFieldsContainer = document.getElementById('studentFields');

    if (addStudentBtn && studentFieldsContainer) {
        addStudentBtn.addEventListener('click', function () {
            const count = studentFieldsContainer.querySelectorAll('.student-input').length + 1;
            const div = document.createElement('div');
            div.className = 'mb-3 student-input';
            div.innerHTML = `
                <div class="input-group">
                    <span class="input-group-text">Student ${count}</span>
                    <input type="text" name="student_name" class="form-control"
                           placeholder="Full Name" required>
                    <button type="button" class="btn btn-outline-danger remove-student"
                            title="Remove">&times;</button>
                </div>
            `;
            studentFieldsContainer.appendChild(div);
            attachRemoveHandlers();
        });

        attachRemoveHandlers();
    }

    function attachRemoveHandlers() {
        document.querySelectorAll('.remove-student').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const inputs = studentFieldsContainer.querySelectorAll('.student-input');
                if (inputs.length > 1) {
                    btn.closest('.student-input').remove();
                    renumberStudents();
                }
            });
        });
    }

    function renumberStudents() {
        const inputs = studentFieldsContainer.querySelectorAll('.student-input');
        inputs.forEach(function (el, idx) {
            const span = el.querySelector('.input-group-text');
            if (span) span.textContent = `Student ${idx + 1}`;
        });
    }

    // ── Auto-dismiss Alerts ──
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // ── Confirm Dangerous Actions ──
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // ── File Upload Preview ──
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            const file = this.files[0];
            const preview = document.getElementById('filePreview');
            if (file && preview) {
                const maxMB = 5;
                if (file.size > maxMB * 1024 * 1024) {
                    alert(`File size (${(file.size / 1024 / 1024).toFixed(1)} MB) exceeds the maximum allowed size (${maxMB} MB).`);
                    this.value = '';
                    preview.innerHTML = '';
                    return;
                }
                preview.innerHTML = `<small class="text-muted">Selected: ${file.name} (${(file.size / 1024).toFixed(0)} KB)</small>`;
            }
        });
    }

    // ── Print Button ──
    document.querySelectorAll('[data-action="print"]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.print();
        });
    });

    // ── Number of students field → auto-create inputs ──
    const numStudentsField = document.getElementById('id_num_students');
    if (numStudentsField && studentFieldsContainer) {
        numStudentsField.addEventListener('change', function () {
            const count = parseInt(this.value) || 1;
            const currentCount = studentFieldsContainer.querySelectorAll('.student-input').length;

            if (count > currentCount) {
                for (let i = currentCount + 1; i <= count; i++) {
                    addStudentBtn.click();
                }
            } else if (count < currentCount) {
                const inputs = studentFieldsContainer.querySelectorAll('.student-input');
                for (let i = currentCount; i > count; i--) {
                    inputs[i - 1].remove();
                }
            }
        });
    }
});
