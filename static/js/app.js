document.addEventListener("DOMContentLoaded", function () {

    // ── SVG Donut chart ───────────────────────────────────────────
    const svg = document.getElementById("donutSvg");
    if (svg) {
        const data = [
            { label: "Applied",   key: "applied",   color: "#3b82f6" },
            { label: "Interview", key: "interview", color: "#f59e0b" },
            { label: "Offer",     key: "offer",     color: "#10b981" },
            { label: "Rejected",  key: "rejected",  color: "#ef4444" },
        ];

        data.forEach(d => { d.value = parseInt(svg.dataset[d.key] || "0"); });
        const total = data.reduce((s, d) => s + d.value, 0);

        const cx = 90, cy = 90, R = 70, r = 44;
        let angle = -Math.PI / 2;

        if (total === 0) {
            // Empty state ring
            const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            circle.setAttribute("cx", cx); circle.setAttribute("cy", cy);
            circle.setAttribute("r", (R + r) / 2);
            circle.setAttribute("fill", "none");
            circle.setAttribute("stroke", "#e2e8f0");
            circle.setAttribute("stroke-width", R - r);
            svg.appendChild(circle);
        } else {
            data.forEach(d => {
                if (d.value === 0) return;
                const slice = (d.value / total) * 2 * Math.PI;
                const x1 = cx + R * Math.cos(angle), y1 = cy + R * Math.sin(angle);
                const x2 = cx + R * Math.cos(angle + slice), y2 = cy + R * Math.sin(angle + slice);
                const ix1 = cx + r * Math.cos(angle + slice), iy1 = cy + r * Math.sin(angle + slice);
                const ix2 = cx + r * Math.cos(angle), iy2 = cy + r * Math.sin(angle);
                const large = slice > Math.PI ? 1 : 0;
                const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                path.setAttribute("d",
                    `M ${x1} ${y1} A ${R} ${R} 0 ${large} 1 ${x2} ${y2} ` +
                    `L ${ix1} ${iy1} A ${r} ${r} 0 ${large} 0 ${ix2} ${iy2} Z`
                );
                path.setAttribute("fill", d.color);
                path.style.transition = "opacity .2s";
                path.addEventListener("mouseenter", () => path.setAttribute("opacity", "0.8"));
                path.addEventListener("mouseleave", () => path.setAttribute("opacity", "1"));
                svg.appendChild(path);
                angle += slice;
            });
        }

        // Centre label
        const tTotal = document.createElementNS("http://www.w3.org/2000/svg", "text");
        tTotal.setAttribute("x", cx); tTotal.setAttribute("y", cy - 8);
        tTotal.setAttribute("text-anchor", "middle");
        tTotal.setAttribute("font-size", "22"); tTotal.setAttribute("font-weight", "800");
        tTotal.setAttribute("fill", "#0f172a"); tTotal.textContent = total;
        svg.appendChild(tTotal);

        const tLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
        tLabel.setAttribute("x", cx); tLabel.setAttribute("y", cy + 12);
        tLabel.setAttribute("text-anchor", "middle");
        tLabel.setAttribute("font-size", "10"); tLabel.setAttribute("font-weight", "600");
        tLabel.setAttribute("fill", "#94a3b8"); tLabel.textContent = "TOTAL";
        svg.appendChild(tLabel);

        // Legend
        const legendEl = document.getElementById("chartLegend");
        if (legendEl) {
            data.forEach(d => {
                const row = document.createElement("div");
                row.className = "legend-row";
                row.innerHTML =
                    `<span class="legend-pip" style="background:${d.color}"></span>` +
                    `<span class="legend-name">${d.label}</span>` +
                    `<span class="legend-num">${d.value}</span>`;
                legendEl.appendChild(row);
            });
        }
    }

    // ── Big bar chart (canvas) ────────────────────────────────────
    const bar = document.getElementById("barCanvas");
    if (bar) {
        const data = [
            { label: "Applied",   value: parseInt(bar.dataset.applied   || "0"), color: "#3b82f6" },
            { label: "Interview", value: parseInt(bar.dataset.interview || "0"), color: "#f59e0b" },
            { label: "Offer",     value: parseInt(bar.dataset.offer     || "0"), color: "#10b981" },
            { label: "Rejected",  value: parseInt(bar.dataset.rejected  || "0"), color: "#ef4444" },
        ];

        const DPR  = window.devicePixelRatio || 1;
        const W    = bar.parentElement.clientWidth || 560;
        const H    = 260;
        bar.width  = W * DPR; bar.height = H * DPR;
        bar.style.width = W + "px"; bar.style.height = H + "px";

        const ctx = bar.getContext("2d");
        ctx.scale(DPR, DPR);

        const pL = 44, pR = 24, pT = 28, pB = 52;
        const cW = W - pL - pR, cH = H - pT - pB;
        const maxV = Math.max(1, ...data.map(d => d.value));
        const steps = 5;

        // Grid
        for (let i = 0; i <= steps; i++) {
            const y = pT + cH - (i / steps) * cH;
            ctx.strokeStyle = i === 0 ? "#cbd5e1" : "#f1f5f9";
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(pL, y); ctx.lineTo(pL + cW, y); ctx.stroke();
            const val = Math.round((i / steps) * maxV);
            ctx.fillStyle = "#94a3b8"; ctx.font = `${11}px sans-serif`;
            ctx.textAlign = "right";
            ctx.fillText(val, pL - 8, y + 4);
        }

        // Bars
        const gap = cW / data.length;
        const bW  = Math.min(64, gap * 0.55);

        data.forEach((d, i) => {
            const bH = (d.value / maxV) * cH || 0;
            const x  = pL + i * gap + (gap - bW) / 2;
            const y  = pT + cH - bH;
            const rr = Math.min(8, bW / 2, bH || 9999);

            // Gradient
            const grad = ctx.createLinearGradient(0, y, 0, y + bH);
            grad.addColorStop(0, d.color);
            grad.addColorStop(1, d.color + "aa");
            ctx.fillStyle = grad;

            if (bH > 0) {
                ctx.beginPath();
                ctx.moveTo(x + rr, y);
                ctx.lineTo(x + bW - rr, y);
                ctx.quadraticCurveTo(x + bW, y, x + bW, y + rr);
                ctx.lineTo(x + bW, y + bH);
                ctx.lineTo(x, y + bH);
                ctx.lineTo(x, y + rr);
                ctx.quadraticCurveTo(x, y, x + rr, y);
                ctx.closePath();
                ctx.fill();

                // Value label
                ctx.fillStyle = "#0f172a";
                ctx.font = `bold ${13}px sans-serif`;
                ctx.textAlign = "center";
                ctx.fillText(d.value, x + bW / 2, y - 7);
            }

            // X label
            ctx.fillStyle = "#64748b"; ctx.font = `${12}px sans-serif`;
            ctx.textAlign = "center";
            ctx.fillText(d.label, x + bW / 2, H - pB + 20);

            // Color dot under label
            ctx.fillStyle = d.color;
            ctx.beginPath();
            ctx.arc(x + bW / 2, H - pB + 30, 3, 0, Math.PI * 2);
            ctx.fill();
        });

        // Chart title
        ctx.fillStyle = "#94a3b8"; ctx.font = `bold ${11}px sans-serif`;
        ctx.textAlign = "left";
        ctx.fillText("APPLICATION STATUS BREAKDOWN", pL, 16);
    }

    // ── Inline status colour swap ─────────────────────────────────
    document.querySelectorAll(".status-select").forEach(sel => {
        const apply = v => {
            sel.className = "status-select ss-" + v.toLowerCase();
        };
        apply(sel.value);
        sel.addEventListener("change", () => apply(sel.value));
    });

});
