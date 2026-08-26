from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tg">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Choryak Platform</title>

<style>
:root{
    --sidebar-bg: #0B192C;
    --main-bg: #0B192C;
    --card-bg: #102238;
    --text-white: #FFFFFF;
    --text-muted: #9FB3C8;
    --green: #10B981;
    --green-hover: #059669;
    --green-soft: rgba(16, 185, 129, 0.15);
    --border: rgba(255, 255, 255, 0.08);
    --red: #EF4444;
    --red-hover: #DC2626;
}

[data-theme="light"] {
    --sidebar-bg: #F8FAFC;
    --main-bg: #F1F5F9;
    --card-bg: #FFFFFF;
    --text-white: #0F172A;
    --text-muted: #64748B;
    --border: rgba(0, 0, 0, 0.08);
}

*{ box-sizing:border-box; }
body{ 
    margin:0; 
    background-color: var(--main-bg);
    color: var(--text-white); 
    font-family: "Segoe UI", Arial, sans-serif; 
}

.sidebar{ position:fixed; left:0; top:0; bottom:0; width:260px; background: var(--sidebar-bg); color:var(--text-white); padding:25px 18px; z-index:100; overflow-y:auto; border-right:1px solid var(--border); transition: width 0.3s ease, padding 0.3s ease; }
.sidebar.collapsed { width: 75px; padding: 25px 10px; }
.sidebar.collapsed .logo-sub,
.sidebar.collapsed .menu-title,
.sidebar.collapsed .menu span,
.sidebar.collapsed .logo-title { display: none; }
.sidebar.collapsed .logo-title-collapsed { display: block !important; font-size: 20px; font-weight: 800; text-align: center; color: var(--green); }

