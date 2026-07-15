// Git Magager - Background Service Worker

importScripts('ExtPay.js');

const SERVER_URL = 'http://127.0.0.1:9456';

// Initialize ExtPay - replace 'git-magager' with your ExtensionPay extension ID
// Register at https://extensionpay.com to get your own ID
var extpay = ExtPay('hckpgnffhjfblnaehcnchfhaihebmkfo');
extpay.startBackground();

// React when a user pays or logs in with a paid account
extpay.onPaid.addListener(user => {
  console.log('[Git Magager] User paid:', user);
  // You can add custom logic here, e.g. unlock premium features
});

// Check server health on install
chrome.runtime.onInstalled.addListener(() => {
  console.log('[Git Magager] Extension installed');
  checkServerHealth();
});

async function checkServerHealth() {
  try {
    const response = await fetch(`${SERVER_URL}/health`);
    const data = await response.json();
    console.log('[Git Magager] Server connected:', data);
    return true;
  } catch (e) {
    console.warn('[Git Magager] Server not running');
    return false;
  }
}

// Listen for messages from popup and content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'CHECK_SERVER') {
    checkServerHealth().then(sendResponse);
    return true;
  }

  if (message.type === 'CHOOSE_FOLDER') {
    fetch(`${SERVER_URL}/choose-folder`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ defaultPath: message.defaultPath })
    })
      .then(res => res.json())
      .then(sendResponse)
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (message.type === 'CLONE') {
    fetch(`${SERVER_URL}/clone`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: message.url, openTerminal: message.openTerminal, directory: message.directory })
    })
      .then(res => res.json())
      .then(sendResponse)
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (message.type === 'GET_CONFIG') {
    fetch(`${SERVER_URL}/config`)
      .then(res => res.json())
      .then(sendResponse)
      .catch(err => sendResponse({ error: err.message }));
    return true;
  }

  if (message.type === 'SET_CONFIG') {
    fetch(`${SERVER_URL}/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message.config)
    })
      .then(res => res.json())
      .then(sendResponse)
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }

  // ─── ExtPay payment handlers ──────────────────────────────────
  if (message.type === 'GET_USER') {
    var extpay = ExtPay('hckpgnffhjfblnaehcnchfhaihebmkfo');
    extpay.getUser()
      .then(sendResponse)
      .catch(err => sendResponse({ error: err.message }));
    return true;
  }

  if (message.type === 'OPEN_PAYMENT_PAGE') {
    var extpay = ExtPay('hckpgnffhjfblnaehcnchfhaihebmkfo');
    extpay.openPaymentPage()
      .then(() => sendResponse({ success: true }))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (message.type === 'OPEN_LOGIN_PAGE') {
    var extpay = ExtPay('hckpgnffhjfblnaehcnchfhaihebmkfo');
    extpay.openLoginPage()
      .then(() => sendResponse({ success: true }))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }
});
