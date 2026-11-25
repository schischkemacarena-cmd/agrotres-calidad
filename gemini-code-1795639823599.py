with open("agrotres-calidad-v4.html", "r", encoding="utf-8") as f:
    base_html = f.read()

with open("agrotres-capacitaciones-r02-v5.html", "r", encoding="utf-8") as f:
    v5_html = f.read()

s_cap = v5_html.find("const CAPACITACIONES_BASE = ")
e_cap = v5_html.find(";\n", s_cap)
cap_base_decl = v5_html[s_cap:e_cap+1]

s_cert_css = v5_html.find("/* --- Certificado A4 ---")
e_cert_css = v5_html.find("</style>", s_cert_css)
cert_css = v5_html[s_cert_css:e_cert_css]

cap_extra_css = """
    .mode-switch-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      background: #e2e8f0;
      padding: 4px;
      border-radius: 12px;
      margin-bottom: 12px;
      gap: 4px;
    }
    .cap-subtabs {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 4px;
      margin-bottom: 12px;
      scrollbar-width: none;
    }
    .cap-subtabs::-webkit-scrollbar { display: none; }
    .cap-subtab {
      border: 1px solid var(--border);
      background: #fff;
      color: var(--text);
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 0.8rem;
      font-weight: 700;
      white-space: nowrap;
      cursor: pointer;
    }
    .cap-subtab.active {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }
    .month-filter-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;
    }
    .m-chip {
      border: 1px solid #cbd5e1;
      background: #fff;
      color: var(--text);
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
    }
    .m-chip.active {
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary);
    }
    .topic-card {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px;
      margin-bottom: 10px;
      background: #fff;
    }
    .topic-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
      margin-bottom: 6px;
    }
    .topic-title {
      font-weight: 800;
      font-size: 0.92rem;
      color: var(--text);
    }
    .b-ok { background: var(--ok-bg); color: var(--ok-tx); }
    .b-warn { background: var(--warn-bg); color: var(--warn-tx); }
    .b-info { background: var(--primary-light); color: var(--primary); }
    .matrix-wrap {
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #fff;
    }
    .matrix-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.75rem;
      min-width: 680px;
    }
    .matrix-table th, .matrix-table td {
      border: 1px solid var(--border);
      padding: 6px 5px;
      text-align: center;
    }
    .matrix-table th {
      background: #f8fafc;
      font-weight: 800;
      color: var(--text);
    }
    .matrix-table td.left-col { text-align: left; padding-left: 8px; }
    .x-mark {
      display: inline-block;
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 5px;
    }
    .video-frame-wrap {
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      border-radius: 12px;
      overflow: hidden;
      background: #0f172a;
      margin-bottom: 10px;
    }
    .video-frame-wrap iframe,
    .video-frame-wrap video {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
    }
    .video-placeholder {
      border: 1.5px dashed #cbd5e1;
      border-radius: 12px;
      padding: 20px 14px;
      text-align: center;
      background: #f8fafc;
      color: var(--muted);
      margin-bottom: 10px;
      font-size: 0.85rem;
    }
    .quiz-card {
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 11px 12px;
      margin-bottom: 10px;
      background: #f8fafc;
    }
    .quiz-q {
      font-weight: 700;
      font-size: 0.86rem;
      margin-bottom: 7px;
      color: var(--text);
    }
    .quiz-opt {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      font-size: 0.83rem;
      padding: 4px 0;
      cursor: pointer;
    }
    .quiz-result-banner {
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 0.84rem;
      font-weight: 700;
      margin-bottom: 12px;
    }
""" + "\n" + cert_css

old_mode_switch = """    <div class="mode-switch">
      <button id="btnModeDaily" class="mode-btn active" type="button">Registros Diarios</button>
      <button id="btnModeDocs" class="mode-btn" type="button">Base Documental</button>
    </div>"""

new_mode_switch = """    <div class="mode-switch-3" id="mainModeSwitch">
      <button id="btnModeDaily" class="mode-btn active" type="button">Registros Diarios</button>
      <button id="btnModeDocs" class="mode-btn" type="button">Base Documental</button>
      <button id="btnModeCap" class="mode-btn" type="button">Capacitaciones (R-02)</button>
    </div>"""