.logo-title-collapsed { display: none; }
.logo-area { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.toggle-btn { background: rgba(128,128,128,0.15); border: none; color: var(--text-white); width: 32px; height: 32px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; }
.toggle-btn:hover { background: rgba(128,128,128,0.25); }

.logo-title{ margin:0; font-size:22px; font-weight:800; letter-spacing:1px; color:var(--text-white); }
.logo-sub{ color:var(--green); font-weight:800; letter-spacing:2px; margin-top:3px; font-size:11px; }
.menu-title{ color:var(--text-muted); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin:25px 12px 8px; }
.menu{ width:100%; display:flex; align-items:center; border:0; background:transparent; color:var(--text-muted); text-align:left; padding:12px 14px; margin:4px 0; border-radius:8px; cursor:pointer; font-size:14px; font-weight:600; transition:.15s; }
.menu:hover{ background:rgba(128,128,128,0.1); color:var(--text-white); }
.menu.active{ background:var(--green-soft); color:var(--green); }

.main{ margin-left:260px; min-height:100vh; background-color: var(--main-bg); transition: margin-left 0.3s ease; }
.main.expanded { margin-left: 75px; }

.topbar{ height:65px; background: var(--sidebar-bg); border-bottom:1px solid var(--border); display:flex; align-items:center; justify-content:space-between; padding:0 30px; position:sticky; top:0; z-index:50; }
.top-title{ font-size:18px; font-weight:800; color:var(--text-white); }
.top-right-group { display: flex; align-items: center; gap: 10px; }
.platform-status{ background:var(--green-soft); color:var(--green); border:1px solid rgba(16,185,129,0.3); padding:7px 14px; border-radius:7px; font-size:12px; font-weight:700; }
.theme-toggle-btn { background: rgba(128,128,128,0.15); border: none; color: var(--text-white); padding: 7px 12px; border-radius: 7px; cursor: pointer; font-size: 12px; font-weight: 700; }

.content{ max-width:1300px; margin:auto; padding:30px; }
.page{ display:none; }
.page.active{ display:block; animation: fadeIn 0.3s ease-in-out; }
.card{ background:var(--card-bg); border:1px solid var(--border); border-radius:10px; box-shadow:0 4px 20px rgba(0,0,0,0.1); padding:28px; margin-bottom:20px; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}

.field{ margin-bottom:18px; }
.field label{ display:block; margin-bottom:7px; font-size:13px; font-weight:800; color:var(--text-muted); }
input, select, textarea{ width:100%; padding:13px; background:var(--main-bg); border:1px solid var(--border); border-radius:7px; outline:none; font-size:14px; color:var(--text-white); }
input:focus, select:focus, textarea:focus{ border-color:var(--green); }
textarea{ resize:vertical; min-height:80px; }

.scan-button{ width:100%; margin-top:10px; padding:14px; border:0; border-radius:7px; background:var(--green); color:#FFFFFF; font-size:14px; font-weight:900; cursor:pointer; transition:.15s; box-shadow:0 2px 8px rgba(16,185,129,0.4); }
.scan-button:hover{ background:var(--green-hover); }

.delete-btn { background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); color: var(--red); width: 32px; height: 32px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; transition: 0.15s; }
.delete-btn:hover { background: var(--red); color: white; }

.question-card{ background:var(--main-bg); border:1px solid var(--border); padding:20px; border-radius:8px; margin-bottom:15px; }
.option-btn{ display:block; width:100%; text-align:left; padding:10px 14px; margin:6px 0; background:var(--card-bg); border:1px solid var(--border); border-radius:6px; cursor:pointer; font-size:13px; font-weight:600; color:var(--text-white); transition:all 0.2s; }
.option-btn:hover{ border-color:var(--green); }
.option-btn.selected-opt{ background:var(--green-soft); border-color:var(--green); color:var(--green); }

.test-item-card { background:var(--main-bg); border:1px solid var(--border); padding:18px; border-radius:8px; margin-bottom:15px; }
.test-meta { display:flex; justify-content:space-between; align-items:center; font-size:13px; color:var(--text-muted); border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:10px; }
.test-variants { font-size:13px; color:var(--text-muted); margin-top:6px; display:grid; grid-template-columns: 1fr 1fr; gap:5px; }

.books-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 15px; margin-top: 15px; }
.book-card { background: var(--main-bg); border: 1px solid var(--border); border-radius: 8px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between; }
.book-title { font-size: 15px; font-weight: 700; margin-bottom: 6px; color: var(--text-white); }
.book-info { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }
.book-actions { display: flex; gap: 8px; }
.book-btn { flex: 1; padding: 8px; text-align: center; border-radius: 6px; font-size: 12px; font-weight: 700; text-decoration: none; cursor: pointer; border: none; }
.read-btn { background: var(--green-soft); color: var(--green); }
.read-btn:hover { background: var(--green); color: #fff; }

.pdf-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 1000; flex-direction: column; }
.pdf-modal-header { background: var(--sidebar-bg); padding: 12px 25px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); }
.close-modal-btn { background: var(--red); color: white; border: none; padding: 6px 14px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; }

.timer-control-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(239, 68, 68, 0.1);
    padding: 12px 18px;
    border-radius: 8px;
    border: 1px solid rgba(239, 68, 68, 0.2);
    margin-bottom: 20px;
}
.timer-box { font-size: 15px; font-weight: bold; color: var(--red); }
.start-test-btn {
    background: var(--green);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 13px;
    cursor: pointer;
}

/* Фақат барои экранҳои хеле хурди телефони мобилӣ (зери 500px) */
@media(max-width: 500px){
    .sidebar { position: relative; width: 100%; height: auto; border-right: none; border-bottom: 1px solid var(--border); }
    .main { margin-left: 0 !important; }
    .content { padding: 15px; }
    .topbar { padding: 0 15px; flex-direction: column; height: auto; gap: 8px; padding-top: 10px; padding-bottom: 10px; }
}
</style>
</head>
<body data-theme="dark">

