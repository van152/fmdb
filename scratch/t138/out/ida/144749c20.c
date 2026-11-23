__int64 __fastcall sub_144749C20(_QWORD *a1, _QWORD *a2)
{
  __int64 v2; // rbp
  __int64 v5; // rbx
  __int64 v6; // rax
  unsigned __int64 v7; // rdi
  __int64 v8; // rbx
  int v9; // r14d
  __int64 v11; // rax
  __int16 v12; // cx
  __int64 v13; // r8
  __int64 v14; // r14
  __int64 v15; // rdx
  __int64 v16; // r15
  int v17; // ebx
  unsigned __int64 v18; // rdi
  unsigned int v19; // ebx
  int v20; // eax
  __int64 v21; // rax
  __int64 v22; // rbx
  __int64 v23; // rdi
  int v24; // r14d
  __int64 v25; // r12
  int v26; // ecx
  unsigned __int64 v27; // rdx
  unsigned int v28; // ecx
  int v29; // ecx
  unsigned __int64 v30; // rdx
  unsigned int v31; // ecx
  _BYTE v32[8]; // [rsp+28h] [rbp-50h] BYREF
  _BYTE v33[7]; // [rsp+30h] [rbp-48h] BYREF
  char v34; // [rsp+37h] [rbp-41h] BYREF
  _DWORD v35[16]; // [rsp+38h] [rbp-40h] BYREF

  sub_140F9F4A0(a1: v32);
  if ( *a1 != a1[1] )
    a1[1] = *a1;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v34, a3: 1);
  if ( *(_DWORD *)(v5 + 16) != 0
    || (sub_14141D290(a1: v35, a2, a3: a1, a4: v33), v35[0] != 0)
    || (unsigned __int8)sub_140F80B80(a1: a1 + 3, a2, a3: 1) == 0 )
  {
    LODWORD(v2) = 0;
  }
  else
  {
    if ( (*(_BYTE *)(*a2 + 12LL) & 2) != 0 )
    {
      v6 = a1[1] - *a1;
      if ( v6 != 0 )
      {
        v7 = ((unsigned __int64)((unsigned __int128)(0x6666666666666667LL * (__int128)v6) >> 64) >> 63) + v6 / 20;
        v8 = 20 * v7;
        v2 = -20LL * v7;
        v9 = 404754432;
        do
        {
          --v7;
          v11 = *a1;
          v12 = *(_WORD *)(*a1 + v8 - 8);
          if ( (unsigned int)v12 <= 0x1C && _bittest(&v9, v12) || v12 == 233 || v12 == 205 )
          {
            if ( v12 == 233 )
            {
              *(_WORD *)(v11 + v8 - 8) = 217;
            }
            else
            {
              sub_141758A00(a1: v11 + v8 - 20, a2: v11 + v8, a3: v2 + a1[1] - v11);
              a1[1] -= 20LL;
            }
          }
          v8 -= 20;
          v2 += 20;
        }
        while ( v7 != 0 );
      }
    }
    LOBYTE(v2) = 1;
    if ( (unsigned __int8)sub_1400015E0() == 0 )
    {
      v13 = a1[1];
      v14 = v13 - *a1;
      if ( v14 != 0 )
      {
        v15 = v14 / 20;
        if ( ((v14 / 20) & 1) != 0 )
        {
          v16 = v15 - 1;
          v17 = *(__int16 *)(*a1 + 20 * (v15 - 1) + 12);
          v18 = (unsigned int)(v17 - 25);
          if ( (unsigned int)v18 > 0x2B || (v21 = 0x80800008001LL, !_bittest64(&v21, v18)) )
          {
            v19 = v17 - 204;
            if ( v19 > 7 || (v20 = 225, !_bittest(&v20, v19)) )
            {
              sub_141758A00(a1: *a1 + 20 * (v15 - 1), a2: *a1 + 20 * v15, a3: v13 - (*a1 + 20 * v15));
              v13 = a1[1] - 20LL;
              a1[1] = v13;
            }
          }
        }
        else
        {
          v16 = v14 / 20;
        }
        if ( (unsigned __int64)(v14 - 20) >= 0x14 )
        {
          v22 = 20 * v16;
          v23 = -20 * v16;
          v24 = 225;
          v25 = 0x80800008001LL;
          do
          {
            v26 = *(__int16 *)(*a1 + v22 - 8);
            v27 = (unsigned int)(v26 - 25);
            if ( (unsigned int)v27 > 0x2B || !_bittest64(&v25, v27) )
            {
              v28 = v26 - 204;
              if ( v28 > 7 || !_bittest(&v24, v28) )
              {
                sub_141758A00(a1: *a1 + v22 - 20, a2: *a1 + v22, a3: v23 + v13 - *a1);
                v13 = a1[1] - 20LL;
                a1[1] = v13;
              }
            }
            v16 -= 2;
            v29 = *(__int16 *)(*a1 + v22 - 28);
            v30 = (unsigned int)(v29 - 25);
            if ( (unsigned int)v30 > 0x2B || !_bittest64(&v25, v30) )
            {
              v31 = v29 - 204;
              if ( v31 > 7 || !_bittest(&v24, v31) )
              {
                sub_141758A00(a1: *a1 + v22 - 40, a2: *a1 + v22 - 20, a3: v23 + v13 - *a1 + 20);
                v13 = a1[1] - 20LL;
                a1[1] = v13;
              }
            }
            v22 -= 40;
            v23 += 40;
          }
          while ( v16 != 0 );
        }
      }
    }
  }
  if ( v32[0] == 0 )
    byte_141B5FC2C = 0;
  return (unsigned int)v2;
}
