def sim(M, pc=0x100, ac=0, inp=None, trace=True):
    out=[];steps=[]
    while True:
        ir=M[pc]; pc+=1; op=ir>>12; x=ir&0xFFF
        if op==1: ac=M[x]
        elif op==2: M[x]=ac
        elif op==3: ac=(ac+M[x])
        elif op==4: ac=(ac-M[x])
        elif op==5: ac=inp.pop(0)
        elif op==6: out.append(ac)
        elif op==7: steps.append((hex(ir),ac)); break
        elif op==8:
            c=(x>>10)&3
            if (c==0 and ac<0) or (c==1 and ac==0) or (c==2 and ac>0): pc+=1
        elif op==9: pc=x
        steps.append((hex(ir),ac))
    return ac,out,steps,M
print('--conversions')
print(0x3C7, bin(0x3C7), format(200,'08b'), hex(200), 0xFFD6, 0xFFD6-65536, format((-2)&0xFFFFFFFF,'08X'))
print('2.5GHz',1/2.5, 'x5', 5/2.5)
print('--cache Q14', hex(0xABCDE&31), (0xABCDE&31), ((0xABCDE>>5)&255), hex((0xABCDE>>5)&255), 0xABCDE>>13, hex(0xABCDE>>13))
print('4-way 64 sets: set', (0xABCDE>>5)&63, 'tag', 0xABCDE>>11, hex(0xABCDE>>11))
print('Q8 fully assoc tag bits 24-4 =',20, 'tag value', hex(0x5A3C8F>>4))
print('Q8 4-way 256 sets: set', (0x5A3C8F>>4)&255, hex((0x5A3C8F>>4)&255), 'tag', hex(0x5A3C8F>>12))
def setassoc(refs,nsets,ways,policy='LRU'):
    S=[[] for _ in range(nsets)];res=[]
    for b in refs:
        s=S[b%nsets]
        if b in s:
            res.append('H')
            if policy=='LRU': s.remove(b); s.append(b)
        else:
            res.append('M')
            if len(s)==ways: s.pop(0)
            s.append(b)
    return ''.join(res), [list(x) for x in S]
r=[0,1,13,2,8,0,14,1]
print('S6-7 direct8', setassoc(r,8,1)); print('fully4 LRU',setassoc(r,1,4)); print('fully4 FIFO',setassoc(r,1,4,'FIFO')); print('4way8 LRU',setassoc(r,2,4)); print('4way FIFO',setassoc(r,2,4,'FIFO'))
r2=[0,4,8,0,4,1,5,1]
print('Q15 2way 2sets LRU',setassoc(r2,2,2),'FIFO',setassoc(r2,2,2,'FIFO'),'direct4',setassoc(r2,4,1),'fully4 LRU',setassoc(r2,1,4))
r3=[1,2,1,3,1,2]; print('lru vs fifo',setassoc(r3,1,2),setassoc(r3,1,2,'FIFO'))
r4=[2,3,6,2,10,3,6]; print('direct4 P11',setassoc(r4,4,1))
print('--pipelines', 160000/32160, 40000/((5+199)*40), (6+499)*15, 500*90, 500*90/((6+499)*15))
print('six-stage diagram 4 instr', (6+4-1))
print('--cpu', 2e9*1.5/3e9, 2e9*1.2/2.4e9)
print('EAT', 0.95*5+0.05*80, 0.99*10+0.01*200)
print('expanding classic', 15*4096+14*256+31*16+16, 'Q9', 13*4096+40*256+50*16+16)
print('S4-5 ex3', 5*256+45*16+32)
print('moore', 10*2**(3/1.5))
print('--MARIE quiz Q5'); M={0x100:0x1106,0x101:0x3107,0x102:0x4108,0x103:0x2109,0x104:0x6000,0x105:0x7000,0x106:60,0x107:40,0x108:15,0x109:0}
print(sim(M)[:3])
print('--S2-3 program'); M={0x100:0x1108,0x101:0x3109,0x102:0x9106,0x103:0x3109,0x104:0x2108,0x105:0x7000,0x106:0x3108,0x107:0x9103,0x108:0x23,0x109:1}
a,o,s,M=sim(M); print([(i,hex(v)) for i,v in s], hex(M[0x108]))
print('--Q8 equal program'); M={0x100:0x1109,0x101:0x410A,0x102:0x8400,0x103:0x9106,0x104:0x110B,0x105:0x9107,0x106:0x110C,0x107:0x6000,0x108:0x7000,0x109:7,0x10A:7,0x10B:1,0x10C:0}
print(sim(M)[:3])
M={0x100:0x1109,0x101:0x410A,0x102:0x8400,0x103:0x9106,0x104:0x110B,0x105:0x9107,0x106:0x110C,0x107:0x6000,0x108:0x7000,0x109:7,0x10A:5,0x10B:1,0x10C:0}
print('unequal', sim(M)[:2])
print('--loop: Prod = A*B by repeated add')
# 100 Loop, LOAD Prod / 101 ADD A / 102 STORE Prod / 103 LOAD Cnt / 104 SUBT One / 105 STORE Cnt / 106 SKIPCOND 400 / 107 JUMP Loop / 108 LOAD Prod / 109 OUTPUT / 10A HALT / 10B A DEC 4 / 10C Cnt DEC 3 / 10D One DEC 1 / 10E Prod DEC 0
M={0x100:0x110E,0x101:0x310B,0x102:0x210E,0x103:0x110C,0x104:0x410D,0x105:0x210C,0x106:0x8400,0x107:0x9100,0x108:0x110E,0x109:0x6000,0x10A:0x7000,0x10B:4,0x10C:3,0x10D:1,0x10E:0}
a,o,s,M=sim(M); print(a,o,len(s))
print('VA', hex(0x3A7F>>12), hex(0x3A7F&0xFFF), hex((5<<12)|0xA7F))
print('two comp 8bit -128', format(128,'08b'), 'neg 1', format(255,'08b'))
print('overflow 0x7F+1 8-bit', hex(0x80), 0x80-256, '100+50 8bit', (150)-256)
print('sign ext -5 8->16', format((-5)&0xFF,'08b'), format((-5)&0xFFFF,'016b'))
print('ME packed', 0x4D, 0x45, 'HI', hex(ord('H')), hex(ord('I')), 'Hi', hex(ord('h')))
print('dec60 hex', hex(60), 'dec -1 16bit', hex((-1)&0xFFFF))
print('0x1234 32 LE', '34 12 00 00')
print('hex sub 0x0100-0x0001', hex(0x100-1), '0x00FF+0x0001', hex(0xFF+1), '0x2A+0x3C', hex(0x2A+0x3C), 0x2A+0x3C)
print('jargon 4.2GHz cycle', 1/4.2)
