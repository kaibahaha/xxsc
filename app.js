const initial={hp:10,distance:3,level:1,wave:0,over:false};let state={...initial};const $=id=>document.getElementById(id);
function render(){ $('hp').textContent=state.hp;$('distance').textContent=state.distance;$('level').textContent=state.level;$('status').textContent=state.over?'防线失守':state.distance<=0?'本波守住':'第 '+(state.wave+1)+' 波进行中';$('turn').disabled=state.over;}
function note(text){const li=document.createElement('li');li.textContent=text;$('log').prepend(li);}
$('build').onclick=()=>{if(state.over)return;state.level++;note('箭塔升级到 '+state.level+' 级');render();};
$('turn').onclick=()=>{if(state.over)return;state.wave++;const damage=state.level;state.distance=Math.max(0,state.distance-damage);if(state.distance===0){note('箭塔击退第 '+state.wave+' 波');state.distance=3+state.wave;}else{state.hp-=2;note('敌军逼近，城墙受到 2 点伤害');if(state.hp<=0){state.hp=0;state.over=true;}}render();};
$('reset').onclick=()=>{state={...initial};$('log').replaceChildren();render();};render();
