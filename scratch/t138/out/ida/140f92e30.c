char __fastcall sub_140F92E30(_BYTE *a1, __int64 *a2, _QWORD *a3, _QWORD *a4, int a5)
{
  _DWORD *v9; // rsi
  int v10; // eax
  char v11; // al
  __int64 v12; // r8
  char result; // al
  __int64 v14; // rsi
  __int64 v15; // rsi
  __int64 v16; // rsi
  __int64 v17; // rsi
  unsigned __int64 v18; // rcx
  __int64 v19; // rax
  unsigned __int64 v20; // rdi
  __int64 v21; // rsi
  int v22; // eax
  __int64 v23; // rsi
  _QWORD *v24; // rdx
  _QWORD *v25; // rdx
  __int64 v26; // rax
  __int64 v27; // rax
  unsigned __int64 v28; // rax
  __int64 v29; // rbx
  __int64 i; // rdi
  _QWORD *v31; // rdx
  char v32; // [rsp+2Bh] [rbp-4Dh] BYREF
  int v33; // [rsp+2Ch] [rbp-4Ch] BYREF
  unsigned int v34; // [rsp+30h] [rbp-48h] BYREF
  __int16 v35; // [rsp+36h] [rbp-42h] BYREF
  unsigned __int64 v36; // [rsp+38h] [rbp-40h] BYREF
  _DWORD v37[13]; // [rsp+44h] [rbp-34h] BYREF

  v9 = (_DWORD *)*a3;
  v10 = *(_DWORD *)(*a3 + 12LL);
  if ( (v10 & 2) != 0 )
  {
    if ( a1[1450] != 0 || a5 == 1 && a1[1451] != 0 )
    {
      if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
        v12 = 4;
      else
        v12 = 8;
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2, a3: v12);
      return v9[4] == 0;
    }
    v11 = (2 * ~(_BYTE)v10) & 4;
    if ( byte_141AAE088 == 0 )
      v11 = 0;
    v32 = v11;
  }
  else
  {
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2: &v32, a3: 1);
    if ( v9[4] != 0 )
      return 0;
    v11 = v32;
  }
  *a2 = 0;
  if ( v11 == 0 )
  {
    v21 = *a3;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: &v34, a3: 2);
    if ( *(_DWORD *)(v21 + 16) == 0 )
    {
      v22 = (__int16)v34;
      if ( (__int16)v34 == -1 )
        return 1;
      LODWORD(v36) = (__int16)v34;
      if ( (_WORD)v34 == 0xFFFE )
      {
        v23 = *a3;
        (*(void (__fastcall **)(_QWORD, unsigned __int64 *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: &v36, a3: 4);
        if ( *(_DWORD *)(v23 + 16) != 0 )
          return 0;
        v22 = v36;
      }
      if ( v22 >= 0 )
      {
        v24 = (_QWORD *)a4[16];
        if ( (__int64)(v24[1] - *v24) >> 3 > (unsigned __int64)(unsigned int)v22 )
        {
          *a2 = *(_QWORD *)(*v24 + 8LL * (unsigned int)v22);
          return 1;
        }
      }
    }
    return 0;
  }
  v37[0] = 0;
  *a2 = 0;
  v14 = *a3;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: &v35, a3: 2);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  if ( v35 == -1 )
    return 1;
  v33 = v35;
  if ( v35 == -2 )
  {
    v15 = *a3;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: &v33, a3: 4);
    if ( *(_DWORD *)(v15 + 16) != 0 )
      return 0;
  }
  v16 = *a3;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: &v34, a3: 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a3;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a3 + 40LL))(a1: *a3, a2: v37, a3: 4);
  result = 0;
  if ( *(_DWORD *)(v17 + 16) == 0 )
  {
    v18 = (unsigned int)v33;
    if ( v33 >= 0 )
    {
      if ( a1[1400] != 0 || (v19 = a4[12], (a4[13] - v19) >> 3 <= (unsigned __int64)v35) )
      {
        v20 = *a2;
      }
      else
      {
        v20 = *(_QWORD *)(v19 + 8LL * (unsigned int)v33);
        *a2 = v20;
      }
      if ( v20 != 0 && *(_DWORD *)(v20 + 12) == v34 )
        return v20 != 0;
      v25 = (_QWORD *)a4[16];
      if ( (__int64)(v25[1] - *v25) >> 3 <= v18 )
      {
        *a2 = 0;
      }
      else
      {
        v20 = *(_QWORD *)(*v25 + 8 * v18);
        *a2 = v20;
        if ( v20 != 0 && *(_DWORD *)(v20 + 12) == v34 )
          return v20 != 0;
      }
      v36 = __PAIR64__(v37[0], v34);
      v26 = sub_140FAD530(a1: a4, a2: &v36);
      *a2 = v26;
      if ( v26 != 0 )
      {
        v20 = v26;
        if ( a1[1400] == 0 )
        {
          if ( a4[12] == a4[13] )
          {
            v27 = *(_QWORD *)(a4[16] + 8LL) - *(_QWORD *)a4[16];
            if ( v27 != 0 )
            {
              v28 = v27 >> 3;
              v29 = 1;
              if ( v28 >= 2 )
                v29 = v28;
              for ( i = 0; i != v29; ++i )
              {
                v36 = *(_QWORD *)(*(_QWORD *)a4[16] + 8 * i);
                sub_14083D020(a1: a4 + 12, a2: &v36, a3: i);
              }
              v20 = *a2;
            }
          }
          v36 = v20;
          sub_14083D020(a1: a4 + 12, a2: &v36, a3: v33);
          *(_DWORD *)(v20 + 8) = v33;
          v20 = *a2;
        }
      }
      else
      {
        v31 = (_QWORD *)a4[16];
        if ( (__int64)(v31[1] - *v31) >> 3 <= (unsigned __int64)v33 )
        {
          v20 = 0;
        }
        else
        {
          v20 = *(_QWORD *)(*v31 + 8LL * v33);
          *a2 = v20;
        }
      }
      return v20 != 0;
    }
  }
  return result;
}
