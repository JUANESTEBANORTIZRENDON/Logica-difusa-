// Capturas reales de la app local mediante el protocolo de depuración de Chrome.
import {spawn} from 'node:child_process';
import {writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
const chrome = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', [
  '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  '--remote-debugging-port=9229', `--user-data-dir=${resolve('evidencias/chrome-cdp-profile')}`,
  'http://127.0.0.1:8518',
], {stdio:'ignore', windowsHide:true});
const delay = ms => new Promise(r=>setTimeout(r,ms));
let ws;
try {
  let pages;
  for(let i=0;i<40;i++) {
    try { pages=await (await fetch('http://127.0.0.1:9229/json')).json(); if(pages.some(p=>p.type==='page')) break; } catch {}
    await delay(500);
  }
  ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);
  await new Promise(r=>ws.addEventListener('open',r,{once:true}));
  let id=0; const pending=new Map();
  ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(pending.has(m.id)){const [ok,fail]=pending.get(m.id);pending.delete(m.id);m.error?fail(m.error):ok(m.result);}});
  const send=(method,params={})=>new Promise((ok,fail)=>{pending.set(++id,[ok,fail]);ws.send(JSON.stringify({id,method,params}));});
  const evaluate=async expression=>(await send('Runtime.evaluate',{expression,returnByValue:true})).result.value;
  await send('Page.enable');
  await send('Page.navigate',{url:'http://127.0.0.1:8518'});
  await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
  let ready=false;
  for(let i=0;i<60;i++) {if(await evaluate("document.body.innerText.includes('Calcular índice')")){ready=true;break;}await delay(500);}
  if(!ready) throw new Error('La interfaz no terminó de cargar');
  await delay(1000);
  console.log(await evaluate(`JSON.stringify({scope:CSS.supports('selector(:scope)'),styleSheets:[...document.styleSheets].map(s=>{try{return [...s.cssRules].slice(0,2).map(r=>r.cssText.slice(0,120))}catch{return []}}).filter(r=>r.some(v=>v.includes('scope'))),svg:document.querySelector('.pulse-disc')?.innerHTML,button:document.querySelector('[data-testid="stFormSubmitButton"]')?.innerHTML.slice(0,700),display:getComputedStyle(document.querySelector('.academic-note')).display})`));
  for(const [name,width,height] of [['escritorio',1440,1100],['movil',390,1000]]) {
    await send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
    await delay(1200);
    const capture=await send('Page.captureScreenshot',{format:'png'});
    writeFileSync(`evidencias/interfaz-${name}.png`,Buffer.from(capture.data,'base64'));
    console.log(name, await evaluate('JSON.stringify({viewport:innerWidth,ancho:document.documentElement.scrollWidth,bootstrap:!!document.querySelector(".clinic-ui .row")})'));
  }
  await send('Browser.close');
} finally { if(ws) ws.close(); chrome.kill(); }
