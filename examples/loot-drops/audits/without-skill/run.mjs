import { legendaryChance, pull, HARD_PITY } from '../drops.js';
// exact legendary distribution
let surv=1, E=0, dist=[], n=0;
for (let k=1;k<=200;k++){ const p=legendaryChance(k); const f=surv*p; dist.push([k,p,f]); E+=k*f; surv*=1-p; if(surv<1e-15){n=k;break;} }
console.log('max pulls to legendary:', n, 'E[pulls]:', E.toFixed(3), 'overall rate:', (100/E).toFixed(3)+'%');
let cum=0; for (const [k,p,f] of dist){ cum+=f; if(k>=74||k===1||k===60) console.log(k, p.toFixed(3), f.toFixed(5), cum.toFixed(5)); }
const med = (()=>{let c=0;for(const [k,,f] of dist){c+=f;if(c>=0.5)return k}})(); console.log('median', med);
console.log('P(reach pull 76)', dist.slice(0,75).reduce((s,d)=>s-d[2],1).toFixed(4));
// simulation
let st={sinceLegendary:0,sinceEpic:0}, N=2e7, c={legendary:0,epic:0,rare:0}, maxGapE=0,gapE=0, maxL=0,gapL=0, pityEpic=0;
for(let i=0;i<N;i++){ const r=pull(st); c[r]++; gapL++; gapE++;
 if(r==='legendary'){maxL=Math.max(maxL,gapL);gapL=0;}
 if(r!=='rare'){maxGapE=Math.max(maxGapE,gapE);gapE=0;} }
console.log('sim', Object.fromEntries(Object.entries(c).map(([k,v])=>[k,(100*v/N).toFixed(3)+'%'])), 'maxLegGap',maxL,'maxEpicOrBetterGap',maxGapE, 'mean pulls/leg', (N/c.legendary).toFixed(2));
// epic-only rate excluding pity
