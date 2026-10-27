function stats(base, from, step, hard){ let s=1,E=0,max=0,cum=0,med=0;
 for(let k=1;k<=hard;k++){ let p = k>=hard?1 : k>from ? Math.min(1,base+step*(k-from)) : base; const f=s*p; E+=k*f; cum+=f; if(!med&&cum>=0.5)med=k; s*=1-p; if(f>0)max=k; if(s<=0)break;}
 return {base,from,step,hard,E:E.toFixed(2),rate:(100/E).toFixed(3)+'%',median:med,max}; }
console.log(stats(0.004,76,0.05,91)); // current behaviour (hard at 91)
console.log(stats(0.004,76,0.05,90)); // off-by-one fixed only
for (const from of [50,55,58,60]) for (const step of [0.05,0.06]) console.log(stats(0.006,from,step,90));
for (const from of [55,58,60,62]) console.log(stats(0.004,from,0.06,90));
