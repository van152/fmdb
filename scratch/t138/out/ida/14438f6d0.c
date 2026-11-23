char __fastcall sub_14438F6D0(__int64 *a1, unsigned __int64 a2)
{
  __int64 v4; // rdx
  __int64 v5; // rax
  unsigned __int64 v6; // rbx
  unsigned __int64 v7; // rcx
  unsigned __int64 v8; // r12
  __int64 v9; // r12
  __int64 v10; // r14
  unsigned __int64 v11; // rax
  unsigned __int64 v12; // rcx
  unsigned __int64 v13; // rbx
  __int64 v14; // rsi
  unsigned __int64 v15; // rcx
  __int64 v16; // rsi
  unsigned __int64 v17; // rcx
  __int64 v18; // rbx
  __int64 v19; // r15
  unsigned __int64 v20; // rcx
  unsigned __int64 v21; // rbx
  __int64 v22; // rsi

  v4 = *a1;
  v5 = a1[1];
  v6 = (v5 - *a1) >> 4;
  if ( v6 <= a2 )
  {
    if ( v6 < a2 )
    {
      v7 = (a1[2] - v4) >> 4;
      if ( v7 >= a2 )
      {
        v20 = a2 - v6;
        if ( a2 != v6 )
        {
          v21 = a2 + ~v6;
          if ( (v20 & 3) != 0 )
          {
            v22 = 0;
            do
            {
              *(_DWORD *)(v5 + 12) = 0;
              *(_WORD *)v5 = 25548;
              *(_QWORD *)(v5 + 2) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v5 + 9) = -252645136;
              v5 += 16;
              ++v22;
            }
            while ( (v20 & 3) != v22 );
            v20 -= v22;
          }
          if ( v21 >= 3 )
          {
            do
            {
              *(_DWORD *)(v5 + 12) = 0;
              *(_WORD *)v5 = 25548;
              *(_QWORD *)(v5 + 2) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v5 + 9) = -252645136;
              *(_WORD *)(v5 + 28) = 0;
              *(_WORD *)(v5 + 16) = 25548;
              *(_QWORD *)(v5 + 18) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v5 + 25) = -252645136;
              *(_DWORD *)(v5 + 30) = 1674313728;
              *(_DWORD *)(v5 + 44) = 0;
              *(_QWORD *)(v5 + 34) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v5 + 41) = -252645136;
              *(_DWORD *)(v5 + 60) = 0;
              *(_WORD *)(v5 + 48) = 25548;
              *(_QWORD *)(v5 + 50) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v5 + 57) = -252645136;
              v5 += 64;
              v20 -= 4LL;
            }
            while ( v20 != 0 );
          }
        }
        a1[1] = v5;
      }
      else
      {
        if ( a2 >> 60 != 0 )
          sub_1400526C0();
        v8 = v7 + (v7 >> 1);
        if ( v8 <= a2 )
          v8 = a2;
        if ( v7 > 0xFFFFFFFFFFFFFFFLL - (v7 >> 1) )
          v8 = 0xFFFFFFFFFFFFFFFLL;
        v9 = 16 * v8;
        v10 = sub_1407E4490(a1: qword_141ABD470, a2: v9);
        v11 = a2 - v6;
        if ( a2 != v6 )
        {
          v12 = v10 + 16 * v6;
          v13 = a2 + ~v6;
          if ( (v11 & 3) != 0 )
          {
            v14 = 0;
            do
            {
              *(_DWORD *)(v12 + 12) = 0;
              *(_WORD *)v12 = 25548;
              *(_QWORD *)(v12 + 2) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v12 + 9) = -252645136;
              v12 += 16LL;
              ++v14;
            }
            while ( (v11 & 3) != v14 );
            v11 -= v14;
          }
          if ( v13 >= 3 )
          {
            v15 = v12 + 62;
            do
            {
              *(_DWORD *)(v15 - 50) = 0;
              *(_WORD *)(v15 - 62) = 25548;
              *(_QWORD *)(v15 - 60) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v15 - 53) = -252645136;
              *(_WORD *)(v15 - 34) = 0;
              *(_WORD *)(v15 - 46) = 25548;
              *(_QWORD *)(v15 - 44) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v15 - 37) = -252645136;
              *(_DWORD *)(v15 - 32) = 1674313728;
              *(_DWORD *)(v15 - 18) = 0;
              *(_QWORD *)(v15 - 28) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v15 - 21) = -252645136;
              *(_DWORD *)(v15 - 2) = 0;
              *(_WORD *)(v15 - 14) = 25548;
              *(_QWORD *)(v15 - 12) = 0xF0F0F0F0F0F0F0F0uLL;
              *(_DWORD *)(v15 - 5) = -252645136;
              v15 += 64LL;
              v11 -= 4LL;
            }
            while ( v11 != 0 );
          }
        }
        LOBYTE(v5) = sub_141758A00(a1: v10, a2: *a1, a3: a1[1] - *a1);
        v16 = *a1;
        if ( *a1 != 0 )
        {
          v17 = a1[2] - v16;
          if ( v17 == -1 )
            v17 = *(unsigned int *)(v16 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v18 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v18) >> 3 > v17)
            && (v19 = *(_QWORD *)(v18 + 8 * v17)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v19 + 32, a2: v16 - *(unsigned int *)(v19 + 120));
            LOBYTE(v5) = *(_BYTE *)(v19 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 + 64)) != 0;
            if ( (_BYTE)v5 == 0 && *(_BYTE *)(v19 + 97) != 0 )
              LOBYTE(v5) = sub_1412D33C0(a1: v19);
          }
          else
          {
            LOBYTE(v5) = MEMORY[0x141948990](a1: v16 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *a1 = v10;
        a1[1] = v10 + 16 * a2;
        a1[2] = v10 + v9;
      }
    }
  }
  else
  {
    a1[1] = 16 * a2 + v4;
  }
  return v5;
}