cap_section_html = """
    <!-- VISTA 3: CAPACITACIONES (R-02) -->
    <section id="viewCap" class="hidden">
      <div class="cap-subtabs" id="capSubTabs">
        <button class="cap-subtab active" data-capsub="cronograma" type="button">1. Cronograma Anual</button>
        <button class="cap-subtab" data-capsub="cursada" type="button">2. Video + Evaluación + Asistencia</button>
        <button class="cap-subtab" data-capsub="certificado" type="button">3. Certificado</button>
        <button class="cap-subtab" data-capsub="planilla" type="button">4. Planilla Asistencia (R-02)</button>
      </div>

      <div id="capsub-cronograma">
        <div class="panel-box">
          <h2 class="panel-title">Cronograma Anual de Capacitaciones</h2>
          <p style="font-size:0.82rem; color:var(--muted); margin:0 0 10px;">
            <strong>Disertante:</strong> Responsable de Calidad - Macarena Schischke. Filtrá por mes o seleccioná un tema para iniciar la capacitación, cargar su enlace de video y tomar asistencia.
          </p>
          <div class="month-filter-bar" id="monthFilterBar">
            <button class="m-chip active" data-mes="ALL" type="button">Todos los meses</button>
            <button class="m-chip" data-mes="ENE" type="button">ENE</button>
            <button class="m-chip" data-mes="FEB" type="button">FEB</button>
            <button class="m-chip" data-mes="MAR" type="button">MAR</button>
            <button class="m-chip" data-mes="ABR" type="button">ABR</button>
            <button class="m-chip" data-mes="MAY" type="button">MAY</button>
            <button class="m-chip" data-mes="JUN" type="button">JUN</button>
            <button class="m-chip" data-mes="JUL" type="button">JUL</button>
            <button class="m-chip" data-mes="AGO" type="button">AGO</button>
            <button class="m-chip" data-mes="SEP" type="button">SEP</button>
            <button class="m-chip" data-mes="OCT" type="button">OCT</button>
            <button class="m-chip" data-mes="NOV" type="button">NOV</button>
            <button class="m-chip" data-mes="DIC" type="button">DIC</button>
          </div>
          <div id="topicsCardsList"></div>
        </div>

        <div class="panel-box">
          <h2 class="panel-title">Matriz Anual Completa</h2>
          <div class="matrix-wrap">
            <table class="matrix-table" id="matrixTable"></table>
          </div>
        </div>
      </div>

      <div id="capsub-cursada" class="hidden">
        <div class="panel-box">
          <h2 class="panel-title">Capacitación, Video y Evaluación</h2>
          <div class="form-group">
            <label class="form-label" for="selTema">Tema de capacitación</label>
            <select id="selTema" class="form-control"></select>
          </div>
          <div id="temaMetaBox" class="rule-banner"></div>

          <div id="videoViewerArea"></div>

          <details style="margin-bottom:14px;">
            <summary class="btn-secondary" style="display:inline-block; cursor:pointer; list-style:none;">
              Configurar / pegar enlace del video
            </summary>
            <div style="margin-top:10px; padding:12px; border:1px solid var(--border); border-radius:10px; background:#f8fafc;">
              <div class="form-group">
                <label class="form-label" for="inputVideoUrl">Enlace de YouTube, Google Drive o archivo de video (.mp4 / .webm)</label>
                <input id="inputVideoUrl" type="url" class="form-control" placeholder="https://www.youtube.com/watch?v=... o enlace de Drive" />
              </div>
              <button id="btnSaveVideoUrl" class="btn-secondary" type="button">Guardar enlace del tema</button>
            </div>
          </details>

          <div class="form-group">
            <label class="check-row" style="background:#fff; cursor:pointer;">
              <input id="chkEvaluacionExterna" type="checkbox" />
              <span>Evaluación realizada en formulario externo / impreso (omitir cuestionario en pantalla)</span>
            </label>
          </div>

          <div id="quizSection">
            <div id="quizQuestionsContainer"></div>
            <div id="quizResultBanner" class="quiz-result-banner hidden"></div>
            <button id="btnCorregirQuiz" class="btn-secondary" type="button" style="margin-bottom:14px;">
              Corregir evaluación (mínimo 75%)
            </button>
          </div>

          <div id="externalEvalBox" class="hidden" style="padding:12px; border:1px solid var(--border); border-radius:10px; background:#f8fafc; margin-bottom:14px;">
            <div class="form-row-2">
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label" for="extNota">Calificación / Resultado</label>
                <input id="extNota" type="text" class="form-control" placeholder="Ej: Aprobado 90%" />
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label" for="extEficacia">Verificación de eficacia (R-02)</label>
                <select id="extEficacia" class="form-control">
                  <option value="Eficaz">Eficaz</option>
                  <option value="Requiere refuerzo">Requiere refuerzo</option>
                  <option value="No eficaz">No eficaz</option>
                </select>
              </div>
            </div>
          </div>

          <div style="border-top:1px solid var(--border); padding-top:14px;">
            <h3 class="panel-title">Registro de Asistencia y Emisión de Certificado</h3>
            <div class="form-row-2">
              <div class="form-group">
                <label class="form-label" for="asistNombre">Nombre y Apellido *</label>
                <input id="asistNombre" type="text" class="form-control" placeholder="Ej: Juan Pérez" />
              </div>
              <div class="form-group">
                <label class="form-label" for="asistDni">DNI *</label>
                <input id="asistDni" type="text" class="form-control" placeholder="Ej: 30123456" />
              </div>
            </div>
            <div class="form-row-2">
              <div class="form-group">
                <label class="form-label" for="asistSector">Sector / Puesto</label>
                <input id="asistSector" type="text" class="form-control" placeholder="Ej: Playa Faena / Despostada" />
              </div>
              <div class="form-group">
                <label class="form-label" for="asistObs">Observación</label>
                <input id="asistObs" type="text" class="form-control" placeholder="Opcional" />
              </div>
            </div>
            <div class="form-row-2">
              <div class="form-group">
                <label class="form-label" for="asistFecha">Fecha</label>
                <input id="asistFecha" type="text" class="form-control" readonly />
              </div>
              <div class="form-group">
                <label class="form-label" for="asistHora">Hora</label>
                <input id="asistHora" type="text" class="form-control" readonly />
              </div>
            </div>
            <button id="btnRegistrarAsistencia" class="btn-primary" type="button">
              Registrar Asistencia y Generar Certificado
            </button>
          </div>
        </div>
      </div>

      <div id="capsub-certificado" class="hidden">
        <div class="panel-box no-print">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
            <div style="flex:1; min-width:220px;">
              <label class="form-label" for="selCertRegistro">Seleccionar certificado emitido</label>
              <select id="selCertRegistro" class="form-control"></select>
            </div>
            <button type="button" class="btn-primary" style="width:auto; padding:10px 16px;" onclick="window.print()">
              Imprimir / Guardar PDF (A4)
            </button>
          </div>
        </div>

        <div class="cert-sheet-wrap">
          <div id="certSheetContent" class="cert-sheet"></div>
        </div>
      </div>

      <div id="capsub-planilla" class="hidden">
        <div class="panel-box">
          <h2 class="panel-title">Planilla de Asistencia y Eficacia (R-02)</h2>
          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label" for="filterPlanillaTema">Filtrar por tema</label>
              <select id="filterPlanillaTema" class="form-control"></select>
            </div>
            <div class="form-group">
              <label class="form-label" for="filterPlanillaSearch">Buscar asistente / DNI / fecha</label>
              <input id="filterPlanillaSearch" type="search" class="form-control" placeholder="Nombre, DNI, sector o fecha..." />
            </div>
          </div>
          <div class="toolbar-export">
            <button id="btnExportAsistCsv" class="btn-secondary" type="button">Descargar Asistencia CSV</button>
            <button id="btnExportAsistJson" class="btn-secondary" type="button">Respaldo Asistencia JSON</button>
          </div>
          <div id="asistenciasListContainer"></div>
        </div>
      </div>
    </section>
"""

