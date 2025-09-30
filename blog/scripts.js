// Blog Post Interactive Features - Clean & Optimized

(function() {
  'use strict';
  
  // ===== DOM ELEMENTS =====
  const body = document.body;
  const progress = document.getElementById('progress');
  const tocList = document.getElementById('tocList');
  const cursorGlow = document.getElementById('cursorGlow');
  const tocToggle = document.getElementById('tocToggle');
  const toc = document.querySelector('.toc');
  
  // ===== PROGRESS BAR =====
  function updateProgress() {
    if (!progress) return;
    const h = document.documentElement;
    const scrolled = h.scrollTop / (h.scrollHeight - h.clientHeight);
    progress.style.width = (scrolled * 100) + '%';
  }
  
  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
  
  // ===== TOC TOGGLE (MOBILE) =====
  if (tocToggle && toc) {
    tocToggle.addEventListener('click', () => {
      toc.classList.toggle('visible');
      const icon = tocToggle.querySelector('i, svg');
      const isVisible = toc.classList.contains('visible');
      
      if (icon) {
        if (icon.tagName === 'I') {
          icon.className = isVisible ? 'fas fa-times' : 'fas fa-list';
        }
      }
      
      tocToggle.setAttribute('aria-expanded', isVisible);
    });
  }
  
  // ===== TOC GENERATION =====
  function buildTOC() {
    if (!tocList) return;
    
    const headings = document.querySelectorAll('#postContent h2, #postContent h3');
    tocList.innerHTML = '';
    const items = [];
    
    headings.forEach((h, i) => {
      const id = h.id || `h-${i}`;
      h.id = id;
      
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `#${id}`;
      a.textContent = h.textContent;
      
      if (h.tagName === 'H3') {
        a.style.paddingLeft = '12px';
      }
      
      li.appendChild(a);
      tocList.appendChild(li);
      items.push({ id, el: h, a });
    });
    
    // Active section observer
    if (items.length > 0) {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const item = items.find(x => x.el === entry.target);
          if (!item) return;
          
          if (entry.isIntersecting) {
            items.forEach(i => i.a.classList.remove('active'));
            item.a.classList.add('active');
          }
        });
      }, { rootMargin: '0px 0px -70% 0px', threshold: 0.1 });
      
      items.forEach(item => obs.observe(item.el));
    }
  }
  
  buildTOC();
  
  // ===== KEYBOARD SHORTCUTS =====
  document.addEventListener('keydown', (e) => {
    switch(e.key.toLowerCase()) {
      case 'h':
        if (e.ctrlKey || e.metaKey) {
          e.preventDefault();
          window.location.href = '/';
        }
        break;
      case 'home':
        if (e.ctrlKey || e.metaKey) {
          e.preventDefault();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        break;
      case 'end':
        if (e.ctrlKey || e.metaKey) {
          e.preventDefault();
          window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
        break;
      case 't':
        if ((e.ctrlKey || e.metaKey) && tocToggle) {
          e.preventDefault();
          tocToggle.click();
        }
        break;
    }
  });
  
  // ===== SOCIAL SHARING =====
  window.shareOnTwitter = function() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(document.title);
    window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
  };
  
  window.shareOnLinkedIn = function() {
    const url = encodeURIComponent(window.location.href);
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
  };
  
  window.copyLink = function() {
    navigator.clipboard.writeText(window.location.href).then(() => {
      showToast('Link copied to clipboard!');
    }).catch(() => {
      showToast('Failed to copy link');
    });
  };
  
  // ===== SCROLL TO TOP =====
  window.scrollToTop = function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  // ===== TOAST NOTIFICATIONS =====
  function showToast(message) {
    let toast = document.querySelector('.toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
  }
  
  // ===== CURSOR GLOW EFFECT =====
  if (cursorGlow) {
    window.addEventListener('mousemove', (e) => {
      cursorGlow.style.setProperty('--mx', e.clientX + 'px');
      cursorGlow.style.setProperty('--my', e.clientY + 'px');
    }, { passive: true });
  }
  
  // ===== READING TIME CALCULATION =====
  function updateReadingTime() {
    const readingElement = document.getElementById('postReading');
    if (!readingElement) return;
    
    const wordsPerMinute = 200;
    const contentElements = document.querySelectorAll('#postContent p, #postContent li');
    let wordCount = 0;
    
    contentElements.forEach(element => {
      wordCount += element.textContent.trim().split(/\s+/).length;
    });
    
    const readingTime = Math.ceil(wordCount / wordsPerMinute);
    readingElement.textContent = `${readingTime} min read`;
  }
  
  updateReadingTime();
  
  // ===== SMOOTH LOADING ANIMATION =====
  document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('loaded');
  });
  
})();