<aside class="sidebar" id="sidebar">
    <div class="logo-area">
        <div>
            <div class="logo-title">CHORYAK</div>
            <div class="logo-title-collapsed">C</div>
            <div class="logo-sub">PLATFORM</div>
        </div>
        <button class="toggle-btn" onclick="toggleSidebar()" title="Кушоду баста кардан">🗜️</button>
    </div>

    <div class="menu-title">Асосӣ</div>
    <button class="menu active" onclick="openPage('home',this)">🏠 &nbsp; <span>Саҳифаи асосӣ</span></button>
    <button class="menu" onclick="openPage('testListSection',this)">📋 &nbsp; <span>Рӯйхати тестҳо</span></button>
    <button class="menu" onclick="openPage('historySection',this)">📊 &nbsp; <span>Таърихи натиҷаҳо</span></button>

    <div class="menu-title">Идоракунӣ</div>
    <button class="menu" onclick="requestPasswordForScanner(this)">➕ &nbsp; <span>Ҷои саволҳо (Илова)</span></button>
    <button class="menu" onclick="openPage('books',this)">📚 &nbsp; <span>Китобҳои дарсӣ</span></button>
</aside>

<main class="main" id="mainArea">
    <header class="topbar">
        <div id="topTitle" class="top-title">Низомномаи Синфҳо ва Тестҳо</div>
        <div class="top-right-group">
            <button class="theme-toggle-btn" onclick="toggleTheme()" id="themeBtn">☀️ Рӯшноӣ</button>
            <div class="platform-status">● Низоми рамзгузоришуда фаъол аст</div>
        </div>
    </header>

    <div class="content">
        <section id="home" class="page active">
            <div class="card">
                <h2>🔍 Интихоби Синф, Чоряк ва Номи Фан</h2>
                <p style="color:var(--text-muted);">Барои дидани тестҳо майдонҳои зеринро пур кунед.</p>
                
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px;">
                    <div class="field">
                        <label>Рақами Синф</label>
                        <input type="text" id="searchClass" placeholder="Масалан: 9" oninput="checkAndLoadTests()">
                    </div>
                    <div class="field">
                        <label>Чоряк</label>
                        <select id="searchQuarter" onchange="checkAndLoadTests()">
                            <option value="1">Чоряки 1</option>
                            <option value="2">Чоряки 1 + 2</option>
                            <option value="3">Чоряки 1 + 2 + 3</option>
                            <option value="4">Чоряки 1 + 2 + 3 + 4</option>
                        </select>
                    </div>
                    <div class="field">
                        <label>Номи Фан</label>
                        <input type="text" id="searchSubject" placeholder="Масалан: Математика" oninput="checkAndLoadTests()">
                    </div>
                </div>
            </div>

            <div id="activeTestSection" class="card" style="display:none;">
                <h3 style="border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:15px;" id="mainResultTitle">Санҷиши фаъол</h3>
                
                <div class="timer-control-wrapper" id="timerControlWrapper">
                    <div class="timer-box">Вақт: <span id="timeLeft">01:00</span></div>
                    <button class="start-test-btn" id="startTestBtn" onclick="beginTestExecution()">▶ Сар кардан</button>
                </div>

                <div id="mainQuestionsList"></div>
                
                <button class="scan-button" id="submitTestBtn" style="margin-top:20px; display:none;" onclick="calculateScore()">Супоридан ва гирифтани баҳо</button>
                <div id="finalScoreBox" style="margin-top:20px; font-size:16px; font-weight:bold;"></div>
            </div>
        </section>

        <section id="testListSection" class="page">
            <div class="card">
                <h2>📋 Рӯйхати тестҳои сабтшуда</h2>
                <div id="sidebarTestListContainer"></div>
            </div>
        </section>

        <section id="historySection" class="page">
            <div class="card">
                <h2>📊 Таърихи натиҷаҳои супоридашуда</h2>
                <div id="historyContainer"></div>
            </div>
        </section>

        <section id="scanner" class="page">
            <div class="card">
                <h2>➕ Илова кардани Саволи Нав</h2>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                    <div class="field"><label>Синф</label><input type="text" id="addClass" placeholder="Масалан: 9"></div>
                    <div class="field"><label>Номи Фан</label><input type="text" id="addSubject" placeholder="Масалан: Математика"></div>
                </div>
                <div class="field">
                    <label>Чоряк</label>
                    <select id="addQuarter">
                        <option value="1">Чоряки 1</option>
                        <option value="2">Чоряки 1 + 2</option>
                        <option value="3">Чоряки 1 + 2 + 3</option>
                        <option value="4">Чоряки 1 + 2 + 3 + 4</option>
                    </select>
                </div>
                <div class="field"><label>Матни савол</label><textarea id="addQuestionText" placeholder="Саволро ин ҷо нависед..."></textarea></div>
                <div class="field"><label>Варианти А</label><input type="text" id="optA" placeholder="Ҷавоби А"></div>
                <div class="field"><label>Варианти Б</label><input type="text" id="optB" placeholder="Ҷавоби Б"></div>
                <div class="field"><label>Варианти В</label><input type="text" id="optV" placeholder="Ҷавоби В"></div>
                <div class="field"><label>Варианти Г</label><input type="text" id="optG" placeholder="Ҷавоби Г"></div>
                <div class="field">
                    <label>Ҷавоби дуруст</label>
                    <select id="correctOpt">
                        <option value="0">А</option><option value="1">Б</option><option value="2">В</option><option value="3">Г</option>
                    </select>
                </div>
                <button class="scan-button" onclick="saveNewQuestion()">Илова кардан ва рамзгузорӣ</button>
            </div>
        </section>

        <section id="books" class="page">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2>📚 Китобҳои дарсӣ (PDF)</h2>
                    <button class="scan-button" style="width: auto; margin-top: 0; padding: 10px 20px;" onclick="document.getElementById('pdfUploadInput').click()">➕ Илова кардани китоб</button>
                    <input type="file" id="pdfUploadInput" style="display: none;" accept="application/pdf" onchange="handlePdfUpload(event)">
                </div>
                <div id="booksGridContainer" class="books-grid"></div>
            </div>
        </section>
    </div>
