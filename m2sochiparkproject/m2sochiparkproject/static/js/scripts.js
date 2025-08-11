
  $(document).ready(function(){
      // Cookie consent functions
      function setCookie(name, value, days) {
        console.log('setCookie');
          var expires = "";
          if (days) {
              var date = new Date();
              date.setTime(date.getTime() + (days*24*60*60*1000));
              expires = "; expires=" + date.toUTCString();
          }
          document.cookie = name + "=" + (value || "") + expires + "; path=/";
          $('#cookieModal').css('display', 'none');
      }
  
      function getCookie(name) {
          var nameEQ = name + "=";
          var ca = document.cookie.split(';');
          for(var i=0;i < ca.length;i++) {
              var c = ca[i];
              while (c.charAt(0)==' ') c = c.substring(1,c.length);
              if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
          }
          return null;
      }
  
      // Show cookie consent modal if not accepted yet
      if(getCookie('cookiesAccepted') === null){
          $('#cookieModal').css('display', 'flex');
      }
  
      // Handle cookie consent choices
      $('#acceptCookies').on('click', function(){
          setCookie('cookiesAccepted', 'true', 365);
          console.log('acceptCookies');
      });
  
      $('#rejectCookies').on('click', function(){
          setCookie('cookiesAccepted', 'false', 365);
          console.log('rejectCookies');
      });

      // input mask
      $(".phone-mask").mask("+7 (999) 999-99-99");
    //   $(".phone-mask").on('focus', function () {
    //     const input = this;
    //     // Установить курсор в начало
    //     setTimeout(function () {
    //         if (input.setSelectionRange) {
    //         input.setSelectionRange(0, 0);
    //         }
    //     }, 0);
    //     });


    


    });

    document.addEventListener('DOMContentLoaded', function () {
      const modal = document.getElementById('getAparmentPlan');

      UIkit.util.on('[uk-toggle]', 'click', function (e) {
        const trigger = e.currentTarget;

        const blockId = trigger.dataset.blockId;
        const formName = trigger.dataset.formName;

        if (modal) {
          const inputBlockId = modal.querySelector('input[name="block_id"]');
          const inputFormName = modal.querySelector('input[name="form_name"]');
          const modalTextEl = modal.querySelector('.uk-modal-title-data');

          if (inputBlockId) inputBlockId.value = blockId || '';
          if (inputFormName) inputFormName.value = formName || '';
          if (modalTextEl) modalTextEl.textContent = formName || '';
        }
      });
    });


    document.addEventListener("DOMContentLoaded", function () {
  const lightbox = document.querySelector('[uk-lightbox]');
  if (!lightbox) return;

  lightbox.addEventListener('click', function (e) {
    const img = e.target.closest('img');
    if (!img) return;

    const overlay = document.createElement('div');
    Object.assign(overlay.style, {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      background: 'rgba(0,0,0,0.9)',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 9999,
      userSelect: 'none',
    });

    const viewArea = document.createElement('div');
    Object.assign(viewArea.style, {
      flex: '1 1 auto',
      position: 'relative',
      overflow: 'hidden',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '100%',
      height: '100%',
    });

    const zoomedImg = document.createElement('img');
    zoomedImg.src = img.src;
    zoomedImg.style.position = 'relative';
    zoomedImg.style.transformOrigin = 'center center';
    zoomedImg.style.cursor = 'grab';
    zoomedImg.style.userSelect = 'none';

    viewArea.appendChild(zoomedImg);
    overlay.appendChild(viewArea);

    const controls = document.createElement('div');
    Object.assign(controls.style, {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '10px',
      padding: '0 0 0 0',
      height: '50px',
      width: '100%',
      background: 'rgba(0,0,0,0.8)',
      flex: '0 0 auto',
      userSelect: 'none',
    });

    const btnZoomOut = document.createElement('button');
    btnZoomOut.textContent = '–';
    const btnZoomIn = document.createElement('button');
    btnZoomIn.textContent = '+';
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';

    [btnZoomOut, btnZoomIn, closeBtn].forEach(btn => {
      Object.assign(btn.style, {
        fontSize: '28px',
        padding: '5px 15px',
        cursor: 'pointer',
        color: '#fff',
        background: 'transparent',
        border: '2px solid #fff',
        borderRadius: '4px',
        transition: 'background-color 0.3s ease',
      });
      btn.addEventListener('mouseenter', () => btn.style.backgroundColor = 'rgba(255,255,255,0.2)');
      btn.addEventListener('mouseleave', () => btn.style.backgroundColor = 'transparent');
    });

    controls.appendChild(btnZoomOut);
    controls.appendChild(btnZoomIn);
    controls.appendChild(closeBtn);
    overlay.appendChild(controls);

    document.body.appendChild(overlay);

    let scale = 1;
    let translateX = 0;
    let translateY = 0;
    let isDragging = false;
    let startX, startY;

    function clampTranslate() {
      const viewRect = viewArea.getBoundingClientRect();
      const imgRect = zoomedImg.getBoundingClientRect();

      const maxTranslateX = (imgRect.width - viewRect.width) / 2;
      const maxTranslateY = (imgRect.height - viewRect.height) / 2;

      if (imgRect.width <= viewRect.width) translateX = 0;
      else translateX = Math.min(Math.max(translateX, -maxTranslateX), maxTranslateX);

      if (imgRect.height <= viewRect.height) translateY = 0;
      else translateY = Math.min(Math.max(translateY, -maxTranslateY), maxTranslateY);
    }

    function updateTransform() {
      clampTranslate();
      zoomedImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    }

    btnZoomIn.onclick = () => {
      scale = Math.min(scale + 0.1, 5);
      updateTransform();
    };

    btnZoomOut.onclick = () => {
      scale = Math.max(scale - 0.1, 1);
      if (scale === 1) {
        translateX = 0;
        translateY = 0;
      }
      updateTransform();
    };

    zoomedImg.addEventListener('mousedown', (ev) => {
      if (scale <= 1) return;
      isDragging = true;
      startX = ev.clientX - translateX;
      startY = ev.clientY - translateY;
      zoomedImg.style.cursor = 'grabbing';
      ev.preventDefault();
    });

    window.addEventListener('mouseup', () => {
      if (!isDragging) return;
      isDragging = false;
      zoomedImg.style.cursor = 'grab';
    });

    window.addEventListener('mousemove', (ev) => {
      if (!isDragging) return;
      translateX = ev.clientX - startX;
      translateY = ev.clientY - startY;
      updateTransform();
    });

    closeBtn.addEventListener('click', () => {
      overlay.remove();
    });

    function escHandler(ev) {
      if (ev.key === 'Escape') {
        overlay.remove();
        document.removeEventListener('keydown', escHandler);
      }
    }
    document.addEventListener('keydown', escHandler);
  });
});

