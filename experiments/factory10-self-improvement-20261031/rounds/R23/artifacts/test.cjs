'use strict';const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');const html=fs.readFileSync(__dirname+'/game.html','utf8');const match=html.match(/<script id="game-core">([\s\S]*?)<\/script>/);assert.ok(match);const ctx={module:{exports:{}}};vm.runInNewContext(match[1],ctx);const g=ctx.module.exports;const base=()=>g.initial();function rejects(name,state,action,pattern){test(name,()=>{const old=JSON.stringify(state);assert.throws(()=>g.step(state,action),pattern);assert.equal(JSON.stringify(state),old,'no mutation on rejection');});}
test('valid east move',()=>{const s=g.step(base(),{id:1,type:'move',dir:'E'});assert.equal(s.x,1);assert.equal(s.energy,11);});
test('deterministic replay',()=>{const a={id:1,type:'move',dir:'E'};assert.equal(JSON.stringify(g.step(base(),a)),JSON.stringify(g.step(base(),a)));});
rejects('missing id',base(),{type:'move',dir:'E'},/invalid id/);
rejects('invalid id type',base(),{id:'1',type:'move',dir:'E'},/invalid id/);
rejects('negative id',base(),{id:-1,type:'move',dir:'E'},/invalid id/);
rejects('unknown type',base(),{id:1,type:'publish'},/invalid type/);
rejects('invalid direction',base(),{id:1,type:'move',dir:'UP'},/invalid direction/);
rejects('out of bounds',base(),{id:1,type:'move',dir:'N'},/out of bounds/);
rejects('harvest outside ore',base(),{id:1,type:'harvest'},/no ore/);
rejects('deposit away from base',{...base(),x:1,cargo:1},{id:1,type:'deposit'},/not at base/);
rejects('empty deposit',base(),{id:1,type:'deposit'},/empty cargo/);
rejects('no energy',{...base(),energy:0},{id:1,type:'move',dir:'E'},/out of energy/);
rejects('duplicate event',{...base(),seen:[1]},{id:1,type:'move',dir:'E'},/duplicate event/);
rejects('completed game',{...base(),gold:2},{id:1,type:'move',dir:'E'},/game finished/);
rejects('null action',base(),null,/invalid action/);
rejects('malformed state',{}, {id:1,type:'move',dir:'E'},/invalid state/);