cap_js = """
    const STORAGE_ASIST_KEY = "agrotres_capacitaciones_asistencia_v1";
    const STORAGE_VIDEOS_KEY = "agrotres_capacitaciones_videos_v1";
    const MESES_ORDEN = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"];

    Object.assign(state, {
      capSub: "cronograma",
      mesFiltro: "ALL",
      temaActivoId: "CAP-01",
      quizAprobado: false,
      quizPuntajeTexto: "",
      certSelectedUid: ""
    });

    function todayAR() {
      return todayISO().split("-").reverse().join("/");
    }

    const _memAsist = [];
    const _memVideos = {};

    function getVideoOverrides() {
      try {
        return JSON.parse(localStorage.getItem(STORAGE_VIDEOS_KEY) || "null") || Object.assign({}, _memVideos);
      } catch (e) {
        return Object.assign({}, _memVideos);
      }
    }

    function saveVideoOverride(temaId, url) {
      _memVideos[temaId] = url;
      try {
        const cur = getVideoOverrides();
        cur[temaId] = url;
        localStorage.setItem(STORAGE_VIDEOS_KEY, JSON.stringify(cur));
      } catch (e) {}
    }

    function getCapacitaciones() {
      const overrides = getVideoOverrides();
      return CAPACITACIONES_BASE.map(c => ({
        ...c,
        video_url: overrides[c.id] !== undefined ? overrides[c.id] : c.video_url
      }));
    }

    function getAsistencias() {
      try {
        return JSON.parse(localStorage.getItem(STORAGE_ASIST_KEY) || "null") || _memAsist.slice();
      } catch (e) {
        return _memAsist.slice();
      }
    }

    function saveAsistencias(list) {
      _memAsist.length = 0;
      _memAsist.push(...list);
      try {
        localStorage.setItem(STORAGE_ASIST_KEY, JSON.stringify(list));
      } catch (e) {}
    }

    function buildEmbedHtml(url, nota) {
      if (!url || !url.trim()) {
        return `
          <div class="video-placeholder">
            <strong>Video pendiente de enlace</strong><br/>
            <span>${nota}</span><br/>
            <span style="font-size:0.78rem;">Abrí <em>"Configurar / pegar enlace del video"</em> abajo para vincular el video de YouTube o Google Drive.</span>
          </div>
        `;
      }
      const clean = url.trim();
      const ytMatch = clean.match(/(?:youtube\\.com\\/(?:watch\\?v=|embed\\/|shorts\\/)|youtu\\.be\\/)([a-zA-Z0-9_-]{11})/);
      if (ytMatch) {
        return `
          <div class="video-frame-wrap">
            <iframe src="https://www.youtube.com/embed/${ytMatch[1]}" allowfullscreen title="Video capacitación"></iframe>
          </div>
        `;
      }
      const gdMatch = clean.match(/drive\\.google\\.com\\/file\\/d\\/([a-zA-Z0-9_-]+)/);
      if (gdMatch) {
        return `
          <div class="video-frame-wrap">
            <iframe src="https://drive.google.com/file/d/${gdMatch[1]}/preview" allow="autoplay" title="Video capacitación Drive"></iframe>
          </div>
        `;
      }
      if (/\\.(mp4|webm|ogg)(\\?.*)?$/i.test(clean)) {
        return `
          <div class="video-frame-wrap">
            <video controls src="${clean}"></video>
          </div>
        `;
      }
      return `
        <div class="video-placeholder">
          <a href="${clean}" target="_blank" rel="noopener noreferrer" class="btn-secondary" style="display:inline-block; text-decoration:none;">
            ▶ Abrir video de capacitación en nueva pestaña
          </a>
        </div>
      `;
    }

    function renderCapCronograma() {
      const caps = getCapacitaciones();
      const asist = getAsistencias();
      const filtradas = state.mesFiltro === "ALL"
        ? caps
        : caps.filter(c => c.meses.includes(state.mesFiltro));

      document.getElementById("topicsCardsList").innerHTML = filtradas.map(c => {
        const countAsist = asist.filter(a => a.tema_id === c.id).length;
        const hasVid = Boolean(c.video_url && c.video_url.trim());
        return `
          <div class="topic-card">
            <div class="topic-head">
              <div>
                <div class="topic-title">${c.tema}</div>
                <div style="font-size:0.78rem; color:var(--muted); margin-top:2px;">
                  <strong>Destinatarios:</strong> ${c.destinatarios}
                </div>
              </div>
              <span class="badge ${hasVid ? 'b-ok' : 'b-warn'}">${hasVid ? 'Video cargado' : 'Sin enlace video'}</span>
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:5px; margin:8px 0;">
              ${c.meses.map(m => `<span class="badge b-info">${m}</span>`).join("")}
              <span class="badge" style="background:#f1f5f9; color:#334155;">Asistentes: ${countAsist}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-top:8px; padding-top:8px; border-top:1px solid var(--border);">
              <span style="font-size:0.75rem; color:var(--muted);">${c.entidad}</span>
              <button class="btn-secondary" type="button" onclick="iniciarTemaCap('${c.id}')">Abrir capacitación →</button>
            </div>
          </div>
        `;
      }).join("");

      const headRow = `
        <tr>
          <th style="text-align:left; padding-left:10px;">Actividad / Tema</th>
          ${MESES_ORDEN.map(m => `<th>${m}</th>`).join("")}
          <th>Personal Destinado</th>
        </tr>
      `;
      const bodyRows = caps.map(c => `
        <tr>
          <td class="left-col"><strong>${c.tema}</strong></td>
          ${MESES_ORDEN.map(m => `<td>${c.meses.includes(m) ? '<span class="x-mark">X</span>' : ''}</td>`).join("")}
          <td class="left-col" style="font-size:0.74rem;">${c.destinatarios}</td>
        </tr>
      `).join("");

      document.getElementById("matrixTable").innerHTML = `<thead>${headRow}</thead><tbody>${bodyRows}</tbody>`;
    }

    function populateCapSelectors() {
      const caps = getCapacitaciones();
      const sel = document.getElementById("selTema");
      sel.innerHTML = caps.map(c => `<option value="${c.id}">${c.tema}</option>`).join("");
      sel.value = state.temaActivoId;

      const filterPlan = document.getElementById("filterPlanillaTema");
      const prevVal = filterPlan.value || "ALL";
      filterPlan.innerHTML = `<option value="ALL">Todos los temas</option>` +
        caps.map(c => `<option value="${c.id}">${c.tema}</option>`).join("");
      filterPlan.value = prevVal;
    }

    function renderCapCursada() {
      const caps = getCapacitaciones();
      const tema = caps.find(c => c.id === state.temaActivoId) || caps[0];
      state.temaActivoId = tema.id;
      state.quizAprobado = false;
      state.quizPuntajeTexto = "";

      document.getElementById("temaMetaBox").innerHTML = `
        <strong>Disertante:</strong> ${tema.entidad} · <strong>Meses cronograma:</strong> ${tema.meses.join(", ")} · <strong>Destinatarios:</strong> ${tema.destinatarios}
      `;
      document.getElementById("inputVideoUrl").value = tema.video_url || "";
      document.getElementById("videoViewerArea").innerHTML = buildEmbedHtml(tema.video_url, tema.video_nota);

      document.getElementById("asistFecha").value = todayAR();
      document.getElementById("asistHora").value = nowTime();

      const qContainer = document.getElementById("quizQuestionsContainer");
      qContainer.innerHTML = tema.preguntas.map((item, idx) => `
        <div class="quiz-card">
          <div class="quiz-q">${idx + 1}. ${item.q}</div>
          ${item.opts.map((opt, oIdx) => `
            <label class="quiz-opt">
              <input type="radio" name="q_${idx}" value="${oIdx}" />
              <span>${opt}</span>
            </label>
          `).join("")}
        </div>
      `).join("");

      const resBanner = document.getElementById("quizResultBanner");
      resBanner.classList.add("hidden");
      resBanner.textContent = "";
    }

    function renderCapCertificado() {
      const asist = getAsistencias();
      const sel = document.getElementById("selCertRegistro");
      const sheet = document.getElementById("certSheetContent");

      if (!asist.length) {
        sel.innerHTML = `<option value="">Sin asistentes registrados aún</option>`;
        sheet.innerHTML = `
          <div class="cert-top-bar"></div>
          <div class="cert-corner-tl"></div>
          <div class="cert-corner-br"></div>
          <div style="padding:28px 16px; color:var(--muted);">
            <div class="cert-header">Frigorífico Agrotres S.A. · Establecimiento Oficial N.º 5258</div>
            <div class="cert-main-title" style="margin-top:10px;">Certificado de Asistencia y Aprobación</div>
            <p style="margin:12px auto 0; max-width:560px; font-size:0.92rem;">
              Todavía no hay certificados emitidos.<br/>
              Completá la evaluación y el formulario de asistencia en <strong>"2. Video + Evaluación + Asistencia"</strong> para generar el certificado en tamaño A4.
            </p>
          </div>
        `;
        return;
      }

      sel.innerHTML = asist.map(a =>
        `<option value="${a.uid}">${a.nombre} (DNI ${a.dni}) — ${a.tema_nombre} (${a.fecha})</option>`
      ).join("");

      if (state.certSelectedUid && asist.some(a => a.uid === state.certSelectedUid)) {
        sel.value = state.certSelectedUid;
      } else {
        state.certSelectedUid = asist[0].uid;
        sel.value = state.certSelectedUid;
      }

      const reg = asist.find(a => a.uid === state.certSelectedUid) || asist[0];

      sheet.innerHTML = `
        <div class="cert-top-bar"></div>
        <div class="cert-corner-tl"></div>
        <div class="cert-corner-br"></div>

        <div>
          <div class="cert-emblem" aria-hidden="true">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <div class="cert-header">Frigorífico Agrotres S.A. · Establecimiento Oficial N.º 5258</div>
          <div class="cert-sub">Sistema de Gestión de Calidad e Inocuidad Alimentaria · Programa Anual de Capacitación (R-02)</div>
          <div class="cert-divider"></div>
          <div class="cert-main-title">Certificado de Asistencia y Aprobación</div>
        </div>

        <div>
          <div class="cert-body">
            Se certifica por la presente que<br/>
            <div class="cert-name">${reg.nombre}</div><br/>
            <strong>DNI N.º ${reg.dni}</strong>${reg.sector ? ` · Sector: <strong>${reg.sector}</strong>` : ""}<br/>
            ha participado y aprobado satisfactoriamente la capacitación interna correspondiente al Cronograma Anual sobre:
          </div>

          <div class="cert-topic-box">
            ${reg.tema_nombre}
          </div>

          <div class="cert-meta-pills">
            <span class="cert-meta-pill"><strong>Fecha:</strong> ${reg.fecha}</span>
            <span class="cert-meta-pill"><strong>Evaluación:</strong> ${reg.resultado_eval}</span>
            <span class="cert-meta-pill"><strong>Verificación R-02:</strong> ${reg.eficacia}</span>
          </div>
        </div>

        <div>
          <div class="cert-signs">
            <div>
              <div class="sign-line">
                <strong>Lic. Macarena Schischke</strong><br/>
                Responsable de Calidad · Est. Oficial N.º 5258
              </div>
            </div>
            <div class="cert-seal">
              <span>AGROTRES</span>
              <span>EST. 5258</span>
              <span>CALIDAD</span>
            </div>
            <div>
              <div class="sign-line">
                <strong>Firma del Asistente</strong><br/>
                ${reg.nombre} · DNI ${reg.dni}
              </div>
            </div>
          </div>
          <div class="cert-footer-code">
            Documento generado desde el Sistema de Capacitaciones R-02 · Frigorífico Agrotres S.A. · Código: ${reg.tema_id}-${reg.uid.slice(-5)}
          </div>
        </div>
      `;
    }

    function renderCapPlanilla() {
      const container = document.getElementById("asistenciasListContainer");
      let list = getAsistencias();
      const temaFilter = document.getElementById("filterPlanillaTema").value;
      const q = document.getElementById("filterPlanillaSearch").value.trim().toLowerCase();

      if (temaFilter && temaFilter !== "ALL") {
        list = list.filter(a => a.tema_id === temaFilter);
      }
      if (q) {
        list = list.filter(a =>
          [a.nombre, a.dni, a.fecha, a.tema_nombre, a.sector].join(" ").toLowerCase().includes(q)
        );
      }

      if (!list.length) {
        container.innerHTML = `<p style="text-align:center; color:var(--muted); font-size:0.86rem; padding:12px 0;">No hay registros de asistencia para mostrar.</p>`;
        return;
      }

      container.innerHTML = list.map(a => `
        <div class="topic-card">
          <div class="topic-head">
            <div>
              <strong>${a.nombre}</strong> · <span style="color:var(--primary); font-weight:700;">DNI ${a.dni}</span>
              <div style="font-size:0.8rem; color:var(--muted);">${a.tema_nombre}</div>
            </div>
            <span class="badge b-ok">${a.resultado_eval}</span>
          </div>
          <div style="font-size:0.78rem; color:var(--muted); margin-top:4px;">
            Fecha: <strong>${a.fecha}</strong> (${a.hora} hs) ${a.sector ? `· Sector: ${a.sector}` : ""} · Eficacia R-02: ${a.eficacia}
          </div>
          ${a.observacion ? `<div style="font-size:0.78rem; color:var(--muted); margin-top:2px;">Obs: ${a.observacion}</div>` : ""}
          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:8px;">
            <button class="btn-secondary" type="button" onclick="verCertificadoCap('${a.uid}')">Ver Certificado</button>
            <button class="btn-danger-sm" type="button" onclick="eliminarAsistenciaCap('${a.uid}')">Eliminar</button>
          </div>
        </div>
      `).join("");
    }

    function switchCapSub(subName) {
      state.capSub = subName;
      document.querySelectorAll("#capSubTabs .cap-subtab").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.capsub === subName);
      });
      ["cronograma", "cursada", "certificado", "planilla"].forEach(s => {
        document.getElementById("capsub-" + s).classList.toggle("hidden", s !== subName);
      });
      if (subName === "cronograma") renderCapCronograma();
      if (subName === "cursada") renderCapCursada();
      if (subName === "certificado") renderCapCertificado();
      if (subName === "planilla") renderCapPlanilla();
    }

    window.iniciarTemaCap = function (temaId) {
      state.temaActivoId = temaId;
      document.getElementById("selTema").value = temaId;
      switchCapSub("cursada");
    };

    window.verCertificadoCap = function (uid) {
      state.certSelectedUid = uid;
      switchCapSub("certificado");
    };

    window.eliminarAsistenciaCap = function (uid) {
      saveAsistencias(getAsistencias().filter(a => a.uid !== uid));
      renderCapPlanilla();
      showToast("Registro de asistencia eliminado");
    };

    document.getElementById("capSubTabs").addEventListener("click", e => {
      const btn = e.target.closest(".cap-subtab");
      if (!btn) return;
      switchCapSub(btn.dataset.capsub);
    });

    document.getElementById("monthFilterBar").addEventListener("click", e => {
      const chip = e.target.closest(".m-chip");
      if (!chip) return;
      state.mesFiltro = chip.dataset.mes;
      document.querySelectorAll("#monthFilterBar .m-chip").forEach(c => c.classList.toggle("active", c === chip));
      renderCapCronograma();
    });

    document.getElementById("selTema").addEventListener("change", e => {
      state.temaActivoId = e.target.value;
      renderCapCursada();
    });

    document.getElementById("btnSaveVideoUrl").addEventListener("click", () => {
      const url = document.getElementById("inputVideoUrl").value.trim();
      saveVideoOverride(state.temaActivoId, url);
      renderCapCursada();
      showToast("Enlace de video actualizado");
    });

    document.getElementById("chkEvaluacionExterna").addEventListener("change", e => {
      const ext = e.target.checked;
      document.getElementById("quizSection").classList.toggle("hidden", ext);
      document.getElementById("externalEvalBox").classList.toggle("hidden", !ext);
    });

    document.getElementById("btnCorregirQuiz").addEventListener("click", () => {
      const caps = getCapacitaciones();
      const tema = caps.find(c => c.id === state.temaActivoId);
      if (!tema) return;

      let correctas = 0;
      let sinResponder = 0;
      tema.preguntas.forEach((p, idx) => {
        const checked = document.querySelector(`input[name="q_${idx}"]:checked`);
        if (!checked) {
          sinResponder++;
        } else if (parseInt(checked.value, 10) === p.ok) {
          correctas++;
        }
      });

      const banner = document.getElementById("quizResultBanner");
      banner.classList.remove("hidden");

      if (sinResponder > 0) {
        banner.style.background = "#fef3c7";
        banner.style.color = "#92400e";
        banner.textContent = `Faltan responder ${sinResponder} pregunta(s) antes de corregir.`;
        return;
      }

      const total = tema.preguntas.length;
      const pct = Math.round((correctas / total) * 100);
      const aprobado = pct >= 75;

      state.quizAprobado = aprobado;
      state.quizPuntajeTexto = `Aprobado (${correctas}/${total} · ${pct}%)`;

      if (aprobado) {
        banner.style.background = "#dcfce7";
        banner.style.color = "#166534";
        banner.textContent = `✓ Evaluación APROBADA: ${correctas} de ${total} respuestas correctas (${pct}%). Ya podés completar la asistencia y emitir el certificado.`;
      } else {
        banner.style.background = "#fee2e2";
        banner.style.color = "#991b1b";
        banner.textContent = `✕ No alcanzó el mínimo (75%): ${correctas} de ${total} (${pct}%). Revisá el video y volvé a intentar.`;
      }
    });

    document.getElementById("btnRegistrarAsistencia").addEventListener("click", () => {
      const nombre = document.getElementById("asistNombre").value.trim();
      const dni = document.getElementById("asistDni").value.trim();
      const sector = document.getElementById("asistSector").value.trim();
      const obs = document.getElementById("asistObs").value.trim();
      const esExterna = document.getElementById("chkEvaluacionExterna").checked;

      if (!nombre || !dni) {
        showToast("Completá Nombre y Apellido y DNI");
        return;
      }

      if (!esExterna && !state.quizAprobado) {
        showToast("Primero aprobá la evaluación (o marcá evaluación externa)");
        return;
      }

      const caps = getCapacitaciones();
      const tema = caps.find(c => c.id === state.temaActivoId);

      const resultadoEval = esExterna
        ? (document.getElementById("extNota").value.trim() || "Aprobado")
        : state.quizPuntajeTexto;

      const eficacia = esExterna
        ? document.getElementById("extEficacia").value
        : "Eficaz";

      const nuevoReg = {
        uid: String(Date.now()),
        fecha: todayAR(),
        hora: nowTime(),
        tema_id: tema.id,
        tema_nombre: tema.tema,
        disertante: tema.entidad,
        nombre,
        dni,
        sector,
        resultado_eval: resultadoEval,
        eficacia,
        observacion: obs
      };

      const list = getAsistencias();
      list.unshift(nuevoReg);
      saveAsistencias(list);

      document.getElementById("asistNombre").value = "";
      document.getElementById("asistDni").value = "";
      document.getElementById("asistSector").value = "";
      document.getElementById("asistObs").value = "";

      state.certSelectedUid = nuevoReg.uid;
      showToast("Asistencia registrada y certificado generado");
      switchCapSub("certificado");
    });

    document.getElementById("selCertRegistro").addEventListener("change", e => {
      state.certSelectedUid = e.target.value;
      renderCapCertificado();
    });

    document.getElementById("filterPlanillaTema").addEventListener("change", renderCapPlanilla);
    document.getElementById("filterPlanillaSearch").addEventListener("input", renderCapPlanilla);

    document.getElementById("btnExportAsistCsv").addEventListener("click", () => {
      const list = getAsistencias();
      if (!list.length) {
        showToast("No hay asistencias registradas para exportar");
        return;
      }
      const headers = [
        "Fecha", "Hora", "Tema_Capacitacion", "Disertante",
        "Nombre_y_Apellido", "DNI", "Sector", "Evaluacion", "Eficacia_R02", "Observacion"
      ];
      const rows = list.map(a => [
        a.fecha, a.hora, a.tema_nombre, a.disertante,
        a.nombre, a.dni, a.sector, a.resultado_eval, a.eficacia, a.observacion
      ].map(v => `"${String(v || "").replace(/"/g, '""')}"`).join(";"));

      const csv = "\\uFEFF" + [headers.join(";"), ...rows].join("\\n");
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `agrotres-asistencia-R02-${todayISO()}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    });

    document.getElementById("btnExportAsistJson").addEventListener("click", () => {
      const payload = {
        establecimiento: "Frigorífico Agrotres S.A. - Est. Oficial N.º 5258",
        registro: "R-02 Capacitaciones y Verificación de Eficacia",
        exportado: new Date().toISOString(),
        asistencias: getAsistencias()
      };
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `agrotres-capacitaciones-R02-${todayISO()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    });
"""

