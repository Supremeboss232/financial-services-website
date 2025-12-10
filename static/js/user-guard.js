(function(){
  // Prevent navigation outside /user for in-app links
  document.addEventListener('click', function(e){
    var el = e.target;
    while(el && el.nodeName !== 'A') el = el.parentElement;
    if(!el) return;
    var href = el.getAttribute('href');
    if(!href) return;
    // allow anchors, javascript:, mailto:, tel:
    if(href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
    // absolute URL handling
    try{
      var url = new URL(href, window.location.origin);
    } catch(err){
      return; // malformed or relative we ignore
    }
    var path = url.pathname || '';
    // allowed prefixes for static/API/auth/admin
    var allowed = ['/user','/api','/js','/css','/lib','/img','/auth','/logout','/static','/admin'];
    var ok = allowed.some(function(p){ return path.startsWith(p); });
    if(!ok && (url.origin === window.location.origin || href.startsWith('/'))){
      e.preventDefault();
      // optional feedback
      if(window.confirm('This link would navigate outside the user area. Proceed to user dashboard instead?')){
        window.location.href = '/user/dashboard';
      }
    }
  }, true);
})();
