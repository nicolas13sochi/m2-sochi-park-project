
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

    document.addEventListener('touchmove', function(e) {
      if (e.touches.length >= 2) {
        // Два пальца — разрешаем
        return;
      }
      // Одиночный тач остаётся под контролем UIkit (например, прокрутка)
    }, { passive: false });


    