assert old_mode_switch in base_html, "old_mode_switch not found"
assert "</style>" in base_html, "</style> not found"
assert "</section>\n  </main>" in base_html, "</section> main not found"

init_anchor = "    const hoy = todayISO();"
assert init_anchor in base_html, "init_anchor not found"

out_html = base_html.replace("</style>", cap_extra_css + "\n  </style>", 1)
out_html = out_html.replace(old_mode_switch, new_mode_switch, 1)
out_html = out_html.replace("</section>\n  </main>", "</section>\n" + cap_section_html + "\n  </main>", 1)

old_switch_mode = """    function switchMode(mode) {
      state.mode = mode;
      document.getElementById("btnModeDocs").classList.toggle("active", mode === "docs");
      document.getElementById("btnModeDaily").classList.toggle("active", mode === "daily");
      document.getElementById("viewDocs").classList.toggle("hidden", mode !== "docs");
      document.getElementById("viewDaily").classList.toggle("hidden", mode !== "daily");

      if (mode === "daily") {
        populateRegSelect();
        renderLogs();
      } else {
        renderDocsList();
      }
    }"""

new_switch_mode = """    function switchMode(mode) {
      state.mode = mode;
      document.getElementById("btnModeDaily").classList.toggle("active", mode === "daily");
      document.getElementById("btnModeDocs").classList.toggle("active", mode === "docs");
      document.getElementById("btnModeCap").classList.toggle("active", mode === "cap");
      document.getElementById("viewDaily").classList.toggle("hidden", mode !== "daily");
      document.getElementById("viewDocs").classList.toggle("hidden", mode !== "docs");
      document.getElementById("viewCap").classList.toggle("hidden", mode !== "cap");

      if (mode === "daily") {
        populateRegSelect();
        renderLogs();
      } else if (mode === "docs") {
        renderDocsList();
      } else if (mode === "cap") {
        populateCapSelectors();
        switchCapSub(state.capSub || "cronograma");
      }
    }"""

assert old_switch_mode in out_html, "old_switch_mode not found"
out_html = out_html.replace(old_switch_mode, new_switch_mode, 1)
out_html = out_html.replace(
    'document.getElementById("btnModeDaily").addEventListener("click", () => switchMode("daily"));',
    'document.getElementById("btnModeDaily").addEventListener("click", () => switchMode("daily"));\n    document.getElementById("btnModeCap").addEventListener("click", () => switchMode("cap"));',
    1
)

out_html = out_html.replace(init_anchor, cap_base_decl + "\n" + cap_js + "\n" + init_anchor, 1)

out_filename = "agrotres-sgc-integrado-v2.html"
with open(out_filename, "w", encoding="utf-8") as f:
    f.write(out_html)

print("Successfully generated:", out_filename, "Size:", len(out_html))