!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports.volume=t():(e.xgplayer=e.xgplayer||{},e.xgplayer.PlayerControls=e.xgplayer.PlayerControls||{},e.xgplayer.PlayerControls.volume=t())}(window,(function(){return function(e){var t={};function n(r){if(t[r])return t[r].exports;var o=t[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(r,o,function(t){return e[t]}.bind(null,o));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=1)}([function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.util=t.PresentationMode=void 0,t.createDom=i,t.hasClass=l,t.addClass=u,t.removeClass=s,t.toggleClass=c,t.findDom=f,t.padStart=d,t.format=p,t.event=v,t.typeOf=g,t.deepCopy=m,t.getBgImage=y,t.copyDom=h,t._setInterval=x,t._clearInterval=b,t.createImgBtn=w,t.isWeiXin=k,t.isUc=C,t.computeWatchDur=L,t.offInDestroy=M,t.on=E,t.once=O,t.getBuffered2=j,t.checkIsBrowser=S,t.setStyle=I,t.checkWebkitSetPresentationMode=function(e){return"function"==typeof e.webkitSetPresentationMode};var r,o=n(3),a=(r=o)&&r.__esModule?r:{default:r};function i(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"div",t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"",n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"",o=document.createElement(e);return o.className=r,o.innerHTML=t,Object.keys(n).forEach((function(t){var r=t,a=n[t];"video"===e||"audio"===e?a&&o.setAttribute(r,a):o.setAttribute(r,a)})),o}function l(e,t){return!!e&&(e.classList?Array.prototype.some.call(e.classList,(function(e){return e===t})):!!e.className&&!!e.className.match(new RegExp("(\\s|^)"+t+"(\\s|$)")))}function u(e,t){e&&(e.classList?t.replace(/(^\s+|\s+$)/g,"").split(/\s+/g).forEach((function(t){t&&e.classList.add(t)})):l(e,t)||(e.className+=" "+t))}function s(e,t){e&&(e.classList?t.split(/\s+/g).forEach((function(t){e.classList.remove(t)})):l(e,t)&&t.split(/\s+/g).forEach((function(t){var n=new RegExp("(\\s|^)"+t+"(\\s|$)");e.className=e.className.replace(n," ")})))}function c(e,t){e&&t.split(/\s+/g).forEach((function(t){l(e,t)?s(e,t):u(e,t)}))}function f(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:document,t=arguments[1],n=void 0;try{n=e.querySelector(t)}catch(r){0===t.indexOf("#")&&(n=e.getElementById(t.slice(1)))}return n}function d(e,t,n){for(var r=String(n),o=t>>0,a=Math.ceil(o/r.length),i=[],l=String(e);a--;)i.push(r);return i.join("").substring(0,o-l.length)+l}function p(e){if(window.isNaN(e))return"";var t=d(Math.floor(e/3600),2,0),n=d(Math.floor((e-3600*t)/60),2,0),r=d(Math.floor(e-3600*t-60*n),2,0);return("00"===t?[n,r]:[t,n,r]).join(":")}function v(e){if(e.touches){var t=e.touches[0]||e.changedTouches[0];e.clientX=t.clientX||0,e.clientY=t.clientY||0,e.offsetX=t.pageX-t.target.offsetLeft,e.offsetY=t.pageY-t.target.offsetTop}e._target=e.target||e.srcElement}function g(e){return Object.prototype.toString.call(e).match(/([^\s.*]+)(?=]$)/g)[0]}function m(e,t){if("Object"===g(t)&&"Object"===g(e))return Object.keys(t).forEach((function(n){"Object"!==g(t[n])||t[n]instanceof Node?"Array"===g(t[n])?e[n]="Array"===g(e[n])?e[n].concat(t[n]):t[n]:e[n]=t[n]:e[n]?m(e[n],t[n]):e[n]=t[n]})),e}function y(e){var t=(e.currentStyle||window.getComputedStyle(e,null)).backgroundImage;if(!t||"none"===t)return"";var n=document.createElement("a");return n.href=t.replace(/url\("|"\)/g,""),n.href}function h(e){if(e&&1===e.nodeType){var t=document.createElement(e.tagName);return Array.prototype.forEach.call(e.attributes,(function(e){t.setAttribute(e.name,e.value)})),e.innerHTML&&(t.innerHTML=e.innerHTML),t}return""}function x(e,t,n,r){e._interval[t]||(e._interval[t]=setInterval(n.bind(e),r))}function b(e,t){clearInterval(e._interval[t]),e._interval[t]=null}function w(e,t,n,r){var o=i("xg-"+e,"",{},"xgplayer-"+e+"-img");if(o.style.backgroundImage='url("'+t+'")',n&&r){var a=void 0,l=void 0,u=void 0;["px","rem","em","pt","dp","vw","vh","vm","%"].every((function(e){return!(n.indexOf(e)>-1&&r.indexOf(e)>-1)||(a=Number(n.slice(0,n.indexOf(e)).trim()),l=Number(r.slice(0,r.indexOf(e)).trim()),u=e,!1)})),o.style.width=""+a+u,o.style.height=""+l+u,o.style.backgroundSize=""+a+u+" "+l+u,o.style.margin="start"===e?"-"+l/2+u+" auto auto -"+a/2+u:"auto 5px auto 5px"}return o}function k(){return window.navigator.userAgent.toLowerCase().indexOf("micromessenger")>-1}function C(){return window.navigator.userAgent.toLowerCase().indexOf("ucbrowser")>-1}function L(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],t=[],n=0;n<e.length;n++)if(!(!e[n].end||e[n].begin<0||e[n].end<0||e[n].end<e[n].begin))if(t.length<1)t.push({begin:e[n].begin,end:e[n].end});else for(var r=0;r<t.length;r++){var o=e[n].begin,a=e[n].end;if(a<t[r].begin){t.splice(r,0,{begin:o,end:a});break}if(!(o>t[r].end)){var i=t[r].begin,l=t[r].end;t[r].begin=Math.min(o,i),t[r].end=Math.max(a,l);break}if(r>t.length-2){t.push({begin:o,end:a});break}}for(var u=0,s=0;s<t.length;s++)u+=t[s].end-t[s].begin;return u}function M(e,t,n,r){e.once(r,(function o(){e.off(t,n),e.off(r,o)}))}function E(e,t,n,r){if(r)e.on(t,n),M(e,t,n,r);else{e.on(t,(function r(o){n(o),e.off(t,r)}))}}function O(e,t,n,r){if(r)e.once(t,n),M(e,t,n,r);else{e.once(t,(function r(o){n(o),e.off(t,r)}))}}function j(e){for(var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:.5,n=[],r=0;r<e.length;r++)n.push({start:e.start(r)<.5?0:e.start(r),end:e.end(r)});n.sort((function(e,t){var n=e.start-t.start;return n||t.end-e.end}));var o=[];if(t)for(var i=0;i<n.length;i++){var l=o.length;if(l){var u=o[l-1].end;n[i].start-u<t?n[i].end>u&&(o[l-1].end=n[i].end):o.push(n[i])}else o.push(n[i])}else o=n;return new a.default(o)}function S(){return!("undefined"==typeof window||void 0===window.document||void 0===window.document.createElement)}function I(e,t,n){var r=e.style;try{r[t]=n}catch(e){r.setProperty(t,n)}}t.PresentationMode={PIP:"picture-in-picture",INLINE:"inline",FULLSCREEN:"fullscreen"};t.util={createDom:i,hasClass:l,addClass:u,removeClass:s,toggleClass:c,findDom:f,padStart:d,format:p,event:v,typeOf:g,deepCopy:m,getBgImage:y,copyDom:h,setInterval:x,clearInterval:b,createImgBtn:w,isWeiXin:k,isUc:C,computeWatchDur:L,offInDestroy:M,on:E,once:O,getBuffered2:j,checkIsBrowser:S,setStyle:I}},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=a(n(2)),o=a(n(5));function a(e){return e&&e.__esModule?e:{default:e}}t.default={name:"volume",method:function(){r.default.method.call(this),o.default.method.call(this)}},e.exports=t.default},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r,o=n(0),a=n(4),i=(r=a)&&r.__esModule?r:{default:r};t.default={name:"volume",method:function(){var e=this,t=e.root,n=void 0,r=void 0,a=void 0,l=void 0;function u(){e.controls&&(e.volume=e.config.volume,(n=e.controls.querySelector(".xgplayer-volume"))&&(r=n.querySelector(".xgplayer-slider"),a=n.querySelector(".xgplayer-bar"),l=n.querySelector(".xgplayer-drag"),"mobile"===i.default.device&&(0===e.volume&&(e.video.muted=!0),v())))}function s(t){if(r){e.video.muted=!1,r.focus(),(0,o.event)(t);var n=a.getBoundingClientRect(),i=(t.clientX,t.clientY),u=l.getBoundingClientRect().height,s=!1,c=function(t){t.preventDefault(),t.stopPropagation(),(0,o.event)(t),s=!0;var r=u-t.clientY+i,a=r/n.height;l.style.height=r+"px",e.volume=Math.max(Math.min(a,1),0)},f=function t(a){if(a.preventDefault(),a.stopPropagation(),(0,o.event)(a),window.removeEventListener("mousemove",c),window.removeEventListener("touchmove",c),window.removeEventListener("mouseup",t),window.removeEventListener("touchend",t),!s){var i=n.height-(a.clientY-n.top),u=i/n.height;l.style.height=i+"px",u<=0&&(e.volume>0?l.volume=e.video.volume:u=l.volume),e.volume=Math.max(Math.min(u,1),0)}r.volume=e.volume,s=!1};return window.addEventListener("mousemove",c),window.addEventListener("touchmove",c),window.addEventListener("mouseup",f),window.addEventListener("touchend",f),!1}}function c(){if("mobile"===i.default.device)e.video.muted?(e.video.muted=!1,e.emit("unmute"),e.volume=1):(e.video.muted=!0,e.emit("mute"),e.volume=0);else{if(!r)return;e.video.muted=!1,e.volume<.1?(r.volume<.1?e.volume=.6:e.volume=r.volume,e.emit("unmute")):(e.volume=0,e.emit("mute"))}}function f(){(0,o.addClass)(t,"xgplayer-volume-active"),n&&n.focus()}function d(){(0,o.removeClass)(t,"xgplayer-volume-active")}e.once("canplay",u),e.on("volumeBarClick",s),e.on("volumeIconClick",c),e.on("volumeIconEnter",f),e.on("volumeIconLeave",d);var p=null;function v(){p&&clearTimeout(p),p=setTimeout((function(){if("mobile"===i.default.device)(0,o.removeClass)(t,"xgplayer-volume-muted"),(0,o.removeClass)(t,"xgplayer-volume-large"),e.video.muted||e.video.defaultMuted?(e.video.muted||(e.video.muted=!0),e.video.defaultMuted=!1,(0,o.addClass)(t,"xgplayer-volume-muted")):(0,o.addClass)(t,"xgplayer-volume-large");else{if((0,o.removeClass)(t,"xgplayer-volume-muted"),(0,o.removeClass)(t,"xgplayer-volume-small"),(0,o.removeClass)(t,"xgplayer-volume-large"),0===e.volume||e.muted?(0,o.addClass)(t,"xgplayer-volume-muted"):e.volume<.5?(0,o.addClass)(t,"xgplayer-volume-small"):(0,o.addClass)(t,"xgplayer-volume-large"),!a)return;var n=a.getBoundingClientRect().height||76;l.style.height=e.volume*n+"px"}}),50)}e.on("volumechange",v),e.once("destroy",(function t(){e.off("canplay",u),e.off("volumeBarClick",s),e.off("volumeIconClick",c),e.off("volumeIconEnter",f),e.off("volumeIconLeave",d),e.off("volumechange",v),e.off("destroy",t),p&&(clearTimeout(p),p=null)}))}},e.exports=t.default},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}();var o=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.bufferedList=t}return r(e,[{key:"start",value:function(e){return this.bufferedList[e].start}},{key:"end",value:function(e){return this.bufferedList[e].end}},{key:"length",get:function(){return this.bufferedList.length}}]),e}();t.default=o,e.exports=t.default},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r={};Object.defineProperty(r,"device",{get:function(){return r.os.isPc?"pc":"mobile"}}),Object.defineProperty(r,"browser",{get:function(){var e=navigator.userAgent.toLowerCase(),t={ie:/rv:([\d.]+)\) like gecko/,firfox:/firefox\/([\d.]+)/,chrome:/chrome\/([\d.]+)/,opera:/opera.([\d.]+)/,safari:/version\/([\d.]+).*safari/};return[].concat(Object.keys(t).filter((function(n){return t[n].test(e)})))[0]||""}}),Object.defineProperty(r,"os",{get:function(){var e=navigator.userAgent,t=/(?:Windows Phone)/.test(e),n=/(?:SymbianOS)/.test(e)||t,r=/(?:Android)/.test(e),o=/(?:Firefox)/.test(e),a=/(?:iPad|PlayBook)/.test(e)||r&&!/(?:Mobile)/.test(e)||o&&/(?:Tablet)/.test(e),i=/(?:iPhone)/.test(e)&&!a;return{isTablet:a,isPhone:i,isAndroid:r,isPc:!(i||r||n||a),isSymbian:n,isWindowsPhone:t,isFireFox:o}}}),t.default=r,e.exports=t.default},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=n(0),o=l(n(6)),a=l(n(7)),i=l(n(8));function l(e){return e&&e.__esModule?e:{default:e}}n(9);t.default={name:"s_volume",method:function(){var e=this,t=(0,r.createDom)("xg-volume",'<xg-icon class="xgplayer-icon">\n                                         <div class="xgplayer-icon-large">'+i.default+'</div>\n                                         <div class="xgplayer-icon-small">'+a.default+'</div>\n                                         <div class="xgplayer-icon-muted">'+o.default+'</div>\n                                       </xg-icon>\n                                       <xg-slider class="xgplayer-slider" tabindex="2">\n                                         <xg-bar class="xgplayer-bar">\n                                           <xg-drag class="xgplayer-drag"></xg-drag>\n                                         </xg-bar>\n                                       </xg-slider>',{},"xgplayer-volume");e.once("ready",(function(){e.controls&&e.controls.appendChild(t)}));var n=t.querySelector(".xgplayer-slider"),l=t.querySelector(".xgplayer-bar"),u=t.querySelector(".xgplayer-drag"),s=t.querySelector(".xgplayer-icon");u.style.height=100*e.config.volume+"%",n.volume=e.config.volume,l.addEventListener("mousedown",(function(t){t.preventDefault(),t.stopPropagation(),e.userGestureTrigEvent("volumeBarClick",t)})),["click","touchend"].forEach((function(t){s.addEventListener(t,(function(t){t.preventDefault(),t.stopPropagation(),e.userGestureTrigEvent("volumeIconClick")}))})),s.addEventListener("mouseenter",(function(t){t.preventDefault(),t.stopPropagation(),e.userGestureTrigEvent("volumeIconEnter")})),["blur","mouseleave"].forEach((function(n){t.addEventListener(n,(function(t){t.preventDefault(),t.stopPropagation(),e.userGestureTrigEvent("volumeIconLeave")}))}))}},e.exports=t.default},function(e,t,n){"use strict";n.r(t),t.default='<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">\n  <path transform="scale(0.0220625 0.0220625)" d="M358.4 358.4h-204.8v307.2h204.8l256 256v-819.2l-256 256z"></path>\n  <path transform="scale(0.0220625 0.0220625)" d="M920.4 439.808l-108.544-109.056-72.704 72.704 109.568 108.544-109.056 108.544 72.704 72.704 108.032-109.568 108.544 109.056 72.704-72.704-109.568-108.032 109.056-108.544-72.704-72.704-108.032 109.568z"></path>\n</svg>\n'},function(e,t,n){"use strict";n.r(t),t.default='<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">\n  <path transform="scale(0.0220625 0.0220625)" d="M358.4 358.4h-204.8v307.2h204.8l256 256v-819.2l-256 256z"></path>\n  <path transform="scale(0.0220625 0.0220625)" d="M795.648 693.248l-72.704-72.704c27.756-27.789 44.921-66.162 44.921-108.544s-17.165-80.755-44.922-108.546l0.002 0.002 72.704-72.704c46.713 46.235 75.639 110.363 75.639 181.248s-28.926 135.013-75.617 181.227l-0.021 0.021zM795.648 693.248l-72.704-72.704c27.756-27.789 44.921-66.162 44.921-108.544s-17.165-80.755-44.922-108.546l0.002 0.002 72.704-72.704c46.713 46.235 75.639 110.363 75.639 181.248s-28.926 135.013-75.617 181.227l-0.021 0.021z"></path>\n</svg>\n'},function(e,t,n){"use strict";n.r(t),t.default='<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">\n  <path transform="scale(0.0220625 0.0220625)" d="M358.4 358.4h-204.8v307.2h204.8l256 256v-819.2l-256 256z"></path>\n  <path transform="scale(0.0220625 0.0220625)" d="M940.632 837.632l-72.192-72.192c65.114-64.745 105.412-154.386 105.412-253.44s-40.299-188.695-105.396-253.424l-0.016-0.016 72.192-72.192c83.639 83.197 135.401 198.37 135.401 325.632s-51.762 242.434-135.381 325.612l-0.020 0.020zM795.648 693.248l-72.704-72.704c27.756-27.789 44.921-66.162 44.921-108.544s-17.165-80.755-44.922-108.546l0.002 0.002 72.704-72.704c46.713 46.235 75.639 110.363 75.639 181.248s-28.926 135.013-75.617 181.227l-0.021 0.021z"></path>\n</svg>\n'},function(e,t,n){var r=n(10);"string"==typeof r&&(r=[[e.i,r,""]]);var o={hmr:!0,transform:void 0,insertInto:void 0};n(12)(r,o);r.locals&&(e.exports=r.locals)},function(e,t,n){(e.exports=n(11)(!1)).push([e.i,'.xgplayer-skin-default .xgplayer-volume{outline:none;-webkit-order:4;-moz-box-ordinal-group:5;order:4;width:40px;height:40px;display:block;position:relative;z-index:18}.xgplayer-skin-default .xgplayer-volume .xgplayer-icon{margin-top:8px;cursor:pointer;position:absolute;bottom:-9px}.xgplayer-skin-default .xgplayer-volume .xgplayer-icon div{position:absolute}.xgplayer-skin-default .xgplayer-volume .xgplayer-icon .xgplayer-icon-large{display:block}.xgplayer-skin-default .xgplayer-volume .xgplayer-icon .xgplayer-icon-muted,.xgplayer-skin-default .xgplayer-volume .xgplayer-icon .xgplayer-icon-small{display:none}.xgplayer-skin-default .xgplayer-slider{display:none;position:absolute;width:28px;height:92px;background:rgba(0,0,0,.54);border-radius:1px;bottom:42px;outline:none}.xgplayer-skin-default .xgplayer-slider:after{content:" ";display:block;height:15px;width:28px;position:absolute;bottom:-15px;left:0;z-index:20}.xgplayer-skin-default .xgplayer-bar,.xgplayer-skin-default .xgplayer-drag{display:block;position:absolute;bottom:6px;left:12px;background:hsla(0,0%,100%,.3);border-radius:100px;width:4px;height:76px;outline:none;cursor:pointer}.xgplayer-skin-default .xgplayer-drag{bottom:0;left:0;background:#fa1f41;max-height:76px}.xgplayer-skin-default .xgplayer-drag:after{content:" ";display:inline-block;width:8px;height:8px;background:#fff;box-shadow:0 0 5px 0 rgba(0,0,0,.26);position:absolute;border-radius:50%;left:-2px;top:-6px}.xgplayer-skin-default.xgplayer-volume-active .xgplayer-slider,.xgplayer-skin-default.xgplayer-volume-large .xgplayer-volume .xgplayer-icon .xgplayer-icon-large{display:block}.xgplayer-skin-default.xgplayer-volume-large .xgplayer-volume .xgplayer-icon .xgplayer-icon-muted,.xgplayer-skin-default.xgplayer-volume-large .xgplayer-volume .xgplayer-icon .xgplayer-icon-small,.xgplayer-skin-default.xgplayer-volume-small .xgplayer-volume .xgplayer-icon .xgplayer-icon-large{display:none}.xgplayer-skin-default.xgplayer-volume-small .xgplayer-volume .xgplayer-icon .xgplayer-icon-small{display:block}.xgplayer-skin-default.xgplayer-volume-muted .xgplayer-volume .xgplayer-icon .xgplayer-icon-large,.xgplayer-skin-default.xgplayer-volume-muted .xgplayer-volume .xgplayer-icon .xgplayer-icon-small,.xgplayer-skin-default.xgplayer-volume-small .xgplayer-volume .xgplayer-icon .xgplayer-icon-muted{display:none}.xgplayer-skin-default.xgplayer-volume-muted .xgplayer-volume .xgplayer-icon .xgplayer-icon-muted{display:block}.xgplayer-skin-default.xgplayer-mobile .xgplayer-volume .xgplayer-slider{display:none}',""])},function(e,t){e.exports=function(e){var t=[];return t.toString=function(){return this.map((function(t){var n=function(e,t){var n=e[1]||"",r=e[3];if(!r)return n;if(t&&"function"==typeof btoa){var o=(i=r,"/*# sourceMappingURL=data:application/json;charset=utf-8;base64,"+btoa(unescape(encodeURIComponent(JSON.stringify(i))))+" */"),a=r.sources.map((function(e){return"/*# sourceURL="+r.sourceRoot+e+" */"}));return[n].concat(a).concat([o]).join("\n")}var i;return[n].join("\n")}(t,e);return t[2]?"@media "+t[2]+"{"+n+"}":n})).join("")},t.i=function(e,n){"string"==typeof e&&(e=[[null,e,""]]);for(var r={},o=0;o<this.length;o++){var a=this[o][0];"number"==typeof a&&(r[a]=!0)}for(o=0;o<e.length;o++){var i=e[o];"number"==typeof i[0]&&r[i[0]]||(n&&!i[2]?i[2]=n:n&&(i[2]="("+i[2]+") and ("+n+")"),t.push(i))}},t}},function(e,t,n){var r,o,a={},i=(r=function(){return window&&document&&document.all&&!window.atob},function(){return void 0===o&&(o=r.apply(this,arguments)),o}),l=function(e){return document.querySelector(e)},u=function(e){var t={};return function(e){if("function"==typeof e)return e();if(void 0===t[e]){var n=l.call(this,e);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(e){n=null}t[e]=n}return t[e]}}(),s=null,c=0,f=[],d=n(13);function p(e,t){for(var n=0;n<e.length;n++){var r=e[n],o=a[r.id];if(o){o.refs++;for(var i=0;i<o.parts.length;i++)o.parts[i](r.parts[i]);for(;i<r.parts.length;i++)o.parts.push(x(r.parts[i],t))}else{var l=[];for(i=0;i<r.parts.length;i++)l.push(x(r.parts[i],t));a[r.id]={id:r.id,refs:1,parts:l}}}}function v(e,t){for(var n=[],r={},o=0;o<e.length;o++){var a=e[o],i=t.base?a[0]+t.base:a[0],l={css:a[1],media:a[2],sourceMap:a[3]};r[i]?r[i].parts.push(l):n.push(r[i]={id:i,parts:[l]})}return n}function g(e,t){var n=u(e.insertInto);if(!n)throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");var r=f[f.length-1];if("top"===e.insertAt)r?r.nextSibling?n.insertBefore(t,r.nextSibling):n.appendChild(t):n.insertBefore(t,n.firstChild),f.push(t);else if("bottom"===e.insertAt)n.appendChild(t);else{if("object"!=typeof e.insertAt||!e.insertAt.before)throw new Error("[Style Loader]\n\n Invalid value for parameter 'insertAt' ('options.insertAt') found.\n Must be 'top', 'bottom', or Object.\n (https://github.com/webpack-contrib/style-loader#insertat)\n");var o=u(e.insertInto+" "+e.insertAt.before);n.insertBefore(t,o)}}function m(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e);var t=f.indexOf(e);t>=0&&f.splice(t,1)}function y(e){var t=document.createElement("style");return e.attrs.type="text/css",h(t,e.attrs),g(e,t),t}function h(e,t){Object.keys(t).forEach((function(n){e.setAttribute(n,t[n])}))}function x(e,t){var n,r,o,a;if(t.transform&&e.css){if(!(a=t.transform(e.css)))return function(){};e.css=a}if(t.singleton){var i=c++;n=s||(s=y(t)),r=k.bind(null,n,i,!1),o=k.bind(null,n,i,!0)}else e.sourceMap&&"function"==typeof URL&&"function"==typeof URL.createObjectURL&&"function"==typeof URL.revokeObjectURL&&"function"==typeof Blob&&"function"==typeof btoa?(n=function(e){var t=document.createElement("link");return e.attrs.type="text/css",e.attrs.rel="stylesheet",h(t,e.attrs),g(e,t),t}(t),r=L.bind(null,n,t),o=function(){m(n),n.href&&URL.revokeObjectURL(n.href)}):(n=y(t),r=C.bind(null,n),o=function(){m(n)});return r(e),function(t){if(t){if(t.css===e.css&&t.media===e.media&&t.sourceMap===e.sourceMap)return;r(e=t)}else o()}}e.exports=function(e,t){if("undefined"!=typeof DEBUG&&DEBUG&&"object"!=typeof document)throw new Error("The style-loader cannot be used in a non-browser environment");(t=t||{}).attrs="object"==typeof t.attrs?t.attrs:{},t.singleton||"boolean"==typeof t.singleton||(t.singleton=i()),t.insertInto||(t.insertInto="head"),t.insertAt||(t.insertAt="bottom");var n=v(e,t);return p(n,t),function(e){for(var r=[],o=0;o<n.length;o++){var i=n[o];(l=a[i.id]).refs--,r.push(l)}e&&p(v(e,t),t);for(o=0;o<r.length;o++){var l;if(0===(l=r[o]).refs){for(var u=0;u<l.parts.length;u++)l.parts[u]();delete a[l.id]}}}};var b,w=(b=[],function(e,t){return b[e]=t,b.filter(Boolean).join("\n")});function k(e,t,n,r){var o=n?"":r.css;if(e.styleSheet)e.styleSheet.cssText=w(t,o);else{var a=document.createTextNode(o),i=e.childNodes;i[t]&&e.removeChild(i[t]),i.length?e.insertBefore(a,i[t]):e.appendChild(a)}}function C(e,t){var n=t.css,r=t.media;if(r&&e.setAttribute("media",r),e.styleSheet)e.styleSheet.cssText=n;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(n))}}function L(e,t,n){var r=n.css,o=n.sourceMap,a=void 0===t.convertToAbsoluteUrls&&o;(t.convertToAbsoluteUrls||a)&&(r=d(r)),o&&(r+="\n/*# sourceMappingURL=data:application/json;base64,"+btoa(unescape(encodeURIComponent(JSON.stringify(o))))+" */");var i=new Blob([r],{type:"text/css"}),l=e.href;e.href=URL.createObjectURL(i),l&&URL.revokeObjectURL(l)}},function(e,t){e.exports=function(e){var t="undefined"!=typeof window&&window.location;if(!t)throw new Error("fixUrls requires window.location");if(!e||"string"!=typeof e)return e;var n=t.protocol+"//"+t.host,r=n+t.pathname.replace(/\/[^\/]*$/,"/");return e.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi,(function(e,t){var o,a=t.trim().replace(/^"(.*)"$/,(function(e,t){return t})).replace(/^'(.*)'$/,(function(e,t){return t}));return/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/|\s*$)/i.test(a)?e:(o=0===a.indexOf("//")?a:0===a.indexOf("/")?n+a:r+a.replace(/^\.\//,""),"url("+JSON.stringify(o)+")")}))}}])}));