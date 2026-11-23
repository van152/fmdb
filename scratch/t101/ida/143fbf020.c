char __fastcall sub_143FBF020(__int64 *a1, unsigned __int64 a2)
{
  __int64 v4; // rdx
  __int64 v5; // rax
  unsigned __int64 v6; // rbx
  unsigned __int64 v7; // rcx
  unsigned __int64 v8; // r12
  __int64 v9; // r12
  __int64 v10; // r14
  unsigned __int64 v11; // rax
  __int64 v12; // rdx
  unsigned __int64 v13; // rcx
  unsigned __int64 v14; // rbx
  __int64 v15; // rbx
  unsigned __int64 v16; // rcx
  __int64 v17; // r8
  __int64 v18; // r15
  unsigned __int64 v19; // rcx
  unsigned __int64 v20; // rbx

  v4 = *a1;
  v5 = a1[1];
  v6 = (v5 - *a1) >> 5;
  if ( v6 <= a2 )
  {
    if ( v6 < a2 )
    {
      v7 = (a1[2] - v4) >> 5;
      if ( v7 >= a2 )
      {
        v19 = a2 - v6;
        if ( a2 != v6 )
        {
          v20 = ~v6;
          if ( (v19 & 1) != 0 )
          {
            *(_QWORD *)(v5 + 16) = 0;
            *(_QWORD *)(v5 + 24) = 0;
            *(_DWORD *)v5 = 124518401;
            *(_QWORD *)(v5 + 4) = -1;
            *(_QWORD *)(v5 + 9) = -1;
            *(_DWORD *)(v5 + 20) = -1;
            *(_WORD *)(v5 + 28) = -1;
            v5 += 32;
            --v19;
          }
          if ( a2 + v20 != 0 )
          {
            do
            {
              *(_QWORD *)(v5 + 16) = 0;
              *(_QWORD *)(v5 + 24) = 0;
              *(_DWORD *)v5 = 124518401;
              *(_QWORD *)(v5 + 4) = -1;
              *(_QWORD *)(v5 + 9) = -1;
              *(_DWORD *)(v5 + 20) = -1;
              *(_WORD *)(v5 + 28) = -1;
              *(_QWORD *)(v5 + 48) = 0;
              *(_QWORD *)(v5 + 56) = 0;
              *(_DWORD *)(v5 + 32) = 124518401;
              *(_QWORD *)(v5 + 36) = -1;
              *(_QWORD *)(v5 + 41) = -1;
              *(_DWORD *)(v5 + 52) = -1;
              *(_WORD *)(v5 + 60) = -1;
              v5 += 64;
              v19 -= 2LL;
            }
            while ( v19 != 0 );
          }
        }
        a1[1] = v5;
      }
      else
      {
        if ( a2 >> 59 != 0 )
          sub_1400526C0();
        v8 = v7 + (v7 >> 1);
        if ( v8 <= a2 )
          v8 = a2;
        if ( v7 > 0x7FFFFFFFFFFFFFFLL - (v7 >> 1) )
          v8 = 0x7FFFFFFFFFFFFFFLL;
        v9 = 32 * v8;
        v10 = sub_1407E4490(qword_141ABD470, v9);
        v11 = a2 - v6;
        if ( a2 != v6 )
        {
          v12 = 32 * v6;
          v13 = v10 + 32 * v6;
          v14 = ~v6;
          if ( (v11 & 1) != 0 )
          {
            *(_QWORD *)(v13 + 24) = 0;
            *(_QWORD *)(v13 + 16) = 0;
            *(_DWORD *)v13 = 124518401;
            *(_QWORD *)(v10 + v12 + 9) = -1;
            *(_QWORD *)(v10 + v12 + 4) = -1;
            *(_DWORD *)(v10 + v12 + 20) = -1;
            *(_WORD *)(v10 + v12 + 28) = -1;
            v13 += 32LL;
            --v11;
          }
          if ( a2 + v14 != 0 )
          {
            do
            {
              *(_QWORD *)(v13 + 16) = 0;
              *(_QWORD *)(v13 + 24) = 0;
              *(_DWORD *)v13 = 124518401;
              *(_QWORD *)(v13 + 4) = -1;
              *(_QWORD *)(v13 + 9) = -1;
              *(_DWORD *)(v13 + 20) = -1;
              *(_WORD *)(v13 + 28) = -1;
              *(_QWORD *)(v13 + 48) = 0;
              *(_QWORD *)(v13 + 56) = 0;
              *(_DWORD *)(v13 + 32) = 124518401;
              *(_QWORD *)(v13 + 36) = -1;
              *(_QWORD *)(v13 + 41) = -1;
              *(_DWORD *)(v13 + 52) = -1;
              *(_WORD *)(v13 + 60) = -1;
              v13 += 64LL;
              v11 -= 2LL;
            }
            while ( v11 != 0 );
          }
        }
        LOBYTE(v5) = sub_141758A00(v10, *a1, a1[1] - *a1);
        v15 = *a1;
        if ( *a1 != 0 )
        {
          v16 = a1[2] - v15;
          if ( v16 == -1 )
            v16 = *(unsigned int *)(v15 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v17 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > v16)
            && (v18 = *(_QWORD *)(v17 + 8 * v16)) != 0 )
          {
            MEMORY[0x1419475D8](v18 + 32, v15 - *(unsigned int *)(v18 + 120));
            LOBYTE(v5) = *(_BYTE *)(v18 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 64)) != 0;
            if ( (_BYTE)v5 == 0 && *(_BYTE *)(v18 + 97) != 0 )
              LOBYTE(v5) = sub_1412D33C0(v18);
          }
          else
          {
            LOBYTE(v5) = MEMORY[0x141948990](v15 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *a1 = v10;
        a1[1] = v10 + 32 * a2;
        a1[2] = v10 + v9;
      }
    }
  }
  else
  {
    a1[1] = 32 * a2 + v4;
  }
  return v5;
}