</main>

<div id="pdfModalViewer" class="pdf-modal">
    <div class="pdf-modal-header">
        <h3 id="modalBookTitle" style="margin:0; font-size:16px; color:white;">Китоб</h3>
        <div style="display:flex; gap:10px; align-items:center;">
            <a id="modalDownloadBtn" href="#" download class="book-btn read-btn" style="padding:6px 12px;">Боргирӣ</a>
            <button class="close-modal-btn" onclick="closePdfViewer()">✕ Баромадан</button>
        </div>
    </div>
    <iframe id="pdfIframe" style="width:100%; height:calc(100% - 50px); border:none;"></iframe>
</div>

<script>
let allQuestions = JSON.parse(localStorage.getItem('choryak_questions')) || [];
let testHistory = JSON.parse(localStorage.getItem('choryak_history')) || [];
let allBooks = JSON.parse(localStorage.getItem('choryak_books')) || [];
let userAnswers = {};
let timerInterval = null;
let currentTotalSeconds = 0;

function encodeToCodes(str) {
    if(!str) return "";
    let codes = [];
    for (let i = 0; i < str.length; i++) codes.push(str.charCodeAt(i));
    return codes.join(',');
}
function decodeFromCodes(codeStr) {
    if(!codeStr) return "";
    return codeStr.split(',').map(c => String.fromCharCode(parseInt(c))).join('');
}
function toggleSidebar() {
    let sidebar = document.getElementById("sidebar");
    let main = document.getElementById("mainArea");
    sidebar.classList.toggle("collapsed");
    main.classList.toggle("expanded");
}
function toggleTheme() {
    let body = document.body;
    let btn = document.getElementById("themeBtn");
    if(body.getAttribute("data-theme") === "dark") {
        body.setAttribute("data-theme", "light");
        btn.textContent = "🌙 Торикӣ";
    } else {
        body.setAttribute("data-theme", "dark");
        btn.textContent = "☀️ Рӯшноӣ";
    }
}
function openPage(pageId, btn){
    if(timerInterval) clearInterval(timerInterval);
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.querySelectorAll(".menu").forEach(m => m.classList.remove("active"));
    document.getElementById(pageId).classList.add("active");
    if(btn) btn.classList.add("active");
    if(pageId === 'home') checkAndLoadTests();
    if(pageId === 'testListSection') renderTestList();
    if(pageId === 'historySection') renderHistory();
    if(pageId === 'books') renderBooks();
}
function requestPasswordForScanner(btnElement){
    let password = prompt("Паролро ворид кунед:");
    if(password === "6113") openPage('scanner', btnElement);
    else if(password !== null) alert("Пароли нодуруст!");
}
function saveNewQuestion(){
    let cls = document.getElementById("addClass").value.trim();
    let subj = document.getElementById("addSubject").value.trim();
    let qtr = document.getElementById("addQuarter").value;
    let text = document.getElementById("addQuestionText").value.trim();
    let oA = document.getElementById("optA").value.trim();
    let oB = document.getElementById("optB").value.trim();
    let oV = document.getElementById("optV").value.trim();
    let oG = document.getElementById("optG").value.trim();
    let correct = parseInt(document.getElementById("correctOpt").value);
    if(!cls || !subj || !text || !oA || !oB || !oV || !oG){ alert("Ҳамаи майдонҳоро пур кунед!"); return; }
    allQuestions.push({ class: cls, subject: subj.toLowerCase(), subjectDisplay: subj, quarter: qtr, textEncoded: encodeToCodes(text), optsEncoded: [encodeToCodes(oA), encodeToCodes(oB), encodeToCodes(oV), encodeToCodes(oG)], correct: correct });
    localStorage.setItem('choryak_questions', JSON.stringify(allQuestions));
    alert("Савол сабт шуд!");
    openPage('home', document.querySelectorAll('.menu')[0]);
}
function deleteQuestion(index){
    if(prompt("Калимаи тасдиқро нависед (confirm):") === "confirm"){
        allQuestions.splice(index, 1);
        localStorage.setItem('choryak_questions', JSON.stringify(allQuestions));
        renderTestList();
    }
}
function renderTestList(){
    let container = document.getElementById("sidebarTestListContainer");
    if(allQuestions.length === 0){ container.innerHTML = `<p style="color:var(--text-muted);">Ҳоло ягон тест нест.</p>`; return; }
    let html = "";
    allQuestions.forEach((q, idx) => {
        html += `<div class="test-item-card"><div class="test-meta"><div><b>#${idx + 1}</b> | Фан: ${q.subjectDisplay} | Синф: ${q.class}</div><button class="delete-btn" onclick="deleteQuestion(${idx})">🗑️</button></div><div>Савол: ${decodeFromCodes(q.textEncoded)}</div></div>`;
    });
    container.innerHTML = html;
}
function handlePdfUpload(event) {
    let file = event.target.files[0];
    if(!file) return;
    let reader = new FileReader();
    reader.onload = function(e) {
        let bookName = prompt("Номи китоб:", file.name.replace(/\.[^/.]+$/, ""));
        if(!bookName) return;
        allBooks.push({ name: bookName, data: e.target.result, date: new Date().toLocaleDateString() });
        localStorage.setItem('choryak_books', JSON.stringify(allBooks));
        renderBooks();
    };
    reader.readAsDataURL(file);
}
function renderBooks() {
    let container = document.getElementById("booksGridContainer");
    if(allBooks.length === 0){ container.innerHTML = `<p style="color:var(--text-muted);">Китоб нест.</p>`; return; }
    let html = "";
    allBooks.forEach((book, idx) => {
        html += `<div class="book-card"><div><div class="book-title">${book.name}</div></div><div class="book-actions"><button class="book-btn read-btn" onclick="openPdfViewer(${idx})">Мутолиа</button><button class="delete-btn" onclick="deleteBook(${idx})">🗑️</button></div></div>`;
    });
    container.innerHTML = html;
}
function openPdfViewer(idx) {
    let book = allBooks[idx];
    document.getElementById("modalBookTitle").textContent = book.name;
    document.getElementById("pdfIframe").src = book.data;
    document.getElementById("modalDownloadBtn").href = book.data;
    document.getElementById("pdfModalViewer").style.display = "flex";
}
function closePdfViewer() { document.getElementById("pdfModalViewer").style.display = "none"; }
function deleteBook(idx) { allBooks.splice(idx, 1); localStorage.setItem('choryak_books', JSON.stringify(allBooks)); renderBooks(); }
function checkAndLoadTests(){
    if(timerInterval) clearInterval(timerInterval);
    let sClass = document.getElementById("searchClass").value.trim();
    let sQuarter = document.getElementById("searchQuarter").value;
    let sSubject = document.getElementById("searchSubject").value.trim().toLowerCase();
    let activeSec = document.getElementById("activeTestSection");
    let questionsList = document.getElementById("mainQuestionsList");
    let submitBtn = document.getElementById("submitTestBtn");
    let timerControlWrapper = document.getElementById("timerControlWrapper");
    if(!sClass || !sSubject){ activeSec.style.display = "none"; return; }
    let filtered = allQuestions.filter(q => q.class === sClass && q.quarter === sQuarter && q.subject.includes(sSubject));
    activeSec.style.display = "block";
    submitBtn.style.display = "none";
    if(filtered.length === 0){
        document.getElementById("mainResultTitle").textContent = `Санҷиш: Синфи ${sClass}`;
        timerControlWrapper.style.display = "none";
        questionsList.innerHTML = `<p style="color:var(--text-muted);">Савол ёфт нашуд.</p>`;
        return;
    }
    timerControlWrapper.style.display = "flex";
    currentTotalSeconds = filtered.length * 60;
    document.getElementById("timeLeft").textContent = "01:00";
    let htmlContent = "";
    filtered.forEach((item, index) => {
        let qNum = index + 1;
        htmlContent += `<div class="question-card"><p><b>Саволи ${qNum}:</b> ${decodeFromCodes(item.textEncoded)}</p><button class="option-btn" onclick="selectOption(${qNum}, 0, this)">А) ${decodeFromCodes(item.optsEncoded[0])}</button><button class="option-btn" onclick="selectOption(${qNum}, 1, this)">Б) ${decodeFromCodes(item.optsEncoded[1])}</button><button class="option-btn" onclick="selectOption(${qNum}, 2, this)">В) ${decodeFromCodes(item.optsEncoded[2])}</button><button class="option-btn" onclick="selectOption(${qNum}, 3, this)">Г) ${decodeFromCodes(item.optsEncoded[3])}</button></div>`;
    });
    questionsList.innerHTML = htmlContent;
    userAnswers = {};
}
function beginTestExecution() {
    document.getElementById("submitTestBtn").style.display = "block";
    startTimer(currentTotalSeconds);
}
function startTimer(duration) {
    let timer = duration, display = document.getElementById("timeLeft");
    if(timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        let m = parseInt(timer / 60, 10), s = parseInt(timer % 60, 10);
        display.textContent = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
        if (--timer < 0) { clearInterval(timerInterval); calculateScore(); }
    }, 1000);
}
function selectOption(qNum, optIndex, btnElement){
    btnElement.parentElement.querySelectorAll(".option-btn").forEach(b => b.classList.remove("selected-opt"));
    btnElement.classList.add("selected-opt");
    userAnswers[qNum] = optIndex;
}
function calculateScore(){
    if(timerInterval) clearInterval(timerInterval);
    let sClass = document.getElementById("searchClass").value.trim();
    let sQuarter = document.getElementById("searchQuarter").value;
    let sSubject = document.getElementById("searchSubject").value.trim().toLowerCase();
    let filtered = allQuestions.filter(q => q.class === sClass && q.quarter === sQuarter && q.subject.includes(sSubject));
    if(filtered.length === 0) return;
    let correctCount = 0;
    filtered.forEach((item, index) => { if(userAnswers[index + 1] === item.correct) correctCount++; });
    let finalGrade = Math.max(2, Math.round((correctCount / filtered.length) * 5));
    document.getElementById("finalScoreBox").innerHTML = `Натиҷа: ${correctCount}/${filtered.length}. Баҳо: <span style="color:var(--green);">${finalGrade}</span>`;
    document.getElementById("submitTestBtn").style.display = "none";
}
function renderHistory(){}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)