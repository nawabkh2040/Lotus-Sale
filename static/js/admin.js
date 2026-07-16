// Lotus Admin dashboard logic
(function () {
    const $ = (id) => document.getElementById(id);

    function esc(s) {
        return String(s == null ? "" : s)
            .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function badgeClass(status) {
        const s = (status || "").toLowerCase();
        if (s.includes("deliver") && !s.includes("out")) return "delivered";
        if (s.includes("out")) return "out";
        if (s.includes("ship")) return "shipped";
        if (s.includes("process")) return "processing";
        return "placed";
    }

    async function getJSON(url) {
        const res = await fetch(url, { headers: { Accept: "application/json" } });
        if (res.status === 401) { window.location.href = "/admin"; return null; }
        if (!res.ok) throw new Error("Request failed: " + res.status);
        return res.json();
    }

    function fmtTime(iso) {
        if (!iso) return "";
        const d = new Date(iso.endsWith("Z") || iso.includes("+") ? iso : iso + "Z");
        if (isNaN(d)) return iso;
        return d.toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
    }

    async function loadStats() {
        try {
            const s = await getJSON("/admin/api/stats");
            if (!s) return;
            $("statSessions").textContent = s.sessions;
            $("statMessages").textContent = s.messages;
            $("statOrders").textContent = s.orders;
        } catch (e) { console.error(e); }
    }

    async function loadSessions() {
        try {
            const sessions = await getJSON("/admin/api/sessions");
            if (!sessions) return;
            const body = $("sessionsBody");
            if (!sessions.length) {
                body.innerHTML = '<tr><td colspan="3" class="muted center">No sessions yet. Chat with the bot first.</td></tr>';
                return;
            }
            body.innerHTML = sessions.map(s => `
                <tr data-sid="${esc(s.session_id)}">
                    <td class="sess-id">${esc(s.session_id).slice(0, 13)}…</td>
                    <td>${s.message_count}</td>
                    <td>${fmtTime(s.last_active)}</td>
                </tr>`).join("");
            body.querySelectorAll("tr").forEach(tr => {
                tr.addEventListener("click", () => {
                    body.querySelectorAll("tr").forEach(r => r.classList.remove("active"));
                    tr.classList.add("active");
                    loadTranscript(tr.dataset.sid);
                });
            });
        } catch (e) { console.error(e); }
    }

    async function loadTranscript(sessionId) {
        const box = $("transcript");
        $("transcriptTitle").textContent = "Transcript · " + sessionId.slice(0, 8);
        box.innerHTML = '<div class="muted center">Loading…</div>';
        try {
            const data = await getJSON("/admin/api/sessions/" + encodeURIComponent(sessionId));
            if (!data) return;
            if (!data.messages.length) {
                box.innerHTML = '<div class="muted center">No messages.</div>';
                return;
            }
            box.innerHTML = data.messages.map(m => `
                <div class="bubble ${m.role === "user" ? "user" : "assistant"}">
                    ${esc(m.message)}
                    <span class="ts">${fmtTime(m.created_at)}</span>
                </div>`).join("");
        } catch (e) {
            box.innerHTML = '<div class="muted center">Failed to load transcript.</div>';
        }
    }

    async function loadOrders() {
        try {
            const orders = await getJSON("/admin/api/orders");
            if (!orders) return;
            const body = $("ordersBody");
            if (!orders.length) {
                body.innerHTML = '<tr><td colspan="6" class="muted center">No orders yet.</td></tr>';
                return;
            }
            body.innerHTML = orders.map(o => `
                <tr>
                    <td class="order-id">${esc(o.order_id)}</td>
                    <td>${esc(o.product_name)}</td>
                    <td>${esc(o.amount)}</td>
                    <td><span class="badge ${badgeClass(o.status)}">${esc(o.status)}</span></td>
                    <td>${esc(o.order_date)}</td>
                    <td>${esc(o.expected_delivery)}</td>
                </tr>`).join("");
        } catch (e) { console.error(e); }
    }

    function initTabs() {
        document.querySelectorAll(".tab").forEach(tab => {
            tab.addEventListener("click", () => {
                document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
                tab.classList.add("active");
                const which = tab.dataset.tab;
                $("tab-sessions").style.display = which === "sessions" ? "" : "none";
                $("tab-orders").style.display = which === "orders" ? "" : "none";
            });
        });
    }

    function refreshAll() {
        loadStats();
        loadSessions();
        loadOrders();
    }

    document.addEventListener("DOMContentLoaded", () => {
        initTabs();
        refreshAll();
        const rb = $("refreshBtn");
        if (rb) rb.addEventListener("click", refreshAll);
    });
})();
