(function(){
  // Prevent navigation outside /admin for in-admin links
  document.addEventListener('click', function(e){
    var el = e.target;
    while(el && el.nodeName !== 'A') el = el.parentElement;
    if(!el) return;
    var href = el.getAttribute('href');
    if(!href) return;
    if(href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
    try{
      var url = new URL(href, window.location.origin);
    } catch(err){
      return;
    }
    var path = url.pathname || '';
    var allowed = ['/admin','/api','/js','/css','/lib','/img','/auth','/logout','/static','/user'];
    var ok = allowed.some(function(p){ return path.startsWith(p); });
    if(!ok && (url.origin === window.location.origin || href.startsWith('/'))){
      e.preventDefault();
      if(window.confirm('This link would navigate outside the admin area. Stay in admin dashboard?')){
        window.location.href = '/admin';
      }
    }
  }, true);
})();
